"""Type definitions for the egyptian-names library."""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union


class Gender(enum.Enum):
    """Biological / cultural gender classification."""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"

    @classmethod
    def _from_code(cls, c: str) -> Gender:
        return {"m": cls.MALE, "f": cls.FEMALE, "n": cls.NEUTRAL}.get(c, cls.NEUTRAL)

    @classmethod
    def parse(cls, val: Optional[Union[str, Gender]]) -> Optional[Gender]:
        if val is None or isinstance(val, cls):
            return val
        s = str(val).strip().lower()
        mapping = {
            "m": cls.MALE, "male": cls.MALE, "ذكر": cls.MALE,
            "f": cls.FEMALE, "female": cls.FEMALE, "أنثى": cls.FEMALE, "انثى": cls.FEMALE,
            "n": cls.NEUTRAL, "neutral": cls.NEUTRAL, "مشترك": cls.NEUTRAL, "محايد": cls.NEUTRAL,
        }
        return mapping.get(s)


class Religion(enum.Enum):
    """Religious community classification."""
    MUSLIM = "muslim"
    CHRISTIAN = "christian"
    NEUTRAL = "neutral"

    @classmethod
    def _from_code(cls, c: str) -> Religion:
        return {"m": cls.MUSLIM, "c": cls.CHRISTIAN, "n": cls.NEUTRAL}.get(c, cls.NEUTRAL)

    @classmethod
    def parse(cls, val: Optional[Union[str, Religion]]) -> Optional[Religion]:
        if val is None or isinstance(val, cls):
            return val
        s = str(val).strip().lower()
        mapping = {
            "m": cls.MUSLIM, "muslim": cls.MUSLIM, "islam": cls.MUSLIM, "مسلم": cls.MUSLIM,
            "c": cls.CHRISTIAN, "christian": cls.CHRISTIAN, "coptic": cls.CHRISTIAN, "مسيحي": cls.CHRISTIAN, "قبطي": cls.CHRISTIAN,
            "n": cls.NEUTRAL, "neutral": cls.NEUTRAL, "مشترك": cls.NEUTRAL, "محايد": cls.NEUTRAL,
        }
        return mapping.get(s)


class NameRole(enum.Enum):
    """Whether a name is primarily a given / first name or a family / surname."""
    GIVEN  = "given"
    FAMILY = "family"
    KUNYA  = "kunya"   # patronymic kunya (أبو X)
    TRIBAL = "tribal"  # tribal/clan name

    @classmethod
    def _from_code(cls, c: str) -> NameRole:
        return {"g": cls.GIVEN, "f": cls.FAMILY, "k": cls.KUNYA, "t": cls.TRIBAL}.get(c, cls.GIVEN)

    @classmethod
    def parse(cls, val: Optional[Union[str, NameRole]]) -> Optional[NameRole]:
        if val is None or isinstance(val, cls):
            return val
        s = str(val).strip().lower()
        mapping = {
            "g": cls.GIVEN, "given": cls.GIVEN, "first": cls.GIVEN, "علم": cls.GIVEN, "اسم": cls.GIVEN,
            "f": cls.FAMILY, "family": cls.FAMILY, "surname": cls.FAMILY, "last": cls.FAMILY, "عائلة": cls.FAMILY, "لقب": cls.FAMILY,
            "k": cls.KUNYA, "kunya": cls.KUNYA, "patronymic": cls.KUNYA, "كنية": cls.KUNYA,
            "t": cls.TRIBAL, "tribal": cls.TRIBAL, "clan": cls.TRIBAL, "قبلي": cls.TRIBAL, "قبيلة": cls.TRIBAL,
        }
        return mapping.get(s)


class FrequencyClass(enum.Enum):
    """Corpus frequency tier."""
    COMMON = "common"     # ≥ 500 occurrences
    NORMAL = "normal"     # 10–499 occurrences
    RARE = "rare"         # < 10 occurrences

    @classmethod
    def _from_code(cls, c: str) -> FrequencyClass:
        return {"c": cls.COMMON, "n": cls.NORMAL, "r": cls.RARE}.get(c, cls.NORMAL)

    @classmethod
    def parse(cls, val: Optional[Union[str, FrequencyClass]]) -> Optional[FrequencyClass]:
        if val is None or isinstance(val, cls):
            return val
        s = str(val).strip().lower()
        mapping = {
            "c": cls.COMMON, "common": cls.COMMON, "شائع": cls.COMMON,
            "n": cls.NORMAL, "normal": cls.NORMAL, "متوسط": cls.NORMAL, "عادي": cls.NORMAL,
            "r": cls.RARE, "rare": cls.RARE, "نادر": cls.RARE,
        }
        return mapping.get(s)



@dataclass(frozen=True, slots=True)
class NameEntry:
    """Internal representation of a single name lemma from the data bundle."""
    ar: str
    en: str
    gender: Gender
    religion: Religion
    role: NameRole
    ar_variants: List[str]
    en_variants: List[str]
    slot_pcts: List[float]       # 8 floats: [slot1%, ..., slot8+%]
    corpus_share: float          # total_count_percentage
    frequency: FrequencyClass
    tashkeel: str
    meaning_ar: str
    meaning_en: str

    @classmethod
    def _from_raw(cls, raw: dict) -> NameEntry:
        return cls(
            ar=raw["a"],
            en=raw["e"],
            gender=Gender._from_code(raw["g"]),
            religion=Religion._from_code(raw["r"]),
            role=NameRole._from_code(raw["l"]),
            ar_variants=raw["av"].split("|") if raw["av"] else [raw["a"]],
            en_variants=raw["ev"].split("|") if raw["ev"] else [raw["e"]],
            slot_pcts=raw["p"],
            corpus_share=raw["tp"],
            frequency=FrequencyClass._from_code(raw["fc"]),
            tashkeel=raw["t"],
            meaning_ar=raw["ma"],
            meaning_en=raw["me"],
        )


@dataclass(frozen=True)
class NameInfo:
    """Public-facing metadata for a single name, returned by annotate() etc."""
    ar: str
    en: str
    gender: str
    religion: str
    role: str
    frequency_class: str
    corpus_share: float
    tashkeel: str
    meaning_ar: Optional[str]
    meaning_en: Optional[str]
    ar_variants: List[str]
    en_variants: List[str]
    slot_distribution: List[float]

    @classmethod
    def _from_entry(cls, e: NameEntry) -> NameInfo:
        return cls(
            ar=e.ar,
            en=e.en,
            gender=e.gender.value,
            religion=e.religion.value,
            role=e.role.value,
            frequency_class=e.frequency.value,
            corpus_share=e.corpus_share,
            tashkeel=e.tashkeel,
            meaning_ar=e.meaning_ar or None,
            meaning_en=e.meaning_en or None,
            ar_variants=list(e.ar_variants),
            en_variants=list(e.en_variants),
            slot_distribution=list(e.slot_pcts),
        )

    def to_dict(self) -> dict:
        """Serialize to a plain dictionary."""
        return {
            "ar": self.ar,
            "en": self.en,
            "gender": self.gender,
            "religion": self.religion,
            "role": self.role,
            "frequency_class": self.frequency_class,
            "corpus_share": self.corpus_share,
            "tashkeel": self.tashkeel,
            "meaning_ar": self.meaning_ar,
            "meaning_en": self.meaning_en,
            "ar_variants": self.ar_variants,
            "en_variants": self.en_variants,
            "slot_distribution": self.slot_distribution,
        }


@dataclass(frozen=True)
class GeneratedName:
    """A generated full Egyptian name in both Arabic and English."""
    ar: str
    en: str
    parts_ar: List[str]
    parts_en: List[str]

    def to_dict(self) -> dict:
        return {
            "ar": self.ar,
            "en": self.en,
            "parts_ar": self.parts_ar,
            "parts_en": self.parts_en,
        }


@dataclass(frozen=True)
class ChainPart:
    """A single part of an analyzed patronymic chain."""
    name: str
    slot: int
    role: str
    detail: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "slot": self.slot,
            "role": self.role,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class GenderDetection:
    """Result of gender detection on a full name."""
    gender: str
    confidence: float

    def to_dict(self) -> dict:
        return {"gender": self.gender, "confidence": round(self.confidence, 3)}


@dataclass(frozen=True)
class ReligionDetection:
    """Result of religion detection on a full name."""
    religion: str
    confidence: float

    def to_dict(self) -> dict:
        return {"religion": self.religion, "confidence": round(self.confidence, 3)}


@dataclass(frozen=True)
class RankInfo:
    """Popularity ranking information for a name."""
    rank: int
    percentile: float
    corpus_share: str
    description: str

    def to_dict(self) -> dict:
        return {
            "rank": self.rank,
            "percentile": round(self.percentile, 2),
            "corpus_share": self.corpus_share,
            "description": self.description,
        }


@dataclass(frozen=True)
class UniquenessScore:
    """How unique a full name chain is."""
    score: float
    label: str
    note: str

    def to_dict(self) -> dict:
        return {
            "score": round(self.score, 3),
            "label": self.label,
            "note": self.note,
        }


@dataclass(frozen=True)
class AgeProfile:
    """Generational age profile for a single name.

    Describes which age group most commonly holds this name today,
    derived from the slot distribution in the corpus.

    Attributes
    ----------
    peak_age_range : tuple[int, int]
        The (min, max) ages most likely to carry this name in the current year.
    generation_label : str
        Human-readable generation label: 'youth', 'parent', 'grandparent',
        'great-grandparent', or 'timeless' (for family/clan names).
    dominant_slot : int
        The slot index (1-based) that has the highest weighted probability.
    age_scores : dict[int, float]
        Normalized relevance score (0.0–1.0) keyed by age (every 5 years from
        0 to 100). Useful for plotting an age-relevance curve.
    """
    peak_age_range: tuple
    generation_label: str
    dominant_slot: int
    age_scores: dict

    def to_dict(self) -> dict:
        return {
            "peak_age_range": list(self.peak_age_range),
            "generation_label": self.generation_label,
            "dominant_slot": self.dominant_slot,
            "age_scores": self.age_scores,
        }


@dataclass(frozen=True)
class AgeDetection:
    """Estimated age of a person based on their name's generational profile.

    Returned by :meth:`EgyNames.detect_age`.

    Attributes
    ----------
    estimated_age : int
        Single best-guess age (midpoint of the peak age range).
    age_range : tuple[int, int]
        Plausible (min, max) age range where the name is most common.
    confidence : float
        Confidence in the estimate, 0.0–1.0.  Higher when the name has a
        narrow generational peak; lower for timeless names like محمد.
    generation_label : str
        Human-readable generation: ``'youth'``, ``'parent'``,
        ``'grandparent'``, ``'great-grandparent'``, or ``'timeless'``.
    note : str
        Plain-language explanation of the estimate.
    """
    estimated_age: int
    age_range: tuple
    confidence: float
    generation_label: str
    note: str

    def to_dict(self) -> dict:
        return {
            "estimated_age": self.estimated_age,
            "age_range": list(self.age_range),
            "confidence": round(self.confidence, 3),
            "generation_label": self.generation_label,
            "note": self.note,
        }
