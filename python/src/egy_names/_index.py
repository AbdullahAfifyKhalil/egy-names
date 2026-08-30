"""Lookup indices for fast name resolution, translation, and correction.

Builds several in-memory hash tables on first access:
  - AR → NameEntry  (canonical AR + all AR variants)
  - EN → NameEntry  (canonical EN + all EN variants, case-insensitive)
  - Normalized AR → NameEntry  (hamza / alef / ya normalization)
  - Correction surface → canonical AR
  - Corpus-share ranked list for ranking queries
"""

from __future__ import annotations

import re
import threading
from typing import Dict, List, Optional, Tuple

from ._data import get_entries, get_corrections
from ._types import NameEntry

_lock = threading.Lock()
_built = False

# ── Lookup Tables ──
_ar_index: Dict[str, NameEntry] = {}           # exact AR form → entry
_en_index: Dict[str, NameEntry] = {}           # lower-case EN form → entry
_ar_norm_index: Dict[str, NameEntry] = {}      # normalized AR → entry
_correction_index: Dict[str, str] = {}          # surface → canonical AR
_ranked: List[NameEntry] = []                    # sorted by corpus_share desc
_all_entries: List[NameEntry] = []               # full list

# ── Arabic Normalization ──

# Characters that should map to bare alef
_ALEF_VARIANTS = re.compile(r"[\u0622\u0623\u0625\u0671]")  # آ أ إ ٱ
# Tashkeel / diacritics to strip
_TASHKEEL = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]")
# Tatweel (kashida)
_TATWEEL = re.compile(r"\u0640")
# Alef maqsura ↔ ya
_ALEF_MAQSURA = "\u0649"  # ى
_YA = "\u064A"  # ي
# Ta marbuta → ha
_TA_MARBUTA = "\u0629"  # ة
_HA = "\u0647"  # ه


def normalize_ar(text: str) -> str:
    """Normalize Arabic text for fuzzy matching.

    Strips diacritics, normalizes hamza/alef variants, alef maqsura → ya,
    ta marbuta → ha, and removes tatweel.
    """
    s = _TASHKEEL.sub("", text)
    s = _TATWEEL.sub("", s)
    s = _ALEF_VARIANTS.sub("\u0627", s)  # → ا
    s = s.replace(_ALEF_MAQSURA, _YA)
    s = s.replace(_TA_MARBUTA, _HA)
    return s


def normalize_en(text: str) -> str:
    """Normalize English text for fuzzy matching (lowercase, strip hyphens)."""
    return text.lower().replace("-", "").replace("'", "").strip()


def _claim_en(key: str, entry: NameEntry) -> None:
    """Bind an English key to the lemma with the larger corpus share."""
    existing = _en_index.get(key)
    if existing is None or entry.corpus_share > existing.corpus_share:
        _en_index[key] = entry


def _claim_ar_variant(
    index: Dict[str, NameEntry], canonical_keys: set, key: str, entry: NameEntry
) -> None:
    """Bind an Arabic variant spelling to the lemma with the larger
    corpus share, same rule as English keys.

    A canonical key (some entry's own ``ar``/normalized ``ar``) always
    wins over any OTHER entry's variant claiming the same string — a
    rare misspelling must never shadow a real lemma's own canonical
    spelling. Among two variants with no canonical claim, the higher
    corpus share wins, exactly like ``_claim_en``.
    """
    if key in canonical_keys:
        # Already bound to its own entry in the canonical pass; a
        # variant from a different lemma must never override it.
        return
    existing = index.get(key)
    if existing is None or entry.corpus_share > existing.corpus_share:
        index[key] = entry


def _build() -> None:
    """Build all lookup indices (called once, thread-safe)."""
    global _built, _ranked, _all_entries

    entries = get_entries()
    corrections = get_corrections()

    # ── AR index, pass 1: canonical spellings are unconditional and
    # take priority over any other lemma's variant claiming the same
    # string (book has zero duplicate canonical ar values). ──
    canonical_ar_keys = {entry.ar for entry in entries}
    canonical_ar_norm_keys = {normalize_ar(entry.ar) for entry in entries}
    for entry in entries:
        _ar_index[entry.ar] = entry
        _ar_norm_index[normalize_ar(entry.ar)] = entry

    for entry in entries:
        # ── AR index, pass 2: variants. Keep the higher-share lemma
        # when two rows' variants claim the same spelling — same rule
        # as English keys, so a rare misspelling cannot steal a common
        # name's lookup the way it could before this was checked. ──
        for v in entry.ar_variants:
            v_stripped = v.strip()
            if v_stripped:
                _claim_ar_variant(_ar_index, canonical_ar_keys, v_stripped, entry)
                _claim_ar_variant(
                    _ar_norm_index,
                    canonical_ar_norm_keys,
                    normalize_ar(v_stripped),
                    entry,
                )

        # ── EN index: canonical + variants (case-insensitive) ──
        # Keep the higher-share lemma when two rows claim the same English key.
        _claim_en(normalize_en(entry.en), entry)
        for v in entry.en_variants:
            v_stripped = v.strip()
            if v_stripped:
                _claim_en(normalize_en(v_stripped), entry)

    # ── Correction index ──
    _correction_index.update(corrections)

    # ── Ranked list ──
    _all_entries = list(entries)
    _ranked = sorted(entries, key=lambda e: e.corpus_share, reverse=True)
    _built = True


def _ensure_built() -> None:
    """Ensure indices are built."""
    if _built:
        return
    with _lock:
        if _built:
            return
        _build()


# ── Public query functions ──

def lookup_ar(name: str) -> Optional[NameEntry]:
    """Look up an Arabic name (exact match, normalized, phonetic alif maqsura, and compounds)."""
    _ensure_built()
    if not name or not name.strip():
        return None
    trimmed = name.strip()

    # 1. Exact match
    entry = _ar_index.get(trimmed)
    if entry:
        return entry

    # 2. Normalized match
    norm = normalize_ar(trimmed)
    entry = _ar_norm_index.get(norm)
    if entry:
        return entry

    # 3. Alif / Alif Maqsura terminal phonetic equivalence (e.g. مصطفا <-> مصطفى, موسا <-> موسى)
    if norm.endswith("\u0627"):
        alt = norm[:-1] + "\u064A"
        alt_entry = _ar_norm_index.get(alt)
        if alt_entry:
            return alt_entry
    elif norm.endswith("\u064A"):
        alt = norm[:-1] + "\u0627"
        alt_entry = _ar_norm_index.get(alt)
        if alt_entry:
            return alt_entry

    # 4. Compound space-less match (e.g. عبد الرحيم <-> عبدالرحيم)
    no_space = trimmed.replace(" ", "")
    if no_space != trimmed:
        entry = _ar_index.get(no_space) or _ar_norm_index.get(normalize_ar(no_space))
        if entry:
            return entry

    return None


def lookup_en(name: str) -> Optional[NameEntry]:
    """Look up an English name (case-insensitive)."""
    _ensure_built()
    return _en_index.get(normalize_en(name))


def lookup(name: str) -> Optional[NameEntry]:
    """Look up a name in either Arabic or English."""
    _ensure_built()
    # Detect script: if any Arabic character, treat as Arabic
    if any("\u0600" <= c <= "\u06FF" or "\uFE70" <= c <= "\uFEFF" for c in name):
        return lookup_ar(name)
    return lookup_en(name)


def correct(surface: str) -> Optional[str]:
    """Look up a correction for a surface form."""
    _ensure_built()
    return _correction_index.get(surface)


def get_ranked() -> List[NameEntry]:
    """Return all entries sorted by descending corpus share."""
    _ensure_built()
    return _ranked


def get_all() -> List[NameEntry]:
    """Return all entries (unordered)."""
    _ensure_built()
    return _all_entries


def get_ar_forms() -> Dict[str, NameEntry]:
    """Return the full AR lookup index (for split/segmentation)."""
    _ensure_built()
    return _ar_index


def get_en_forms() -> Dict[str, NameEntry]:
    """Return the full EN lookup index."""
    _ensure_built()
    return _en_index


def get_ar_norm_forms() -> Dict[str, NameEntry]:
    """Return the normalized AR lookup index."""
    _ensure_built()
    return _ar_norm_index


def is_arabic(text: str) -> bool:
    """Check if text contains Arabic characters."""
    return any("\u0600" <= c <= "\u06FF" or "\uFE70" <= c <= "\uFEFF" for c in text)


# ── Age-Aware Generation Engine ───────────────────────────────────────────────
#
# The corpus is Egyptian high school graduation records (2017 & 2023).
# Each full name in the corpus is:
#   slot1 = the student's own first name     (born ~1998-2006)
#   slot2 = the father's first name          (born ~1966-1980)
#   slot3 = the grandfather's first name     (born ~1934-1954)
#   slot4 = the great-grandfather's name     (born ~1902-1930)
#   slot5 = family surname                   (timeless)
#   slot6 = clan/tribal name                 (timeless)
#
# Corpus anchor year: 2020 (midpoint of 2017/2023 cohorts).
# Average generation gap in Egypt: ~30 years.
# σ (standard deviation) of Gaussian window: 12 years.

_CORPUS_ANCHOR_YEAR   = 2020  # Midpoint of 2017 & 2023 high school cohorts
_STUDENT_GRAD_AGE     = 18    # Standard Thanaweya Amma graduation age in Egypt
_CORPUS_STUDENT_BIRTH = _CORPUS_ANCHOR_YEAR - _STUDENT_GRAD_AGE  # 2002

_GENERATION_GAP       = 30    # Average generation gap in Egyptian families (years)
_GAUSSIAN_SIGMA       = 12    # Standard deviation for generational age window (years)

# Centre birth-years for each generational slot:
# Slot 1: Student (birth ~2002)
# Slot 2: Father (birth ~1972)
# Slot 3: Grandfather (birth ~1942)
# Slot 4: Great-grandfather (birth ~1912)
# Slots 5 & 6: Family & Clan (timeless)
_SLOT_BIRTH_CENTERS = [
    _CORPUS_STUDENT_BIRTH - i * _GENERATION_GAP
    for i in range(4)
] + [None, None]


_GEN_LABELS = {
    0: "youth",
    1: "parent",
    2: "grandparent",
    3: "great-grandparent",
}


def _gaussian(x: float, center: float, sigma: float) -> float:
    """Standard Gaussian (normal) kernel, unnormalized."""
    import math
    return math.exp(-0.5 * ((x - center) / sigma) ** 2)


def score_for_age(entry: "NameEntry", birth_year: int) -> float:
    """Compute an age-relevance score for a NameEntry given a target birth year.

    Score ∈ [0.0, 1.0].  Returns 0.0 for entries with no slot data.

    Algorithm
    ---------
    For each slot i with a known generational centre:
        weight_i = Gaussian(birth_year, centre_i, σ)
    For timeless slots (5, 6):
        weight = 0.05  (small constant — family names exist at all ages)
    Final score = Σ(slot_pct[i] * weight_i) / 100
    """
    p = list(entry.slot_pcts)
    while len(p) < 6:
        p.append(0.0)
    p = p[:6]
    if sum(p) == 0:
        return 0.0

    total = 0.0
    for i, centre in enumerate(_SLOT_BIRTH_CENTERS):
        if centre is None:
            # Timeless slot — small constant relevance
            total += p[i] * 0.05
        else:
            total += p[i] * _gaussian(birth_year, centre, _GAUSSIAN_SIGMA)

    # Normalize by max possible (all weight in the best-matching slot)
    max_w = max(
        _gaussian(birth_year, c, _GAUSSIAN_SIGMA)
        for c in _SLOT_BIRTH_CENTERS[:4]
        if c is not None
    )
    normalizer = max_w * 100 if max_w > 0 else 100
    return min(total / normalizer, 1.0)


def names_for_age(
    age: int,
    *,
    gender: Optional[str] = None,
    as_of_year: Optional[int] = None,
    top: int = 20,
    include_family: bool = False,
) -> List["NameEntry"]:
    """Return names most likely to belong to a person of the given age.

    Parameters
    ----------
    age : int
        Age in years.
    gender : str, optional
        Filter by gender: ``'m'``, ``'male'``, ``'f'``, ``'female'``,
        ``'n'``, ``'neutral'``.  ``None`` means no filter.
    as_of_year : int, optional
        The reference year (defaults to current year).
    top : int
        Maximum number of results to return.
    include_family : bool
        If True, also include family surnames (role=FAMILY) in results.
        Defaults to False (given names only).

    Returns
    -------
    list[NameEntry]
        Entries sorted by age-relevance score descending.
    """
    import datetime
    from ._types import Gender as G, NameRole as NR

    _ensure_built()

    year = as_of_year or datetime.date.today().year
    birth_year = year - max(0, age)

    # Gender normalisation
    gender_filter: Optional[G] = G.parse(gender)

    results: List[Tuple[float, "NameEntry"]] = []
    import math
    for entry in _all_entries:
        # Role filter
        if not include_family and entry.role not in (NR.GIVEN, NR.KUNYA):
            continue

        # Gender filter: NEUTRAL matches everyone
        if gender_filter is not None:
            if entry.gender not in (gender_filter, G.NEUTRAL):
                continue

        score = score_for_age(entry, birth_year)
        if score <= 0.0:
            continue

        # Frequency boost: log-scale occurrence count
        occ = sum(entry.slot_pcts)   # proxy when .occ not stored
        freq_boost = 1.0 + math.log1p(entry.corpus_share * 1000)
        final = score * freq_boost
        results.append((final, entry))

    results.sort(key=lambda x: -x[0])
    return [e for _, e in results[:top]]


def age_profile(entry: "NameEntry", as_of_year: Optional[int] = None) -> "AgeProfile":
    """Build a full generational age profile for a name entry.

    Parameters
    ----------
    entry : NameEntry
        The name to profile.
    as_of_year : int, optional
        Reference year (defaults to current year).

    Returns
    -------
    AgeProfile
        Contains peak_age_range, generation_label, dominant_slot, and
        age_scores (dict of age → normalized relevance score).
    """
    import datetime
    from ._types import AgeProfile, NameRole as NR

    year = as_of_year or datetime.date.today().year

    p = list(entry.slot_pcts)
    while len(p) < 6:
        p.append(0.0)
    p = p[:6]

    # Build age_scores every 5 years from 0 to 100
    age_scores: dict = {}
    for age in range(0, 101, 5):
        birth_year = year - age
        age_scores[age] = round(score_for_age(entry, birth_year), 3)

    # Find peak age range: ages where score >= 50% of max
    max_score = max(age_scores.values()) if age_scores else 0
    threshold = max_score * 0.5
    in_peak = [a for a, s in age_scores.items() if s >= threshold]
    peak_range = (min(in_peak), max(in_peak)) if in_peak else (0, 100)

    # Determine dominant slot by weighted slot score
    slot_scores = []
    for i, centre in enumerate(_SLOT_BIRTH_CENTERS):
        if centre is None:
            slot_scores.append(p[i] * 0.05)
        else:
            # Use the birth year of the peak age midpoint
            peak_birth = year - (peak_range[0] + peak_range[1]) // 2
            slot_scores.append(p[i] * _gaussian(peak_birth, centre, _GAUSSIAN_SIGMA))

    # Timeless check: family/clan names
    if entry.role in (NR.FAMILY, NR.TRIBAL):
        dominant_slot = 5
        gen_label = "timeless"
    elif sum(slot_scores) == 0:
        dominant_slot = 1
        gen_label = "unknown"
    else:
        dominant_slot = slot_scores.index(max(slot_scores)) + 1  # 1-based
        gen_label = _GEN_LABELS.get(dominant_slot - 1, "timeless")

    return AgeProfile(
        peak_age_range=peak_range,
        generation_label=gen_label,
        dominant_slot=dominant_slot,
        age_scores=age_scores,
    )


def detect_age_for_entry(
    entry: "NameEntry",
    as_of_year: Optional[int] = None,
) -> "AgeDetection":
    """Estimate the likely age of a person who has this name (single-name API).

    Delegates to :func:`detect_age_from_chain` with a single token.
    """
    return detect_age_from_chain([(entry, 0)], as_of_year=as_of_year)


def detect_age_from_chain(
    token_entries: List[Tuple["NameEntry", int]],
    as_of_year: Optional[int] = None,
) -> "AgeDetection":
    """Estimate the likely age of a person from a multi-token name chain.

    Each token in an Egyptian name chain belongs to a specific generation:

    - **slot 0** – person's own name → age = detected age directly
    - **slot 1** – father's name     → person's age = father_age − 30
    - **slot 2** – grandfather       → person's age = grandfather_age − 60
    - **slot 3** – great-grandfather → person's age = gg_age − 90

    The final estimate is a **weighted average** across all resolved tokens.
    Closer-generation tokens carry more weight (slot 0 = 1.0, slot 1 = 0.6,
    slot 2 = 0.3, slot 3 = 0.15).  If multiple tokens agree on the same age,
    confidence is boosted; if they disagree widely, confidence is penalised.

    Parameters
    ----------
    token_entries : list of (NameEntry, slot_index)
        Each tuple is a resolved name token and its 0-based slot position.
        slot_index 0 = person, 1 = father, 2 = grandfather, etc.
    as_of_year : int, optional
        Reference year (defaults to current year).

    Returns
    -------
    AgeDetection
    """
    import datetime, math, statistics
    from ._types import AgeDetection, NameRole as NR

    year = as_of_year or datetime.date.today().year

    # Slot weights — closer generation = higher weight
    SLOT_WEIGHTS  = {0: 1.0, 1: 0.6, 2: 0.3, 3: 0.15}
    GENERATION_GAP = _GENERATION_GAP  # 30 years

    def _peak_age_for_entry(e: "NameEntry") -> Tuple[int, float]:
        """Return (peak_age, sharpness) for a single entry."""
        scores = {}
        for age in range(0, 101):
            scores[age] = score_for_age(e, year - age)
        if not scores or max(scores.values()) == 0:
            return (35, 0.0)
        peak = max(scores, key=lambda a: scores[a])
        peak_s = scores[peak]
        mean_s = sum(scores.values()) / len(scores)
        sharpness = (peak_s - mean_s) / (peak_s + 1e-9)
        return (peak, max(0.0, min(1.0, sharpness)))

    # ── Per-token estimates ────────────────────────────────────────────────────
    token_estimates: List[Tuple[int, float, float]] = []   # (implied_age, sharpness, weight)

    for entry, slot_idx in token_entries:
        # Skip family / tribal names — they carry no generational age signal
        if entry.role in (NR.FAMILY, NR.TRIBAL):
            continue
        peak_age, sharpness = _peak_age_for_entry(entry)
        # Convert this token's peak age into an implied age for the *person*
        implied_person_age = peak_age - slot_idx * GENERATION_GAP
        # Clamp to valid range
        implied_person_age = max(0, min(100, implied_person_age))
        weight = SLOT_WEIGHTS.get(slot_idx, 0.1)
        token_estimates.append((implied_person_age, sharpness, weight))

    if not token_estimates:
        # Only family names — no generational signal at all
        return AgeDetection(
            estimated_age=35,
            age_range=(0, 100),
            confidence=0.0,
            generation_label="timeless",
            note="Only family/clan names were given — no age signal available.",
        )

    # ── Weighted average of implied ages ──────────────────────────────────────
    total_weight      = sum(w for _, _, w in token_estimates)
    weighted_age_sum  = sum(age * w for age, _, w in token_estimates)
    estimated_age     = round(weighted_age_sum / total_weight)

    # ── Confidence: base from slot0 sharpness ─────────────────────────────────
    slot0_sharpness = next((sh for age, sh, w in token_estimates[:1]), 0.0)
    base_confidence = slot0_sharpness

    # Agreement bonus: if multiple tokens give close implied ages, boost confidence
    if len(token_estimates) >= 2:
        implied_ages = [age for age, _, _ in token_estimates]
        try:
            spread = statistics.stdev(implied_ages)
        except statistics.StatisticsError:
            spread = 0.0
        # spread of 0 → +0.2 bonus; spread of 30+ → no bonus
        agreement_bonus = max(0.0, 0.2 * (1.0 - spread / 30.0))
        confidence = min(1.0, base_confidence + agreement_bonus)
    else:
        confidence = base_confidence

    confidence = round(confidence, 3)

    # ── Age range: ±σ * 12 around estimate ───────────────────────────────────
    #   (mirrors the corpus Gaussian window used for scoring)
    sigma = _GAUSSIAN_SIGMA
    age_range = (max(0, estimated_age - sigma), min(100, estimated_age + sigma))

    # ── Generation label ──────────────────────────────────────────────────────
    # Use slot0 entry (person's own name) if available
    slot0_entries = [e for e, si in token_entries if si == 0 and e.role not in (NR.FAMILY, NR.TRIBAL)]
    if slot0_entries:
        est_birth = year - estimated_age
        closest   = min(
            range(4),
            key=lambda i: abs(est_birth - (_CORPUS_STUDENT_BIRTH - i * _GENERATION_GAP))
        )
        gen_label = _GEN_LABELS.get(closest, "timeless")
    else:
        gen_label = "unknown"

    # ── Human-readable note ───────────────────────────────────────────────────
    n_tokens = len(token_estimates)
    token_word = "name" if n_tokens == 1 else f"{n_tokens}-token chain"
    range_str = f"{age_range[0]}–{age_range[1]} years old"
    conf_str = (
        "high confidence"     if confidence >= 0.6
        else "moderate confidence" if confidence >= 0.3
        else "low confidence (common across generations)"
    )
    note = (
        f"Based on {token_word}: estimated age ~{estimated_age} "
        f"({range_str}), {gen_label} generation, {conf_str}."
    )

    return AgeDetection(
        estimated_age=estimated_age,
        age_range=age_range,
        confidence=confidence,
        generation_label=gen_label,
        note=note,
    )


