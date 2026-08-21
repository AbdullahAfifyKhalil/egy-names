"""Multi-criteria name search and filtering engine."""

from __future__ import annotations

from typing import List, Optional

from ._index import get_all, is_arabic, normalize_ar, normalize_en
from ._types import (
    FrequencyClass,
    Gender,
    NameEntry,
    NameInfo,
    NameRole,
    Religion,
)


def search(
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
    """Search names by multiple criteria.

    Args:
        gender: "male", "female", "neutral", or None for any.
        religion: "muslim", "christian", "neutral", or None for any.
        role: "given", "family", or None for any.
        frequency: "common", "normal", "rare", or None for any.
        starts_with: Name prefix (Arabic or English).
        ends_with: Name suffix (Arabic or English).
        prefix: Alias for starts_with.
        suffix: Alias for ends_with.
        contains: Substring to match.
        min_corpus_share: Minimum corpus share percentage.
        max_results: Maximum number of results (default 50).
        sort_by: "corpus_share" (default, desc), "alphabetical", or "rank".

    Returns:
        List of NameInfo matching all criteria.
    """
    effective_starts = prefix if prefix is not None else starts_with
    effective_ends = suffix if suffix is not None else ends_with
    entries = get_all()

    # ── Apply filters ──
    g = Gender.parse(gender)
    r = Religion.parse(religion)
    rl = NameRole.parse(role)
    f = FrequencyClass.parse(frequency)

    # Detect if prefix/suffix/contains is Arabic or English
    prefix_ar = effective_starts and is_arabic(effective_starts)
    suffix_ar = effective_ends and is_arabic(effective_ends)
    contains_ar = contains and is_arabic(contains)

    filtered: List[NameEntry] = []

    for e in entries:
        if g is not None and e.gender != g and e.gender != Gender.NEUTRAL:
            continue
        if r is not None and e.religion != r and e.religion != Religion.NEUTRAL:
            continue
        if rl is not None and e.role != rl:
            continue
        if f is not None and e.frequency != f:
            continue
        if min_corpus_share is not None and e.corpus_share < min_corpus_share:
            continue

        # Prefix match
        if effective_starts:
            if prefix_ar:
                if not normalize_ar(e.ar).startswith(normalize_ar(effective_starts)):
                    continue
            else:
                if not normalize_en(e.en).startswith(normalize_en(effective_starts)):
                    continue

        # Suffix match
        if effective_ends:
            if suffix_ar:
                if not normalize_ar(e.ar).endswith(normalize_ar(effective_ends)):
                    continue
            else:
                if not normalize_en(e.en).endswith(normalize_en(effective_ends)):
                    continue

        # Contains match
        if contains:
            if contains_ar:
                if normalize_ar(contains) not in normalize_ar(e.ar):
                    continue
            else:
                if normalize_en(contains) not in normalize_en(e.en):
                    continue

        filtered.append(e)

    # ── Sort ──
    if sort_by == "alphabetical":
        filtered.sort(key=lambda x: x.ar)
    elif sort_by == "rank":
        filtered.sort(key=lambda x: x.corpus_share, reverse=True)
    else:
        filtered.sort(key=lambda x: x.corpus_share, reverse=True)

    # ── Limit & convert ──
    return [NameInfo._from_entry(e) for e in filtered[:max_results]]
