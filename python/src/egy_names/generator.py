"""Slot-weighted probabilistic Egyptian name generation engine.

Generates culturally authentic full Egyptian names by sampling from
corpus-grounded positional probability distributions.  Every generated
name mirrors real Egyptian naming patterns derived from 2.46 million
student records.
"""

from __future__ import annotations

import random
from typing import List, Optional, Sequence

from ._index import get_all
from ._types import (
    FrequencyClass,
    Gender,
    GeneratedName,
    NameEntry,
    NameRole,
    Religion,
)

# Slot labels for the patronymic chain
_SLOT_ROLES = [
    "first",
    "father",
    "grandfather",
    "great-grandfather",
    "great-great-grandfather",
    "ancestor",
    "ancestor",
    "ancestor",
]

# Default chain-length range matching Egyptian naming convention
_DEFAULT_MIN_LEN = 4
_DEFAULT_MAX_LEN = 5


def _filter_entries(
    entries: Sequence[NameEntry],
    *,
    gender: Optional[Gender] = None,
    religion: Optional[Religion] = None,
    role: Optional[NameRole] = None,
    frequency: Optional[FrequencyClass] = None,
) -> List[NameEntry]:
    """Filter entries by optional criteria."""
    result = list(entries)
    if gender is not None:
        result = [
            e for e in result
            if e.gender == gender or e.gender == Gender.NEUTRAL
        ]
    if religion is not None:
        result = [
            e for e in result
            if e.religion == religion or e.religion == Religion.NEUTRAL
        ]
    if role is not None:
        result = [e for e in result if e.role == role]
    if frequency is not None:
        result = [e for e in result if e.frequency == frequency]
    return result


def _weighted_pick(
    entries: List[NameEntry],
    slot_idx: int,
    rng: random.Random,
) -> NameEntry:
    """Pick a name entry using slot-positional weight × corpus share.

    slot_idx is 0-based (0 = first name, 7 = eighth-or-later).
    Weight = slot_pcts[slot_idx] × corpus_share.  Entries with zero
    weight for the given slot are excluded.
    """
    candidates: List[NameEntry] = []
    weights: List[float] = []

    for e in entries:
        slot_val = e.slot_pcts[slot_idx] if slot_idx < len(e.slot_pcts) else (e.slot_pcts[-1] if e.slot_pcts else 0.0)
        w = slot_val * e.corpus_share
        if w > 0:
            candidates.append(e)
            weights.append(w)

    if not candidates:
        # Fallback: use corpus share alone
        candidates = entries
        weights = [max(e.corpus_share, 1e-9) for e in entries]

    return rng.choices(candidates, weights=weights, k=1)[0]


def generate(
    *,
    count: int = 1,
    gender: Optional[str] = None,
    religion: Optional[str] = None,
    length: Optional[int] = None,
    family_name: bool = True,
    frequency: Optional[str] = None,
    lang: str = "both",
    seed: Optional[int] = None,
) -> List[GeneratedName]:
    """Generate realistic Egyptian full names.

    Args:
        count: Number of names to generate.
        gender: "male", "female", or None for any.
        religion: "muslim", "christian", or None for any.
        length: Number of parts (default: random 4–5).
        family_name: If True, the last part is a family/surname.
        frequency: "common", "normal", "rare", or None for any.
        lang: "ar", "en", or "both".
        seed: Random seed for reproducibility.

    Returns:
        List of GeneratedName objects.
    """
    rng = random.Random(seed)
    all_entries = get_all()

    # Parse filter enums
    g = Gender.parse(gender)
    r = Religion.parse(religion)
    f = FrequencyClass.parse(frequency)


    # Patronymic slots: given names only (middle names are always male in
    # Egyptian patronymic tradition, regardless of the person's gender)
    patron_gender = Gender.MALE

    # Filter pools
    first_pool = _filter_entries(
        all_entries, gender=g, religion=r, role=NameRole.GIVEN, frequency=f,
    )
    patron_pool = _filter_entries(
        all_entries, gender=patron_gender, religion=r, role=NameRole.GIVEN, frequency=f,
    )
    family_pool = _filter_entries(
        all_entries, religion=r, role=NameRole.FAMILY, frequency=f,
    )

    if not first_pool:
        first_pool = _filter_entries(all_entries, gender=g, role=NameRole.GIVEN)
    if not patron_pool:
        patron_pool = _filter_entries(all_entries, gender=patron_gender, role=NameRole.GIVEN)
    if not family_pool:
        family_pool = _filter_entries(all_entries, role=NameRole.FAMILY)

    results: List[GeneratedName] = []

    for _ in range(count):
        chain_len = length if length else rng.randint(_DEFAULT_MIN_LEN, _DEFAULT_MAX_LEN)

        parts_ar: List[str] = []
        parts_en: List[str] = []
        seen: set = set()  # avoid immediate duplicates in a chain

        # Slot 1: the person's given name
        entry = _weighted_pick(first_pool, 0, rng)
        attempts = 0
        while entry.ar in seen and attempts < 20:
            entry = _weighted_pick(first_pool, 0, rng)
            attempts += 1
        parts_ar.append(entry.ar)
        parts_en.append(entry.en)
        seen.add(entry.ar)

        # Slots 2 .. (N-1 or N): patronymic chain
        patron_end = chain_len - 1 if family_name else chain_len
        for slot in range(1, patron_end):
            slot_idx = min(slot, 7)  # cap at slot 8 (index 7)
            entry = _weighted_pick(patron_pool, slot_idx, rng)
            attempts = 0
            while entry.ar in seen and attempts < 20:
                entry = _weighted_pick(patron_pool, slot_idx, rng)
                attempts += 1
            parts_ar.append(entry.ar)
            parts_en.append(entry.en)
            seen.add(entry.ar)

        # Last slot: family name (if requested)
        if family_name and chain_len > 1:
            slot_idx = min(chain_len - 1, 7)
            entry = _weighted_pick(family_pool, slot_idx, rng)
            attempts = 0
            while entry.ar in seen and attempts < 20:
                entry = _weighted_pick(family_pool, slot_idx, rng)
                attempts += 1
            parts_ar.append(entry.ar)
            parts_en.append(entry.en)

        results.append(GeneratedName(
            ar=" ".join(parts_ar),
            en=" ".join(parts_en),
            parts_ar=parts_ar,
            parts_en=parts_en,
        ))

    return results
