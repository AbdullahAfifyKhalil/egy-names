"""Tests for the Faker companion — wrap egy-names, do not resample."""

from __future__ import annotations

import re

from egy_names import GeneratedName
from faker import Faker
from faker_egy_names import Provider, egyptian_faker
from faker_egy_names import provider as provider_mod

_ARABIC = re.compile(r"[\u0600-\u06FF]")


def test_egyptian_faker_registers_methods():
    fake = egyptian_faker()
    assert callable(fake.egyptian_name)
    assert callable(fake.egyptian_full_name)
    assert callable(fake.egyptian_person)
    assert callable(fake.egyptian_father)
    assert callable(fake.egyptian_grandfather)
    assert callable(fake.egyptian_family)


def test_egyptian_name_returns_engine_object():
    fake = egyptian_faker()
    name = fake.egyptian_name()
    assert isinstance(name, GeneratedName)
    assert name.ar and name.en
    assert len(name.parts_ar) >= 2
    assert len(name.parts_ar) == len(name.parts_en)
    assert name.ar == " ".join(name.parts_ar)
    assert name.en == " ".join(name.parts_en)


def test_lang_ar_en_both():
    fake = egyptian_faker()
    en = fake.egyptian_full_name()
    ar = fake.egyptian_full_name("ar")
    both = fake.egyptian_full_name(lang="both")
    assert isinstance(en, str) and not _ARABIC.search(en)
    assert isinstance(ar, str) and _ARABIC.search(ar)
    assert isinstance(both, tuple) and len(both) == 2
    assert _ARABIC.search(both[0])
    assert not _ARABIC.search(both[1])


def test_slots_index_one_generated_chain(monkeypatch):
    canned = GeneratedName(
        ar="يارا عادل فاروق الشناوي",
        en="Yara Adel Farouk Elshenawy",
        parts_ar=["يارا", "عادل", "فاروق", "الشناوي"],
        parts_en=["Yara", "Adel", "Farouk", "Elshenawy"],
    )
    seen = []

    def fake_generate(**kwargs):
        seen.append(kwargs)
        return [canned]

    monkeypatch.setattr(provider_mod._engine, "generate", fake_generate)
    fake = egyptian_faker()

    assert fake.egyptian_full_name() == "Yara Adel Farouk Elshenawy"
    assert fake.egyptian_full_name("ar") == "يارا عادل فاروق الشناوي"
    assert fake.egyptian_person() == "Yara"
    assert fake.egyptian_father() == "Adel"
    assert fake.egyptian_grandfather() == "Farouk"
    assert fake.egyptian_family() == "Elshenawy"
    assert fake.egyptian_person(lang="both") == ("يارا", "Yara")

    assert seen
    assert all(call["count"] == 1 for call in seen)


def test_generate_kwargs_are_forwarded(monkeypatch):
    canned = GeneratedName(
        ar="أ ب ج",
        en="A B C",
        parts_ar=["أ", "ب", "ج"],
        parts_en=["A", "B", "C"],
    )
    seen = []

    def fake_generate(**kwargs):
        seen.append(kwargs)
        return [canned]

    monkeypatch.setattr(provider_mod._engine, "generate", fake_generate)
    fake = egyptian_faker()
    fake.egyptian_name(
        gender="female",
        religion="christian",
        length=4,
        family_name=True,
        frequency="common",
        seed=7,
    )

    assert len(seen) == 1
    assert seen[0] == {
        "count": 1,
        "gender": "female",
        "religion": "christian",
        "length": 4,
        "family_name": True,
        "frequency": "common",
        "seed": 7,
    }


def test_family_name_false_has_empty_family(monkeypatch):
    canned = GeneratedName(
        ar="أ ب ج",
        en="A B C",
        parts_ar=["أ", "ب", "ج"],
        parts_en=["A", "B", "C"],
    )
    monkeypatch.setattr(
        provider_mod._engine,
        "generate",
        lambda **kwargs: [canned],
    )
    fake = egyptian_faker()
    assert fake.egyptian_family(family_name=False) == ""
    assert fake.egyptian_grandfather(family_name=False) == "C"


def test_faker_seed_is_reproducible():
    a = Faker()
    a.seed_instance(42)
    a.add_provider(Provider)
    b = Faker()
    b.seed_instance(42)
    b.add_provider(Provider)
    assert a.egyptian_full_name() == b.egyptian_full_name()
    assert a.egyptian_name().en != ""  # engine still runs

    c = Faker()
    c.seed_instance(99)
    c.add_provider(Provider)
    a.seed_instance(42)
    assert a.egyptian_full_name() != c.egyptian_full_name()


def test_explicit_seed_overrides_faker_rng():
    fake = egyptian_faker()
    fake.seed_instance(1)
    left = fake.egyptian_full_name(seed=123)
    fake.seed_instance(999)
    right = fake.egyptian_full_name(seed=123)
    assert left == right


def test_default_chain_has_father_and_family():
    fake = egyptian_faker()
    name = fake.egyptian_name()
    assert len(name.parts_en) >= 4
    assert fake.egyptian_father(seed=0)
    assert fake.egyptian_family(seed=0)


def test_parse_template():
    fake = egyptian_faker()
    text = fake.parse("{{egyptian_full_name}}")
    assert text and text != "{{egyptian_full_name}}"
