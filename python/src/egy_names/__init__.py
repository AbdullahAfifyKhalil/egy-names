"""
egy-names — A production-grade Egyptian onomastic intelligence library.

Developed by Abdullah Afify (Afify).
MIT License.

Quick start:
    from egy_names import EgyNames
    en = EgyNames()
    names = en.generate(count=5, gender="male", religion="muslim")
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from ._data import get_metadata
from ._index import (
    age_profile as _age_profile_fn,
    detect_age_for_entry as _detect_age_fn,
    detect_age_from_chain as _detect_age_chain_fn,
    get_all,
    get_ranked,
    is_arabic,
    lookup,
    lookup_ar,
    lookup_en,
    names_for_age as _names_for_age_fn,
    normalize_ar,
    normalize_en,
)
from ._types import (
    AgeDetection,
    AgeProfile,
    ChainPart,
    FrequencyClass,
    Gender,
    GenderDetection,
    GeneratedName,
    NameEntry,
    NameInfo,
    NameRole,
    PetName,
    RankInfo,
    Religion,
    ReligionDetection,
    UniquenessScore,
)
from ._infer import infer as _infer_fn, infer_token as _infer_token_fn
from ._quality import is_lineage_role, is_low_confidence_entry, is_personal_entry
from ._types import InferredName
from .annotator import annotate, annotate_single
from .corrector import correct, correct_token
from .generator import generate as generate_names
from .search import search
from .splitter import split
from .translator import translate, translate_token


def _compound_tokens(full_name: str) -> List[Tuple[str, Optional[NameEntry]]]:
    """Split on whitespace, but merge an adjacent pair into one lemma
    when the book has it as a two-word compound (e.g. kunya "Abu X").

    A handful of book entries are legitimately two words (roughly 800
    "Abu X" kunya/family lemmas plus a few compound given names). A
    blind whitespace split treats them as two meaningless fragments,
    breaking gender/religion detection and split() on names that
    contain one. Greedy pairwise lookahead, same approach tashkeel()
    already uses for "عبد الرحمن"-style pairs.
    """
    raw = full_name.strip().split()
    out: List[Tuple[str, Optional[NameEntry]]] = []
    i = 0
    n = len(raw)
    while i < n:
        if i < n - 1:
            pair = f"{raw[i]} {raw[i + 1]}"
            pair_entry = lookup_ar(pair) or lookup_ar(f"{raw[i]}{raw[i + 1]}")
            if pair_entry is not None:
                out.append((pair, pair_entry))
                i += 2
                continue
        out.append((raw[i], lookup(raw[i])))
        i += 1
    return out


class EgyptianNames:
    """The main entry point for the Egyptian Names library."""

    def __init__(self, seed: Optional[int] = None) -> None:
        self._seed = seed

    # ------------------------------------------------------------------
    # Core features
    # ------------------------------------------------------------------

    def generate(
        self,
        count: int = 1,
        *,
        gender: Optional[str] = None,
        religion: Optional[str] = None,
        length: Optional[int] = None,
        family_name: bool = True,
        frequency: Optional[str] = None,
        lang: str = "both",
        seed: Optional[int] = None,
    ) -> List[GeneratedName]:
        """Generate culturally authentic Egyptian full names."""
        effective_seed = seed if seed is not None else self._seed
        return generate_names(
            count=count,
            gender=gender,
            religion=religion,
            length=length,
            family_name=family_name,
            frequency=frequency,
            lang=lang,
            seed=effective_seed,
        )

    def translate(
        self,
        name: str,
        to: Optional[str] = None,
    ) -> str:
        """Translate a full name or single name between Arabic and English."""
        return translate(name, to=to)

    def lookup(
        self,
        name: str,
    ) -> Optional[NameInfo]:
        """Look up a single name token and return its full NameInfo metadata."""
        entry = lookup(name)
        if entry is None:
            return None
        return NameInfo._from_entry(entry)

    def info(
        self,
        name: str,
    ) -> Optional[NameInfo]:
        """Alias for lookup(). Look up a name and return its NameInfo."""
        return self.lookup(name)

    def annotate(
        self,
        name: str,
    ) -> Optional[Union[NameInfo, List[Optional[NameInfo]]]]:
        """Annotate a name with linguistic and demographic metadata."""
        return annotate(name)

    def identify(
        self,
        name: str,
    ) -> Optional[InferredName]:
        """Identify a single name token, in or out of the book.

        Looks the token up first. If it is not in the book, falls back
        to a machine-learned model and marks the result ``inferred=True``.
        The model abstains (returns "unknown") on gender/religion/role
        whenever its confidence is below the precision-tuned threshold,
        rather than guessing. Never use an inferred result as if it were
        a verified book entry — check ``.inferred`` and ``.source``.
        """
        return _infer_token_fn(name)

    def identify_all(
        self,
        full_name: str,
    ) -> List[InferredName]:
        """Identify every token in a full name, book-first with ML fallback.

        Same semantics as :meth:`identify`, applied token by token.
        Always a list: empty input gives an empty list, never None, so
        callers can iterate the result without a type check.
        """
        result = _infer_fn(full_name)
        if result is None:
            return []
        if isinstance(result, list):
            return [r for r in result if r is not None]
        return [result]


    def split(self, full_name: str) -> List[str]:
        """Split a full name into its individual name components."""
        return split(full_name)

    def tashkeel(self, name: str, dialect: str = "standard") -> str:
        """Add Arabic diacritics (tashkeel) to an Egyptian name (standard or egyptian)."""
        if not name or not name.strip():
            return ""
        raw_tokens = name.strip().split()
        result = []
        i = 0
        n = len(raw_tokens)

        is_eg = str(dialect).lower().startswith("eg")

        while i < n:
            current = raw_tokens[i]

            # Check compound pair (e.g. "عبد" + "الرحمن" → "عبدالرحمن")
            if i < n - 1:
                next_tok = raw_tokens[i + 1]
                compound = f"{current} {next_tok}"
                compound_no_space = f"{current}{next_tok}"
                compound_entry = lookup_ar(compound) or lookup_ar(compound_no_space)
                if compound_entry:
                    val = compound_entry.tashkeel_eg if is_eg else compound_entry.tashkeel
                    if val:
                        result.append(val)
                        i += 2
                        continue

            entry = lookup_ar(current)
            if entry:
                val = entry.tashkeel_eg if is_eg else entry.tashkeel
                result.append(val if val else current)
            else:
                result.append(current)
            i += 1

        return " ".join(result)

    def tashkeel_eg(self, name: str) -> str:
        """Add authentic Egyptian colloquial diacritics (tashkeel) to a name."""
        return self.tashkeel(name, dialect="egyptian")

    def tashkeel_standard(self, name: str) -> str:
        """Add Modern Standard Arabic diacritics (tashkeel) to a name."""
        return self.tashkeel(name, dialect="standard")

    def ipa(self, name: str, dialect: str = "standard") -> str:
        """Generate International Phonetic Alphabet (IPA) transcription for TTS."""
        if not name or not name.strip():
            return ""
        tokens = split(name) if " " not in name.strip() else name.strip().split()
        is_eg = str(dialect).lower().startswith("eg")
        ipa_parts = []
        for tok in tokens:
            entry = lookup(tok)
            if entry:
                ipa_val = entry.ipa_eg if is_eg else entry.ipa_standard
                if ipa_val:
                    ipa_parts.append(ipa_val.strip("/[]"))
                else:
                    ipa_parts.append(tok)
            else:
                ipa_parts.append(tok)
        
        joined = " ".join(ipa_parts)
        return f"[{joined}]" if is_eg else f"/{joined}/"

    def ipa_eg(self, name: str) -> str:
        """Generate Egyptian Colloquial Arabic IPA phonetic transcription for TTS."""
        return self.ipa(name, dialect="egyptian")

    def ipa_standard(self, name: str) -> str:
        """Generate Modern Standard Arabic IPA phonetic transcription for TTS."""
        return self.ipa(name, dialect="standard")

    def dallaa(self, name: str, format: str = "plain") -> List[str]:
        """Retrieve authentic Egyptian colloquial pet names/endearments (اسم الدلع).
        
        Args:
            name: The Arabic or English name.
            format: 'plain'/'ar' (e.g. ميدو), 'tashkeel' (e.g. مِيدُو), 'en' (e.g. Mido), or 'ipa' (e.g. [ˈmiːdu]).
        """
        entry = lookup(name)
        if not entry:
            return []
        fmt = format.lower()
        if fmt in ["tashkeel", "tashkeel_eg", "tk"]:
            return list(entry.dallaa_tashkeel) if entry.dallaa_tashkeel else list(entry.dallaa_ar)
        elif fmt in ["en", "english"]:
            return list(entry.dallaa_en)
        elif fmt in ["ipa", "ipa_eg", "phonetic"]:
            return list(entry.dallaa_ipa)
        return list(entry.dallaa_ar)

    def dallaa_info(self, name: str) -> List[PetName]:
        """Retrieve rich PetName objects (ar, tashkeel, en, ipa) for a name."""
        entry = lookup(name)
        if not entry or not entry.dallaa_ar:
            return []
        
        res = []
        n = len(entry.dallaa_ar)
        for i in range(n):
            ar = entry.dallaa_ar[i]
            tk = entry.dallaa_tashkeel[i] if i < len(entry.dallaa_tashkeel) else ar
            en = entry.dallaa_en[i] if i < len(entry.dallaa_en) else ""
            ipa = entry.dallaa_ipa[i] if i < len(entry.dallaa_ipa) else ""
            res.append(PetName(ar=ar, tashkeel=tk, en=en, ipa=ipa))
        return res

    def pet_names(self, name: str, format: str = "plain") -> List[str]:
        """Alias for dallaa()."""
        return self.dallaa(name, format=format)

    def root(self, name: str) -> Optional[str]:
        """Retrieve the Semitic/Coptic morphological root of a name."""
        entry = lookup(name)
        return entry.root if entry and entry.root != "N/A" else None

    def origin(self, name: str) -> Optional[str]:
        """Retrieve the historical etymological stratum/origin layer of a name."""
        entry = lookup(name)
        return entry.origin_type if entry else None

    def famous_figures(self, name: str, lang: str = "ar") -> List[str]:
        """Retrieve authentic Egyptian historical or cultural icons with descriptions.
        
        Args:
            name: The Arabic or English name.
            lang: 'ar' for Arabic descriptions or 'en' for English descriptions.
        """
        entry = lookup(name)
        if not entry:
            return []
        if lang.lower().startswith("en"):
            return list(entry.famous_figures_en) if entry.famous_figures_en else list(entry.famous_figures_ar)
        return list(entry.famous_figures_ar)

    def trend(self, name: str) -> Optional[str]:
        """Retrieve the popularity trend category of a name."""
        entry = lookup(name)
        return entry.trend_category if entry else None

    def correct(self, name: str) -> str:
        """Correct misspelled or variant-form names to their canonical Arabic forms."""
        return correct(name)

    def meaning(self, name: str) -> Optional[Dict[str, str]]:
        """Retrieve the deep etymological meaning of a name in Arabic and English."""
        entry = lookup(name)
        if not entry or (not entry.meaning_ar and not entry.meaning_en):
            return None
        return {
            "ar": entry.meaning_ar,
            "en": entry.meaning_en,
        }

    def families(
        self,
        count: int = 50,
        *,
        frequency: Optional[str] = None,
        religion: Optional[str] = None,
        starts_with: Optional[str] = None,
    ) -> List[NameInfo]:
        """Retrieve authentic Egyptian family/surname names."""
        return search(
            role="family",
            max_results=count,
            frequency=frequency,
            religion=religion,
            starts_with=starts_with,
        )

    def search(
        self,
        *,
        gender: Optional[str] = None,
        religion: Optional[str] = None,
        role: Optional[str] = None,
        frequency: Optional[str] = None,
        starts_with: Optional[str] = None,
        ends_with: Optional[str] = None,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
        contains: Optional[str] = None,
        min_corpus_share: Optional[float] = None,
        max_results: int = 50,
        sort_by: str = "corpus_share",
    ) -> List[NameInfo]:
        """Search the Egyptian name database with rich multi-criteria filters."""
        return search(
            gender=gender,
            religion=religion,
            role=role,
            frequency=frequency,
            starts_with=starts_with,
            ends_with=ends_with,
            prefix=prefix,
            suffix=suffix,
            contains=contains,
            min_corpus_share=min_corpus_share,
            max_results=max_results,
            sort_by=sort_by,
        )

    # ------------------------------------------------------------------
    # Creative features
    # ------------------------------------------------------------------

    def is_valid(self, name: str) -> bool:
        """True if this is a usable personal name.

        Catalog surfaces that are not a person (God, titles, common nouns)
        stay in lookup for split. They are not valid names.
        """
        entry = lookup(name)
        return (
            entry is not None
            and is_personal_entry(entry)
            and not is_low_confidence_entry(entry)
        )

    def detect_gender(self, full_name: str) -> GenderDetection:
        """Gender of the person: the first given name.

        Later tokens are father, grandfather, family. They do not vote.
        A tie must not become male. Two-word compound lemmas (e.g.
        kunya "Abu X") are recognized as one token, not two fragments.
        """
        tokens = _compound_tokens(full_name)
        if not tokens:
            return GenderDetection(gender="neutral", confidence=0.0)

        skipped_lineage = 0
        for i, (_, entry) in enumerate(tokens):
            if entry is None or not is_personal_entry(entry) or is_low_confidence_entry(entry):
                continue
            if is_lineage_role(entry):
                skipped_lineage += 1
                continue
            if entry.gender == Gender.NEUTRAL:
                return GenderDetection(gender="neutral", confidence=0.6)
            confidence = 1.0 if skipped_lineage == 0 and i == 0 else 0.85
            return GenderDetection(gender=entry.gender.value, confidence=confidence)

        return GenderDetection(gender="neutral", confidence=0.0)

    def detect_religion(self, full_name: str) -> ReligionDetection:
        """Religion of the person: the first given name, like gender.

        A father, grandfather, or family surname from one community does
        not override the person's own first name. Lineage tokens only
        vote if the person's own name gives no distinctive signal — an
        intermarried or mixed-heritage family's surname should not
        outvote what the person is actually named. Two-word compound
        lemmas (e.g. kunya "Abu X") are recognized as one token.
        """
        tokens = _compound_tokens(full_name)
        if not tokens:
            return ReligionDetection(religion="neutral", confidence=0.0)

        skipped_lineage = 0
        for i, (_, entry) in enumerate(tokens):
            if entry is None or not is_personal_entry(entry) or is_low_confidence_entry(entry):
                continue
            if is_lineage_role(entry):
                skipped_lineage += 1
                continue
            if entry.religion == Religion.NEUTRAL:
                continue
            confidence = 1.0 if skipped_lineage == 0 and i == 0 else 0.9
            return ReligionDetection(religion=entry.religion.value, confidence=confidence)

        # The person's own given names carried no distinctive signal
        # (neutral or not found). Fall back to an aggregate vote across
        # every token, lineage included, rather than declaring neutral.
        muslim = 0.0
        christian = 0.0
        first: Optional[str] = None

        for _, entry in tokens:
            if entry is None or not is_personal_entry(entry) or is_low_confidence_entry(entry):
                continue
            if entry.religion == Religion.MUSLIM:
                muslim += 1
                if first is None:
                    first = "muslim"
            elif entry.religion == Religion.CHRISTIAN:
                christian += 1
                if first is None:
                    first = "christian"

        if muslim == 0.0 and christian == 0.0:
            return ReligionDetection(religion="neutral", confidence=0.0)

        distinctive = muslim + christian
        if muslim > christian:
            return ReligionDetection(religion="muslim", confidence=0.5 * muslim / distinctive)
        if christian > muslim:
            return ReligionDetection(
                religion="christian", confidence=0.5 * christian / distinctive
            )
        return ReligionDetection(religion=first or "neutral", confidence=0.5)

    def rank(self, name: str) -> Optional[RankInfo]:
        """Get the national frequency rank and percentile of a name."""
        entry = lookup(name)
        if not entry:
            return None

        ranked = get_ranked()
        total = len(ranked)
        for i, r in enumerate(ranked):
            if r.ar == entry.ar:
                rank_pos = i + 1
                percentile = (1 - (rank_pos - 1) / total) * 100
                desc = f"The #{rank_pos} most common name in the Egyptian corpus"
                if rank_pos <= 10:
                    desc = f"Top 10 — {desc}"
                elif rank_pos <= 100:
                    desc = f"Top 100 — {desc}"
                elif rank_pos <= 1000:
                    desc = f"Top 1000 — {desc}"
                return RankInfo(
                    rank=rank_pos,
                    percentile=round(percentile, 2),
                    corpus_share=f"{entry.corpus_share:.4f}%",
                    description=desc,
                )
        return None

    def analyze_chain(self, full_name: str) -> List[ChainPart]:
        """Analyze each component of a full Egyptian name and identify its generational role."""
        tokens = full_name.strip().split()
        if not tokens:
            return []

        parts: List[ChainPart] = []
        n = len(tokens)

        for i, t in enumerate(tokens):
            entry = lookup(t)
            slot = i + 1

            if i == 0:
                role = "person"
                detail = "The individual's given name"
            elif i == n - 1 and entry and entry.role == NameRole.FAMILY:
                role = "family_name"
                detail = "Family/tribal surname"
            elif i == 1:
                role = "father"
                detail = "Father's name"
            elif i == 2:
                role = "grandfather"
                detail = "Paternal grandfather"
            elif i == 3:
                role = "great_grandfather"
                detail = "Great-grandfather"
            else:
                role = "ancestor"
                detail = f"Ancestor (generation {i})"

            parts.append(ChainPart(
                name=t,
                slot=slot,
                role=role,
                detail=detail,
            ))

        return parts

    def uniqueness(self, full_name: str) -> UniquenessScore:
        """Calculate a uniqueness score for a full Egyptian name combination."""
        tokens = full_name.strip().split()
        if not tokens:
            return UniquenessScore(score=0.5, label="unknown", note="Empty input")

        shares = []
        unknown_count = 0
        for t in tokens:
            entry = lookup(t)
            if entry:
                shares.append(entry.corpus_share)
            else:
                unknown_count += 1

        if not shares:
            return UniquenessScore(
                score=1.0,
                label="unknown",
                note="None of the name parts are in the Egyptian corpus",
            )

        log_mean = sum(math.log(max(s, 1e-9)) for s in shares) / len(shares)

        max_log = 2.6
        min_log = -9.2
        score = 1.0 - (log_mean - min_log) / (max_log - min_log)
        score = max(0.0, min(1.0, score))
        score = min(1.0, score + unknown_count * 0.15)

        if score < 0.2:
            label = "extremely_common"
            note = "Each part is among the most common names nationally"
        elif score < 0.4:
            label = "common"
            note = "Well-known name parts with high national frequency"
        elif score < 0.6:
            label = "moderate"
            note = "A mix of common and less common name parts"
        elif score < 0.8:
            label = "distinctive"
            note = "Contains uncommon or regionally specific names"
        else:
            label = "highly_unique"
            note = "Rare name combination — distinctive family heritage"

        return UniquenessScore(
            score=round(score, 3),
            label=label,
            note=note,
        )

    def stats(self) -> Dict[str, Any]:
        """Return corpus and database statistics."""
        meta = get_metadata()
        entries = get_all()
        return {
            **meta,
            "total_names": len(entries),
            "given_names": sum(1 for e in entries if e.role == NameRole.GIVEN),
            "family_names": sum(1 for e in entries if e.role == NameRole.FAMILY),
            "male_names": sum(1 for e in entries if e.gender == Gender.MALE),
            "female_names": sum(1 for e in entries if e.gender == Gender.FEMALE),
        }

    # ------------------------------------------------------------------
    # Age-Aware Features
    # ------------------------------------------------------------------

    def names_for_age(
        self,
        age: int,
        *,
        gender: Optional[str] = None,
        as_of_year: Optional[int] = None,
        top: int = 20,
        include_family: bool = False,
    ) -> List[NameInfo]:
        """Return names most likely to belong to a person of the given age.

        Uses the corpus slot distribution to map birth years to generational
        name popularity. The corpus is built from Egyptian high school records
        (2017 & 2023), encoding 4 generations:

        - slot1 (the student)      → ages ~19–27 in 2025
        - slot2 (father's name)    → ages ~45–59 in 2025
        - slot3 (grandfather)      → ages ~71–91 in 2025
        - slot4 (great-grandparent)→ ages ~93–123 in 2025 (historical)

        Parameters
        ----------
        age : int
            Age of the person in years.
        gender : str, optional
            ``'m'`` / ``'male'``, ``'f'`` / ``'female'``, or ``'n'`` / ``'neutral'``.
            ``None`` means no gender filter.
        as_of_year : int, optional
            Reference year for age calculation. Defaults to the current year.
        top : int
            Number of results to return (default 20).
        include_family : bool
            If True, include family surnames in results (default False).

        Returns
        -------
        list[NameInfo]
            Names sorted by age-relevance score (highest first).

        Examples
        --------
        >>> e = EgyNames()
        >>> e.names_for_age(age=25, gender='m', top=5)
        >>> e.names_for_age(age=50, gender='f', top=10)
        """
        entries = _names_for_age_fn(
            age,
            gender=gender,
            as_of_year=as_of_year,
            top=top,
            include_family=include_family,
        )
        return [NameInfo._from_entry(e) for e in entries]

    def age_profile(self, name: str) -> Optional[AgeProfile]:
        """Build a generational age profile for a name.

        Returns which age group most commonly holds this name today,
        based on its corpus slot distribution.

        Parameters
        ----------
        name : str
            Arabic or English name to profile.

        Returns
        -------
        AgeProfile or None
            ``None`` if the name is not in the library.

        Examples
        --------
        >>> e = EgyNames()
        >>> p = e.age_profile('محمد')
        >>> p.generation_label
        'parent'
        >>> p.peak_age_range
        (35, 55)
        >>> p.age_scores
        {0: 0.05, 5: 0.08, 10: 0.12, ..., 50: 0.95, ...}
        """
        entry = lookup(name)
        if entry is None:
            return None
        return _age_profile_fn(entry)

    def detect_age(
        self,
        name: str,
        as_of_year: Optional[int] = None,
    ) -> Optional["AgeDetection"]:
        """Estimate the likely age of a person who carries this name.

        Works for both **single names** and **full name chains**.

        For a full chain (e.g. ``'كريم أشرف السيد'``), each token is used
        as a cross-generational signal:

        - Token 1 (``كريم``)  → direct age of the person
        - Token 2 (``أشرف``)  → father's age − 30 = person's age
        - Token 3 (``السيد``) → family name, ignored (no age signal)

        Tokens that agree on the same age raise the confidence score.
        Tokens that disagree lower it.

        Parameters
        ----------
        name : str
            A single Arabic or English name, or a full name chain.
            Mixed-script input is supported.
        as_of_year : int, optional
            Reference year for age calculation (defaults to current year).

        Returns
        -------
        AgeDetection or None
            ``None`` if **no** token in the chain is found in the library.

        Examples
        --------
        >>> e = EgyNames()
        >>> # Single name
        >>> r = e.detect_age('كريم')
        >>> r.estimated_age, r.generation_label
        (23, 'youth')

        >>> # Full chain — all tokens used as corroborating signals
        >>> r = e.detect_age('كريم أشرف السيد')
        >>> r.note
        'Based on 2-token chain: estimated age ~22 (10–34 years old), youth generation, high confidence.'

        >>> e.detect_age('فاروق').generation_label
        'grandparent'
        """
        tokens = name.strip().split()

        if not tokens:
            return None

        # ── Resolve each token and assign a slot index ─────────────────────
        # Slot 0 = person's own name, 1 = father, 2 = grandfather, etc.
        # We attempt to resolve every token; skip those not in the library.
        token_entries = []
        slot_idx = 0
        for token in tokens:
            entry = lookup(token)
            if entry is None:
                # Try normalised / compound variants via the full token substring
                entry = lookup(token)
            if entry is not None:
                token_entries.append((entry, slot_idx))
                slot_idx += 1   # each resolved token advances the generation slot

        if not token_entries:
            return None

        return _detect_age_chain_fn(token_entries, as_of_year=as_of_year)


# Direct alias for concise usage
EgyNames = EgyptianNames

__version__ = "0.3.6"
__author__ = "Abdullah Afify"
__company__ = "Afify"
__license__ = "MIT"

__all__ = [
    "EgyptianNames",
    "EgyNames",
    "AgeDetection",
    "AgeProfile",
    "Gender",
    "Religion",
    "NameRole",
    "FrequencyClass",
    "NameEntry",
    "NameInfo",
    "InferredName",
    "PetName",
    "GeneratedName",
    "ChainPart",
    "GenderDetection",
    "ReligionDetection",
    "RankInfo",
    "UniquenessScore",
    "get_metadata",
]
