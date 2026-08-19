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


def _build() -> None:
    """Build all lookup indices (called once, thread-safe)."""
    global _built, _ranked, _all_entries

    entries = get_entries()
    corrections = get_corrections()

    for entry in entries:
        # ── AR index: canonical + variants ──
        _ar_index[entry.ar] = entry
        _ar_norm_index[normalize_ar(entry.ar)] = entry
        for v in entry.ar_variants:
            v_stripped = v.strip()
            if v_stripped:
                _ar_index.setdefault(v_stripped, entry)
                _ar_norm_index.setdefault(normalize_ar(v_stripped), entry)

        # ── EN index: canonical + variants (case-insensitive) ──
        _en_index[normalize_en(entry.en)] = entry
        for v in entry.en_variants:
            v_stripped = v.strip()
            if v_stripped:
                _en_index.setdefault(normalize_en(v_stripped), entry)

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
