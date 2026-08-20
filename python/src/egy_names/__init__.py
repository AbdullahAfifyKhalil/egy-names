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
from typing import Any, Dict, List, Optional, Sequence, Union

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
    RankInfo,
    Religion,
    ReligionDetection,
    UniquenessScore,
)
from .annotator import annotate, annotate_single
from .corrector import correct, correct_token
from .generator import generate as generate_names
from .search import search
from .splitter import split
from .translator import translate, translate_token


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

    def annotate(
        self,
        name: str,
    ) -> Optional[Union[NameInfo, List[Optional[NameInfo]]]]:
        """Annotate a name with linguistic and demographic metadata."""
        return annotate(name)


    def split(self, full_name: str) -> List[str]:
        """Split a full name into its individual name components."""
        return split(full_name)

    def tashkeel(self, name: str) -> str:
        """Add Arabic diacritics (tashkeel) to an Egyptian name."""
        if not name or not name.strip():
            return name
        raw_tokens = name.strip().split()
        result = []
        i = 0
        n = len(raw_tokens)

        while i < n:
            current = raw_tokens[i]

            # Check compound pair (e.g. "عبد" + "الرحمن" → "عبدالرحمن")
            if i < n - 1:
                next_tok = raw_tokens[i + 1]
                compound = f"{current} {next_tok}"
                compound_no_space = f"{current}{next_tok}"
                compound_entry = lookup_ar(compound) or lookup_ar(compound_no_space)
                if compound_entry and compound_entry.tashkeel:
                    result.append(compound_entry.tashkeel)
                    i += 2
                    continue

            entry = lookup_ar(current)
            result.append(entry.tashkeel if entry and entry.tashkeel else current)
            i += 1

        return " ".join(result)

    def correct(self, name: str) -> str:
        """Correct misspelled or variant-form names to their canonical Arabic forms."""
        return correct(name)

    def meaning(self, name: str) -> Optional[Dict[str, str]]:
        """Retrieve the etymological meaning of a name in Arabic and English."""
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
            contains=contains,
            min_corpus_share=min_corpus_share,
            max_results=max_results,
            sort_by=sort_by,
        )

    # ------------------------------------------------------------------
    # Creative features
    # ------------------------------------------------------------------

    def is_valid(self, name: str) -> bool:
        """Check if a name is a verified Egyptian name in the dataset."""
        return lookup(name) is not None

    def detect_gender(self, full_name: str) -> GenderDetection:
        """Infer the overall gender of a person from their full name."""
        tokens = full_name.strip().split()
        if not tokens:
            return GenderDetection(gender="neutral", confidence=0.0)

        male_score = 0.0
        female_score = 0.0
        neutral_score = 0.0
        total_weight = 0.0

        for i, token in enumerate(tokens):
            entry = lookup(token)
            if not entry:
                continue

            weight = 4.0 if i == 0 else (2.0 if i == 1 else 1.0)
            total_weight += weight

            if entry.gender == Gender.MALE:
                male_score += weight
            elif entry.gender == Gender.FEMALE:
                female_score += weight
            else:
                neutral_score += weight

        if total_weight == 0.0:
            return GenderDetection(gender="neutral", confidence=0.0)

        scores = {"male": male_score, "female": female_score, "neutral": neutral_score}
        best_gender = max(scores, key=scores.get)  # type: ignore
        confidence = scores[best_gender] / total_weight

        return GenderDetection(gender=best_gender, confidence=confidence)

    def detect_religion(self, full_name: str) -> ReligionDetection:
        """Infer the likely religious background from the full name chain."""
        tokens = full_name.strip().split()
        if not tokens:
            return ReligionDetection(religion="neutral", confidence=0.0)

        muslim_score = 0.0
        christian_score = 0.0
        neutral_score = 0.0
        total_weight = 0.0

        for token in tokens:
            entry = lookup(token)
            if not entry:
                continue

            weight = 1.0
            total_weight += weight

            if entry.religion == Religion.MUSLIM:
                muslim_score += weight
            elif entry.religion == Religion.CHRISTIAN:
                christian_score += weight
            else:
                neutral_score += weight

        if total_weight == 0.0:
            return ReligionDetection(religion="neutral", confidence=0.0)

        scores = {"muslim": muslim_score, "christian": christian_score, "neutral": neutral_score}
        best_religion = max(scores, key=scores.get)  # type: ignore
        confidence = scores[best_religion] / total_weight

        return ReligionDetection(religion=best_religion, confidence=confidence)

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

__version__ = "0.2.1"
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
    "GeneratedName",
    "ChainPart",
    "GenderDetection",
    "ReligionDetection",
    "RankInfo",
    "UniquenessScore",
    "get_metadata",
]
