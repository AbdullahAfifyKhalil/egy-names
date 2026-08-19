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
    get_all,
    get_ranked,
    is_arabic,
    lookup,
    lookup_ar,
    lookup_en,
    normalize_ar,
    normalize_en,
)
from ._types import (
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


# Direct alias for concise usage
EgyNames = EgyptianNames

__version__ = "0.1.1"
__author__ = "Abdullah Afify"
__company__ = "Afify"
__license__ = "MIT"

__all__ = [
    "EgyptianNames",
    "EgyNames",
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
