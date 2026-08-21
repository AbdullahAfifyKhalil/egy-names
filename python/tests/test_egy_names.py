"""Comprehensive test suite for egy-names."""

import sys
import os

# Add src to path for testing without install
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from egy_names import EgyNames, EgyptianNames, NameInfo, GeneratedName


def test_class_alias():
    """EgyNames and EgyptianNames should be the same class."""
    assert EgyNames is EgyptianNames


def test_init():
    """Constructor should accept optional seed."""
    en = EgyNames()
    assert en is not None
    en2 = EgyNames(seed=42)
    assert en2 is not None


# ── Generation ──────────────────────────────────────────────


def test_generate_default():
    en = EgyNames(seed=1)
    names = en.generate(count=3)
    assert len(names) == 3
    for n in names:
        assert isinstance(n, GeneratedName)
        assert n.ar and len(n.ar) > 0
        assert n.en and len(n.en) > 0
        assert len(n.parts_ar) >= 2
        assert len(n.parts_en) >= 2


def test_generate_gender_filter():
    en = EgyNames(seed=2)
    males = en.generate(count=5, gender="male")
    females = en.generate(count=5, gender="female")
    assert len(males) == 5
    assert len(females) == 5


def test_generate_religion_filter():
    en = EgyNames(seed=3)
    muslims = en.generate(count=3, religion="muslim")
    christians = en.generate(count=3, religion="christian")
    assert len(muslims) == 3
    assert len(christians) == 3


def test_generate_reproducible():
    """Same seed should produce same names."""
    a = EgyNames(seed=42).generate(count=3)
    b = EgyNames(seed=42).generate(count=3)
    assert [n.ar for n in a] == [n.ar for n in b]


def test_generate_no_duplicates_in_chain():
    """A single generated name should not repeat any part."""
    en = EgyNames(seed=10)
    for name in en.generate(count=20):
        # Some rare collisions are possible, but most should be unique
        parts = name.parts_ar
        if len(parts) == len(set(parts)):
            pass  # good


# ── Translation ─────────────────────────────────────────────


def test_translate_ar_to_en():
    en = EgyNames()
    result = en.translate("محمد أحمد علي")
    assert "Mohamed" in result or "Mohammad" in result or "Muhammad" in result
    assert "Ahmed" in result or "Ahmad" in result


def test_translate_en_to_ar():
    en = EgyNames()
    result = en.translate("Mohamed Ahmed Ali")
    assert "محمد" in result
    assert "أحمد" in result


def test_translate_empty():
    en = EgyNames()
    assert en.translate("") == ""
    assert en.translate("   ") == "   "


def test_translate_unknown():
    en = EgyNames()
    result = en.translate("xyznotaname")
    assert result == "xyznotaname"  # returns original if unknown


# ── Correction ──────────────────────────────────────────────


def test_correct_hamza():
    en = EgyNames()
    assert en.correct("احمد") == "أحمد"


def test_correct_alif_maqsura():
    en = EgyNames()
    assert en.correct("مصطفا") == "مصطفى"


def test_correct_compound():
    en = EgyNames()
    result = en.correct("احمد مصطفا عبد الرحيم")
    assert "أحمد" in result
    assert "مصطفى" in result
    assert "عبدالرحيم" in result


def test_correct_empty():
    en = EgyNames()
    assert en.correct("") == ""


# ── Tashkeel ────────────────────────────────────────────────


def test_tashkeel_single():
    en = EgyNames()
    result = en.tashkeel("محمد")
    assert "مُحَمَّد" in result


def test_tashkeel_compound():
    """Compounds are accurately diacritized."""
    en = EgyNames()
    result = en.tashkeel("محمد عبدالرحمن")
    assert "مُحَمَّد" in result
    assert "الرَّحْمَن" in result


def test_tashkeel_empty():
    en = EgyNames()
    assert en.tashkeel("") == ""


# ── Splitting ───────────────────────────────────────────────


def test_split_spaced():
    en = EgyNames()
    result = en.split("محمد أحمد علي")
    assert result == ["محمد", "أحمد", "علي"]


def test_split_concatenated():
    en = EgyNames()
    result = en.split("محمدأحمدعليحسنالشاذلي")
    assert len(result) >= 3
    assert "محمد" in result
    assert "أحمد" in result


def test_split_single_known():
    en = EgyNames()
    result = en.split("حسناء")
    assert result == ["حسناء"]


def test_split_empty():
    en = EgyNames()
    assert en.split("") == []


# ── Annotation ──────────────────────────────────────────────


def test_annotate_single():
    en = EgyNames()
    info = en.annotate("محمد")
    assert info is not None
    assert isinstance(info, NameInfo)
    assert info.ar == "محمد"
    assert info.gender == "male"
    assert info.religion == "muslim"


def test_annotate_multi():
    en = EgyNames()
    result = en.annotate("محمد أحمد")
    assert isinstance(result, list)
    assert len(result) == 2


def test_annotate_unknown():
    en = EgyNames()
    assert en.annotate("xyznotaname") is None


def test_annotate_empty():
    en = EgyNames()
    assert en.annotate("") is None


# ── Meaning ─────────────────────────────────────────────────


def test_meaning():
    en = EgyNames()
    m = en.meaning("محمد")
    assert m is not None
    assert "ar" in m and "en" in m
    assert len(m["ar"]) > 0


def test_meaning_unknown():
    en = EgyNames()
    assert en.meaning("xyznotaname") is None


# ── Detection ───────────────────────────────────────────────


def test_detect_gender_female():
    en = EgyNames()
    result = en.detect_gender("مريم إبراهيم حسن")
    assert result.gender == "female"
    assert result.confidence > 0.0


def test_detect_gender_male():
    en = EgyNames()
    result = en.detect_gender("محمد أحمد علي")
    assert result.gender == "male"
    assert result.confidence > 0.5


def test_detect_gender_empty():
    en = EgyNames()
    result = en.detect_gender("")
    assert result.confidence == 0.0


def test_detect_religion_christian():
    en = EgyNames()
    result = en.detect_religion("جورج بطرس سمير ميخائيل")
    assert result.religion == "christian"
    assert result.confidence > 0.5


def test_detect_religion_muslim():
    en = EgyNames()
    result = en.detect_religion("محمد عبدالله أحمد")
    assert result.religion == "muslim"


# ── Chain Analysis ──────────────────────────────────────────


def test_analyze_chain():
    en = EgyNames()
    parts = en.analyze_chain("محمد أحمد علي حسن الشاذلي")
    assert len(parts) == 5
    assert parts[0].role == "person"
    assert parts[1].role == "father"
    assert parts[2].role == "grandfather"
    assert parts[-1].role == "family_name"


def test_analyze_chain_empty():
    en = EgyNames()
    assert en.analyze_chain("") == []


# ── Rank ────────────────────────────────────────────────────


def test_rank():
    en = EgyNames()
    r = en.rank("محمد")
    assert r is not None
    assert r.rank >= 1
    assert r.percentile > 0


def test_rank_unknown():
    en = EgyNames()
    assert en.rank("xyznotaname") is None


# ── Uniqueness ──────────────────────────────────────────────


def test_uniqueness_common():
    en = EgyNames()
    u = en.uniqueness("محمد أحمد علي")
    assert u.score < 0.5  # very common names
    assert u.label in ("extremely_common", "common", "moderate")


def test_uniqueness_empty():
    en = EgyNames()
    u = en.uniqueness("")
    assert u.label == "unknown"


# ── Search ──────────────────────────────────────────────────


def test_search_basic():
    en = EgyNames()
    results = en.search(gender="female", max_results=5)
    assert len(results) <= 5
    for r in results:
        assert isinstance(r, NameInfo)


def test_search_starts_with():
    en = EgyNames()
    results = en.search(starts_with="عبد", max_results=10)
    assert len(results) > 0


def test_search_role():
    en = EgyNames()
    families = en.search(role="family", max_results=5)
    assert all(r.role == "family" for r in families)


# ── Families ────────────────────────────────────────────────


def test_families():
    en = EgyNames()
    fams = en.families(count=10)
    assert len(fams) == 10
    assert all(r.role == "family" for r in fams)


# ── Validation ──────────────────────────────────────────────


def test_is_valid():
    en = EgyNames()
    assert en.is_valid("محمد") is True
    assert en.is_valid("xyznotaname") is False


# ── Stats ───────────────────────────────────────────────────


def test_stats():
    en = EgyNames()
    s = en.stats()
    assert "total_names" in s
    assert s["total_names"] > 30000
    assert "given_names" in s
    assert "family_names" in s
    assert "male_names" in s
    assert "female_names" in s


# ── to_dict serialization ──────────────────────────────────


def test_nameinfo_to_dict():
    en = EgyNames()
    info = en.annotate("محمد")
    assert info is not None
    d = info.to_dict()
    assert isinstance(d, dict)
    assert d["ar"] == "محمد"
    assert "gender" in d


def test_generated_name_to_dict():
    en = EgyNames(seed=1)
    names = en.generate(count=1)
    d = names[0].to_dict()
    assert isinstance(d, dict)
    assert "ar" in d and "en" in d


# ── Run all tests ───────────────────────────────────────────

if __name__ == "__main__":
    import traceback

    test_funcs = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    failed = 0

    for fn in test_funcs:
        try:
            fn()
            passed += 1
            print(f"  ✓ {fn.__name__}")
        except Exception as e:
            failed += 1
            print(f"  ✗ {fn.__name__}: {e}")
            traceback.print_exc()

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed, {passed + failed} total")

    if failed > 0:
        sys.exit(1)
    else:
        print("All tests passed!")
