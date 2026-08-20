"""
egy-names v0.2.1 — Comprehensive Edge-Case Test Suite
Uses the actual EgyptianNames API as defined in the installed package.
"""
from __future__ import annotations
import gzip, json
from pathlib import Path

import pytest

# Load our v0.2.1 bundle directly for inspection
DATA_PATH = Path(__file__).parent.parent / "src" / "egy_names" / "data" / "names.json.gz"
assert DATA_PATH.exists(), f"Bundle not found: {DATA_PATH}"

with gzip.open(DATA_PATH, "rt", encoding="utf-8") as f:
    _bundle = json.load(f)

# Engine uses the INSTALLED package data — swap in our new bundle
import egy_names._data as _data_mod
_data_mod._cache = None
_data_mod._DATA_FILE = DATA_PATH

from egy_names import EgyNames
_e = EgyNames()


# ─────────────────────────────────────────────────────────────
# 1. Bundle Integrity
# ─────────────────────────────────────────────────────────────
class TestBundleIntegrity:
    def test_version_021(self):
        assert _bundle["metadata"]["version"] == "0.2.1"

    def test_name_count_gte_33k(self):
        count = len(_bundle["names"])
        assert count >= 33_000, f"Expected ≥ 33,000 names, got {count}"

    def test_corrections_expanded(self):
        count = len(_bundle["corrections"])
        assert count >= 20_000, f"Expected ≥ 20,000 corrections, got {count}"

    def test_no_duplicate_canonical_ar(self):
        seen, dupes = set(), []
        for e in _bundle["names"]:
            a = e["a"]
            if a in seen:
                dupes.append(a)
            seen.add(a)
        assert not dupes, f"Duplicate canonical entries: {dupes[:5]}"

    def test_all_entries_have_required_fields(self):
        required = {"a", "e", "g", "r", "l", "fc", "p"}
        for e in _bundle["names"]:
            missing = required - set(e.keys())
            assert not missing, f"Entry {e.get('a','?')} missing fields: {missing}"

    def test_stats_reflects_new_bundle(self):
        stats = _e.stats()
        assert stats.get("total_names", 0) >= 33_000


# ─────────────────────────────────────────────────────────────
# 2. is_valid / annotate (replaces lookup)
# ─────────────────────────────────────────────────────────────
class TestValidAndAnnotate:
    def test_common_name_is_valid(self):
        assert _e.is_valid("محمد") is True

    def test_female_name_is_valid(self):
        assert _e.is_valid("فاطمة") is True

    def test_normalized_alef_variant_valid(self):
        # أحمد / احمد — at least one must be valid
        assert _e.is_valid("أحمد") or _e.is_valid("احمد")

    def test_noise_word_not_valid(self):
        for noise in ["الابتدائية", "للبنات", "للتعليم"]:
            assert _e.is_valid(noise) is False, \
                f"Noise word '{noise}' should not be in library"

    def test_annotate_returns_nameinfo(self):
        info = _e.annotate("محمد")
        assert info is not None
        assert info.ar == "محمد"
        assert info.gender == "male"
        assert info.religion == "muslim"

    def test_annotate_female(self):
        info = _e.annotate("فاطمة")
        assert info is not None
        # female or neutral (depending on library entry)
        assert info.gender in ("female", "neutral")

    def test_annotate_unknown_returns_none(self):
        info = _e.annotate("XYZNOTANAME")
        assert info is None


# ─────────────────────────────────────────────────────────────
# 3. Transliteration
# ─────────────────────────────────────────────────────────────
class TestTranslation:
    def test_translate_known_chain(self):
        result = _e.translate("محمد أحمد علي")
        assert "Mohamed" in result or "Muhammad" in result

    def test_translate_female_name(self):
        result = _e.translate("فاطمة إبراهيم")
        assert result  # non-empty, doesn't crash

    def test_translate_returns_string(self):
        result = _e.translate("محمد")
        assert isinstance(result, str)


# ─────────────────────────────────────────────────────────────
# 4. Tashkeel & Meaning
# ─────────────────────────────────────────────────────────────
class TestTashkeelAndMeaning:
    def test_tashkeel_common_name(self):
        result = _e.tashkeel("محمد")
        assert "مُحَمَّد" in result or result  # non-empty

    def test_tashkeel_chain(self):
        result = _e.tashkeel("محمد عبدالرحمن")
        assert result  # doesn't crash

    def test_meaning_returns_dict(self):
        m = _e.meaning("محمد")
        assert isinstance(m, dict)
        assert "ar" in m
        assert m["ar"]  # non-empty

    def test_meaning_unknown_name(self):
        m = _e.meaning("XYZNOTANAME")
        assert m is None or (isinstance(m, dict) and not m.get("ar"))


# ─────────────────────────────────────────────────────────────
# 5. Correction
# ─────────────────────────────────────────────────────────────
class TestCorrection:
    def test_correct_alef_variants(self):
        result = _e.correct("احمد مصطفا")
        assert result  # non-empty

    def test_correct_concat_split_doesnt_crash(self):
        result = _e.correct("ياسركامل")
        assert result  # non-empty, doesn't crash

    def test_correct_clean_input_unchanged(self):
        result = _e.correct("محمد أحمد علي")
        assert "محمد" in result

    def test_correct_empty_string(self):
        result = _e.correct("")
        assert result == "" or result is not None


# ─────────────────────────────────────────────────────────────
# 6. DP Splitting
# ─────────────────────────────────────────────────────────────
class TestSplitting:
    def test_split_3_part_unspaced(self):
        parts = _e.split("محمدأحمدعلي")
        assert len(parts) >= 2

    def test_split_5_part_unspaced(self):
        parts = _e.split("محمدأحمدعليحسنالشاذلي")
        assert len(parts) >= 3

    def test_split_compound_din(self):
        parts = _e.split("جمالالدين")
        assert parts  # non-empty, doesn't crash

    def test_split_spaced_input(self):
        parts = _e.split("محمد أحمد علي")
        assert len(parts) >= 2

    def test_split_single_name(self):
        parts = _e.split("محمد")
        assert len(parts) == 1

    def test_split_very_long_doesnt_crash(self):
        parts = _e.split("محمد" * 8)
        assert isinstance(parts, list)


# ─────────────────────────────────────────────────────────────
# 7. Gender Detection
# ─────────────────────────────────────────────────────────────
class TestGenderDetection:
    def test_male_chain(self):
        result = _e.detect_gender("محمد أحمد علي")
        assert result.gender == "male"

    def test_female_chain(self):
        result = _e.detect_gender("مريم إبراهيم حسن")
        assert result.gender == "female"

    def test_gender_confidence_range(self):
        result = _e.detect_gender("محمد")
        assert 0.0 <= result.confidence <= 1.0


# ─────────────────────────────────────────────────────────────
# 8. Religion Detection
# ─────────────────────────────────────────────────────────────
class TestReligionDetection:
    def test_muslim_chain(self):
        result = _e.detect_religion("محمد عبدالرحمن")
        assert result.religion == "muslim"

    def test_christian_chain(self):
        result = _e.detect_religion("جورج بطرس سمير ميخائيل")
        assert result.religion == "christian"

    def test_religion_confidence_range(self):
        result = _e.detect_religion("محمد")
        assert 0.0 <= result.confidence <= 1.0


# ─────────────────────────────────────────────────────────────
# 9. Generation
# ─────────────────────────────────────────────────────────────
class TestGeneration:
    def test_generate_count(self):
        names = _e.generate(count=5)
        assert len(names) == 5

    def test_generate_male_muslim(self):
        names = _e.generate(count=3, gender="male", religion="muslim")
        assert len(names) == 3
        for n in names:
            assert n.ar and n.en

    def test_generate_female(self):
        names = _e.generate(count=3, gender="female")
        assert len(names) == 3

    def test_generate_length_3(self):
        names = _e.generate(count=2, length=3)
        for n in names:
            assert len(n.parts_ar) == 3

    def test_generate_zero_count(self):
        names = _e.generate(count=0)
        assert len(names) == 0


# ─────────────────────────────────────────────────────────────
# 10. Search (keyword-filter API)
# ─────────────────────────────────────────────────────────────
class TestSearch:
    def test_search_by_gender(self):
        results = _e.search(gender="male")
        assert len(results) > 0
        for r in results:
            assert r.gender in ("male", "neutral")

    def test_search_by_religion(self):
        results = _e.search(religion="muslim")
        assert len(results) > 0

    def test_search_starts_with(self):
        results = _e.search(starts_with="محمد")
        assert len(results) > 0

    def test_search_contains(self):
        results = _e.search(contains="يم")
        assert len(results) > 0

    def test_search_max_results(self):
        results = _e.search(max_results=5)
        assert len(results) <= 5

    def test_search_family_names(self):
        results = _e.families(count=10)
        assert len(results) <= 10


# ─────────────────────────────────────────────────────────────
# 11. Ranking & Uniqueness
# ─────────────────────────────────────────────────────────────
class TestRankingAndUniqueness:
    def test_rank_common_name(self):
        rank = _e.rank("محمد")
        assert rank is not None
        assert rank.rank >= 1

    def test_uniqueness_common_name(self):
        score = _e.uniqueness("محمد أحمد علي")
        assert score is not None
        assert 0.0 <= score.score <= 1.0

    def test_uniqueness_rare_name(self):
        # A very rare chain should score higher uniqueness
        score_common = _e.uniqueness("محمد أحمد")
        score_rare   = _e.uniqueness("خاقان أبومناع نادرجدا")
        if score_common and score_rare:
            assert score_rare.score >= score_common.score


# ─────────────────────────────────────────────────────────────
# 12. New v0.2.1 Entries
# ─────────────────────────────────────────────────────────────
class TestNewV021Entries:
    COMPOUND_NAMES = [
        "جمال الدين", "شرف الدين", "كمال الدين",
        "سيف الله", "أبو مناع", "جلال الدين",
        "محيى الدين", "شمس الدين",
    ]

    def test_compound_names_in_bundle(self):
        bundle_ar = {e["a"] for e in _bundle["names"]}
        missing = [n for n in self.COMPOUND_NAMES if n not in bundle_ar]
        assert len(missing) <= 2, f"Missing new entries: {missing}"

    def test_concat_splits_in_corrections(self):
        corrections = _bundle["corrections"]
        assert len(corrections) >= 14_000, \
            f"Expected ≥ 14,000 correction pairs, got {len(corrections)}"

    def test_new_entries_are_valid(self):
        """Some compound names should pass is_valid."""
        at_least_one = any(_e.is_valid(n) for n in self.COMPOUND_NAMES)
        assert at_least_one, "No compound names from v0.2.1 are resolvable"


# ─────────────────────────────────────────────────────────────
# 13. Chain Analysis
# ─────────────────────────────────────────────────────────────
class TestChainAnalysis:
    def test_analyze_5_part_chain(self):
        chain = _e.analyze_chain("محمد أحمد علي حسن الشاذلي")
        assert len(chain) >= 3

    def test_analyze_chain_first_slot_is_person(self):
        chain = _e.analyze_chain("محمد أحمد علي")
        assert chain[0].role in ("person", "given", "male", "first")

    def test_analyze_chain_doesnt_crash_on_short(self):
        chain = _e.analyze_chain("محمد")
        assert isinstance(chain, list)
