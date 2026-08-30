"""Faker provider that forwards to egy-names.generate().

No sampling, filtering, or transliteration lives here. Slot strings are
indexes into the chain the engine already returned.
"""

from __future__ import annotations

from typing import Optional, Tuple, Union

from egy_names import EgyNames, GeneratedName
from faker import Faker
from faker.providers import BaseProvider

_engine = EgyNames()

Localized = Union[str, Tuple[str, str]]


def egyptian_faker(*args, **kwargs) -> Faker:
    """Return a Faker instance with this provider already registered."""
    fake = Faker(*args, **kwargs)
    fake.add_provider(Provider)
    return fake


def _localized(ar: str, en: str, lang: str) -> Localized:
    key = (lang or "en").lower()
    if key == "ar":
        return ar
    if key == "both":
        return (ar, en)
    return en


def _roles(
    name: GeneratedName,
    family_name: bool,
) -> Tuple[Tuple[str, str], Tuple[str, str], Tuple[str, str], Tuple[str, str]]:
    """Map generate() parts onto person / father / grandfather / family."""
    parts_ar = list(name.parts_ar)
    parts_en = list(name.parts_en)
    family = ("", "")
    if family_name and len(parts_ar) > 1:
        family = (parts_ar[-1], parts_en[-1])
        parts_ar = parts_ar[:-1]
        parts_en = parts_en[:-1]

    def slot(index: int) -> Tuple[str, str]:
        if index < len(parts_ar):
            return (parts_ar[index], parts_en[index])
        return ("", "")

    return slot(0), slot(1), slot(2), family


class Provider(BaseProvider):
    """Egyptian patronymic names via egy-names 0.3.6."""

    def egyptian_name(
        self,
        gender: Optional[str] = None,
        religion: Optional[str] = None,
        length: Optional[int] = None,
        family_name: bool = True,
        frequency: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> GeneratedName:
        """Return one grounded chain from the engine."""
        return self._generate(
            gender=gender,
            religion=religion,
            length=length,
            family_name=family_name,
            frequency=frequency,
            seed=seed,
        )

    def egyptian_full_name(
        self,
        lang: str = "en",
        *,
        gender: Optional[str] = None,
        religion: Optional[str] = None,
        length: Optional[int] = None,
        family_name: bool = True,
        frequency: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> Localized:
        """Full patronymic name as a string (or `(ar, en)` when `lang='both'`)."""
        name = self._generate(
            gender=gender,
            religion=religion,
            length=length,
            family_name=family_name,
            frequency=frequency,
            seed=seed,
        )
        return _localized(name.ar, name.en, lang)

    def egyptian_person(
        self,
        lang: str = "en",
        *,
        gender: Optional[str] = None,
        religion: Optional[str] = None,
        length: Optional[int] = None,
        family_name: bool = True,
        frequency: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> Localized:
        """Slot 1 — the person's given name."""
        return self._slot(
            0,
            lang,
            gender=gender,
            religion=religion,
            length=length,
            family_name=family_name,
            frequency=frequency,
            seed=seed,
        )

    def egyptian_father(
        self,
        lang: str = "en",
        *,
        gender: Optional[str] = None,
        religion: Optional[str] = None,
        length: Optional[int] = None,
        family_name: bool = True,
        frequency: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> Localized:
        """Slot 2 — father. Empty if the generated chain has no father slot."""
        return self._slot(
            1,
            lang,
            gender=gender,
            religion=religion,
            length=length,
            family_name=family_name,
            frequency=frequency,
            seed=seed,
        )

    def egyptian_grandfather(
        self,
        lang: str = "en",
        *,
        gender: Optional[str] = None,
        religion: Optional[str] = None,
        length: Optional[int] = None,
        family_name: bool = True,
        frequency: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> Localized:
        """Slot 3 — grandfather. Empty if the generated chain is too short."""
        return self._slot(
            2,
            lang,
            gender=gender,
            religion=religion,
            length=length,
            family_name=family_name,
            frequency=frequency,
            seed=seed,
        )

    def egyptian_family(
        self,
        lang: str = "en",
        *,
        gender: Optional[str] = None,
        religion: Optional[str] = None,
        length: Optional[int] = None,
        family_name: bool = True,
        frequency: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> Localized:
        """Final clan / toponymic surname. Empty when `family_name=False`."""
        name = self._generate(
            gender=gender,
            religion=religion,
            length=length,
            family_name=family_name,
            frequency=frequency,
            seed=seed,
        )
        _person, _father, _grandfather, family = _roles(name, family_name)
        return _localized(family[0], family[1], lang)

    def _slot(
        self,
        index: int,
        lang: str,
        *,
        gender: Optional[str],
        religion: Optional[str],
        length: Optional[int],
        family_name: bool,
        frequency: Optional[str],
        seed: Optional[int],
    ) -> Localized:
        name = self._generate(
            gender=gender,
            religion=religion,
            length=length,
            family_name=family_name,
            frequency=frequency,
            seed=seed,
        )
        roles = _roles(name, family_name)
        ar, en = roles[index]
        return _localized(ar, en, lang)

    def _generate(
        self,
        *,
        gender: Optional[str] = None,
        religion: Optional[str] = None,
        length: Optional[int] = None,
        family_name: bool = True,
        frequency: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> GeneratedName:
        if seed is None:
            seed = self.generator.random.getrandbits(32)
        return _engine.generate(
            count=1,
            gender=gender,
            religion=religion,
            length=length,
            family_name=family_name,
            frequency=frequency,
            seed=seed,
        )[0]


EgyptianNamesProvider = Provider
