"""Type definitions for the egyptian-names library."""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import List, Optional


class Gender(enum.Enum):
    """Biological / cultural gender classification."""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"

    @classmethod
    def _from_code(cls, c: str) -> Gender:
        return {"m": cls.MALE, "f": cls.FEMALE, "n": cls.NEUTRAL}[c]


class Religion(enum.Enum):
    """Religious community classification."""
    MUSLIM = "muslim"
    CHRISTIAN = "christian"
    NEUTRAL = "neutral"

    @classmethod
    def _from_code(cls, c: str) -> Religion:
        return {"m": cls.MUSLIM, "c": cls.CHRISTIAN, "n": cls.NEUTRAL}[c]


class NameRole(enum.Enum):
    """Whether a name is primarily a given / first name or a family / surname."""
    GIVEN = "given"
    FAMILY = "family"

    @classmethod
    def _from_code(cls, c: str) -> NameRole:
        return {"g": cls.GIVEN, "f": cls.FAMILY}[c]


class FrequencyClass(enum.Enum):
    """Corpus frequency tier."""
    COMMON = "common"     # ≥ 500 occurrences
    NORMAL = "normal"     # 10–499 occurrences
    RARE = "rare"         # < 10 occurrences

    @classmethod
    def _from_code(cls, c: str) -> FrequencyClass:
        return {"c": cls.COMMON, "n": cls.NORMAL, "r": cls.RARE}[c]


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
