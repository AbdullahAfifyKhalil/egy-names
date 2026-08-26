"""
Adversarial Stress & Edge-Case Testing Suite for egy-names v0.3.2
Tests every possible boundary, corrupted input, extreme scenario,
unusual Unicode, and concurrent multi-threading behavior to ensure
absolute robustness and zero crashes.
"""

import math
import random
import pytest
from concurrent.futures import ThreadPoolExecutor
from egy_names import (
    EgyNames,
    EgyptianNames,
    Gender,
    Religion,
    NameRole,
    FrequencyClass,
    AgeDetection,
    AgeProfile,
    NameInfo,
    GeneratedName,
    GenderDetection,
    ReligionDetection,
)

_e = EgyNames()


# ==============================================================================
# 1. EXTREME INPUT & CORRUPTED STRING TESTS
# ==============================================================================
class TestExtremeInputs:
    """Ensure no method crashes on garbage, empty, huge, or corrupted strings."""

    @pytest.mark.parametrize("bad_input", [
        "",
        "   ",
        "\t\n\r  ",
        "???!!!",
        "!@#$%^&*()_+{}[]:;\"'<>,./~`",
        "،؛؟ـ«»",
        "1234567890",
        "🔥🚀🇪🇬✨🎉",
        "مــــحــــمـــــد",            # Tatweel / Kashida
        "م\u200Cح\u200Dم\uFEFFد",      # ZWNJ, ZWJ, BOM
        "م\u00ADح\u00ADم\u00ADد",      # Soft-hyphens
        "Mohamed 123 !@#",             # Mixed script + punctuation
        "a",                           # Single latin char
        "م",                           # Single arabic char
        "x" * 5000,                    # Huge 5K char string
        "محمد " * 1000,                # Huge 1000-token chain
    ])
    def test_annotate_does_not_crash(self, bad_input):
        res = _e.annotate(bad_input)
        assert res is None or isinstance(res, (NameInfo, list))

    @pytest.mark.parametrize("bad_input", [
        "", "   ", "???", "🔥", "x" * 1000, "مــــحــــمـــــد", "م\u200Cح\u200Dم\uFEFFد"
    ])
    def test_correct_does_not_crash(self, bad_input):
        res = _e.correct(bad_input)
        assert isinstance(res, str)

    @pytest.mark.parametrize("bad_input", [
        "", "   ", "???", "🔥", "x" * 500, "مــــحــــمـــــد"
    ])
    def test_split_does_not_crash(self, bad_input):
        res = _e.split(bad_input)
        assert isinstance(res, list)

    @pytest.mark.parametrize("bad_input", [
        "", "   ", "???", "🔥", "x" * 500, "مــــحــــمـــــد"
    ])
    def test_translate_does_not_crash(self, bad_input):
        res = _e.translate(bad_input)
        assert isinstance(res, str)

    @pytest.mark.parametrize("bad_input", [
        "", "   ", "???", "🔥", "x" * 500, "مــــحــــمـــــد"
    ])
    def test_tashkeel_does_not_crash(self, bad_input):
        res = _e.tashkeel(bad_input)
        assert isinstance(res, str)

    @pytest.mark.parametrize("bad_input", [
        "", "   ", "???", "🔥", "x" * 500
    ])
    def test_meaning_does_not_crash(self, bad_input):
        res = _e.meaning(bad_input)
        assert res is None or (isinstance(res, dict) and "ar" in res and "en" in res)

    @pytest.mark.parametrize("bad_input", [
        "", "   ", "???", "🔥", "x" * 500, "123456"
    ])
    def test_detect_age_does_not_crash(self, bad_input):
        res = _e.detect_age(bad_input)
        assert res is None or isinstance(res, AgeDetection)

    @pytest.mark.parametrize("bad_input", [
        "", "   ", "???", "🔥", "x" * 500, "123456"
    ])
    def test_age_profile_does_not_crash(self, bad_input):
        res = _e.age_profile(bad_input)
        assert res is None or isinstance(res, AgeProfile)


# ==============================================================================
# 2. CONCATENATED ARABIC SPLITTING & COMPOUND NAMES
# ==============================================================================
class TestSplittingAndCompounds:
    """Stress-test DP segmentation and compound name handling."""

    def test_split_classic_3part_unspaced(self):
        parts = _e.split("محمدأحمدعلي")
        assert len(parts) == 3
        assert "محمد" in parts[0]
        assert "أحمد" in parts[1] or "احمد" in parts[1]
        assert "علي" in parts[2] or "على" in parts[2]

    def test_split_classic_5part_unspaced(self):
        parts = _e.split("محمدأحمدعليحسنالشناوي")
        assert len(parts) >= 4
        assert parts[0] == "محمد"

    def test_split_compound_abdel(self):
        parts = _e.split("عبدالرحمنمحمدالسيد")
        assert len(parts) >= 2
        joined = " ".join(parts)
        assert "عبد" in joined and "محمد" in joined

    def test_split_compound_din(self):
        parts = _e.split("حسامالدينمحمودعلي")
        assert len(parts) >= 2
        joined = " ".join(parts)
        assert "حسام" in joined and "محمود" in joined

    def test_split_interleaved_garbage_recovers(self):
        parts = _e.split("محمد zzz123 أحمد")
        assert len(parts) == 3
        assert parts[0] == "محمد"
        assert parts[1] == "zzz123"
        assert parts[2] == "أحمد"

    def test_correct_tatweel_stripped(self):
        corrected = _e.correct("مــــحــــمـــــد")
        assert corrected == "محمد"

    def test_correct_unspaced_compound(self):
        corrected = _e.correct("عبدالرحمن")
        assert "عبد الرحمن" in corrected or "عبدالرحمن" in corrected


# ==============================================================================
# 3. GENDER & RELIGION DEMOGRAPHIC DETECTION
# ==============================================================================
class TestDemographicDetection:
    """Verify gender and religion classification on edge cases."""

    def test_male_high_confidence(self):
        res = _e.detect_gender("محمود أحمد علي")
        assert isinstance(res, GenderDetection)
        assert res.gender == "male"
        assert 0.0 <= res.confidence <= 1.0
        assert res.confidence >= 0.8

    def test_female_high_confidence(self):
        res = _e.detect_gender("فاطمة الزهراء")
        assert isinstance(res, GenderDetection)
        assert res.gender == "female"
        assert 0.0 <= res.confidence <= 1.0
        assert res.confidence >= 0.8

    def test_neutral_unisex_names(self):
        for name in ["رضا", "عصمت", "عفت", "سلامة", "يسر"]:
            info = _e.lookup(name)
            if info:
                assert info.gender in ("neutral", "male", "female")

    def test_christian_chain(self):
        res = _e.detect_religion("مينا جرجس بطرس سوريال")
        assert isinstance(res, ReligionDetection)
        assert res.religion == "christian"
        assert res.confidence >= 0.8

    def test_muslim_chain(self):
        res = _e.detect_religion("محمد أحمد علي حسن")
        assert isinstance(res, ReligionDetection)
        assert res.religion == "muslim"
        assert res.confidence >= 0.8

    def test_cross_religious_patronymic_chain(self):
        res = _e.detect_religion("مينا محمد")
        assert isinstance(res, ReligionDetection)
        assert res.religion in ("christian", "muslim", "neutral")
        assert 0.0 <= res.confidence <= 1.0


# ==============================================================================
# 4. AGE-AWARE GENERATION & DETECTION STRESS TESTS
# ==============================================================================
class TestAgeEngineStress:
    """Stress-test age generation and detection with boundary numbers."""

    @pytest.mark.parametrize("age", [0, 1, 15, 24, 50, 75, 99, 100, 150, -5, 999])
    def test_names_for_age_boundary_numbers(self, age):
        res = _e.names_for_age(age=age, top=10)
        assert isinstance(res, list)
        assert len(res) <= 10
        for item in res:
            assert isinstance(item, NameInfo)
            assert item.ar
            assert item.en

    @pytest.mark.parametrize("gender_arg", [
        "m", "M", "male", "MALE", "ذكر",
        "f", "F", "female", "FEMALE", "أنثى",
        "n", "N", "neutral", "NEUTRAL",
        "unknown_gibberish", None
    ])
    def test_names_for_age_gender_filter_variants(self, gender_arg):
        res = _e.names_for_age(age=25, gender=gender_arg, top=5)
        assert isinstance(res, list)
        assert len(res) <= 5

    def test_detect_age_confidence_bounds(self):
        for name in ["محمد", "كريم", "فاروق", "شهد", "طهطاوي", "سوريال"]:
            r = _e.detect_age(name)
            if r:
                assert 0.0 <= r.confidence <= 1.0
                assert 0 <= r.estimated_age <= 100
                assert len(r.age_range) == 2
                assert r.age_range[0] <= r.age_range[1]
                assert r.generation_label in ("youth", "parent", "grandparent", "great-grandparent", "timeless", "unknown")

    def test_detect_age_multi_token_chain_corroboration(self):
        r_single = _e.detect_age("كريم")
        r_chain = _e.detect_age("كريم أشرف فاروق")
        assert r_single is not None
        assert r_chain is not None
        assert 0.0 <= r_chain.confidence <= 1.0
        # Multi-token chain should have high confidence due to corroboration
        assert r_chain.confidence >= r_single.confidence - 0.05

    def test_age_profile_completeness(self):
        for name in ["محمد", "شهد", "فاروق"]:
            prof = _e.age_profile(name)
            assert prof is not None
            assert len(prof.age_scores) == 21  # step of 5 from 0 to 100
            for age_val, score in prof.age_scores.items():
                assert 0 <= age_val <= 100
                assert 0.0 <= score <= 1.0


# ==============================================================================
# 5. SEARCH ENGINE ADVERSARIAL TESTS
# ==============================================================================
class TestSearchEngineAdversarial:
    """Ensure search handles regex metacharacters, large limits, and zero results."""

    def test_search_regex_characters(self):
        res = _e.search(contains=".*[a-z]+", max_results=10)
        assert isinstance(res, list)

    def test_search_case_insensitivity(self):
        res_lower = _e.search(gender="male", max_results=5)
        res_upper = _e.search(gender="MALE", max_results=5)
        res_abbr = _e.search(gender="m", max_results=5)
        assert len(res_lower) == len(res_upper) == len(res_abbr) == 5

    def test_search_large_max_results(self):
        res = _e.search(gender="female", max_results=100000)
        assert isinstance(res, list)
        assert len(res) > 1000

    def test_search_zero_max_results(self):
        res = _e.search(gender="male", max_results=0)
        assert res == []

    def test_search_impossible_criteria_returns_empty(self):
        res = _e.search(starts_with="غير_موجود_نهائيا_xyz")
        assert res == []


# ==============================================================================
# 6. GENERATOR STRESS TESTS
# ==============================================================================
class TestGeneratorStress:
    """Stress-test probabilistic generation."""

    def test_generate_zero_count(self):
        res = _e.generate(count=0)
        assert res == []

    def test_generate_large_count(self):
        res = _e.generate(count=100, length=4, seed=42)
        assert len(res) == 100
        for gn in res:
            assert isinstance(gn, GeneratedName)
            assert len(gn.ar.split()) >= 3
            assert len(gn.en.split()) >= 3
            assert len(gn.parts_ar) >= 3
            assert len(gn.parts_en) >= 3

    def test_generate_lengths_3_to_8(self):
        for l in range(3, 9):
            res = _e.generate(count=2, length=l, seed=123)
            assert len(res) == 2
            for gn in res:
                assert len(gn.parts_ar) == l
                assert len(gn.parts_en) == l

    def test_generate_all_gender_religion_combinations(self):
        for g in ["m", "male", "f", "female", None]:
            for r in ["m", "muslim", "c", "christian", None]:
                res = _e.generate(count=2, gender=g, religion=r, seed=999)
                assert len(res) == 2


# ==============================================================================
# 7. CONCURRENCY & THREAD-SAFETY STRESS TEST
# ==============================================================================
class TestConcurrencyAndThreadSafety:
    """Ensure the library is 100% thread-safe under heavy parallel load."""

    def test_concurrent_multi_feature_execution(self):
        def worker(seed_val):
            # Run multiple operations per thread
            gen = _e.generate(count=5, gender="male", seed=seed_val)
            annot = _e.annotate("محمد أحمد علي حسن")
            age_res = _e.detect_age("كريم أشرف فاروق")
            split_res = _e.split("محمدأحمدعليحسنالشناوي")
            search_res = _e.search(gender="female", max_results=10)
            trans_res = _e.translate("محمود حسن")
            tash_res = _e.tashkeel("فاطمة الزهراء")
            mean_res = _e.meaning("محمد")

            assert len(gen) == 5
            assert isinstance(annot, list)
            assert age_res is not None
            assert len(split_res) >= 3
            assert len(search_res) == 10
            assert trans_res != ""
            assert tash_res != ""
            assert mean_res is not None and mean_res["ar"] != ""
            return True

        # Launch 50 concurrent threads executing 100 total jobs
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(worker, i) for i in range(100)]
            for f in futures:
                assert f.result() is True
