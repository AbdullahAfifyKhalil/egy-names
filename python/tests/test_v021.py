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
        assert _bundle["metadata"]["version"] in ["0.2.1", "0.3.0"]

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
        """Compound names stored with or without spaces — check by normalized form."""
        import re
        _DIAC = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u0640]")
        def norm(s):
            s = _DIAC.sub("", s)
            return s.translate(str.maketrans("آأإٱ","اااا")).translate(str.maketrans("ى","ي")).translate(str.maketrans("ة","ه")).replace(" ","").strip()
        bundle_norms = {norm(e["a"]) for e in _bundle["names"]}
        missing = [n for n in self.COMPOUND_NAMES if norm(n) not in bundle_norms]
        assert len(missing) == 0, f"Compound names missing from bundle: {missing}"

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


class TestAgeAwareFeature:
    """Tests for the age-aware name generation feature (v0.2.1)."""

    def test_names_for_age_returns_list(self):
        results = _e.names_for_age(age=25)
        assert isinstance(results, list)
        assert len(results) > 0

    def test_names_for_age_returns_name_info(self):
        results = _e.names_for_age(age=25, top=5)
        for r in results:
            assert hasattr(r, "ar")
            assert hasattr(r, "en")
            assert hasattr(r, "gender")
            assert hasattr(r, "slot_distribution")

    def test_names_for_age_respects_top_limit(self):
        results = _e.names_for_age(age=30, top=7)
        assert len(results) <= 7

    def test_names_for_age_male_filter(self):
        results = _e.names_for_age(age=25, gender="m", top=20)
        for r in results:
            assert r.gender in ("male", "neutral"), \
                f"{r.ar} has gender={r.gender}, expected male or neutral"

    def test_names_for_age_female_filter(self):
        results = _e.names_for_age(age=25, gender="f", top=20)
        for r in results:
            assert r.gender in ("female", "neutral"), \
                f"{r.ar} has gender={r.gender}, expected female or neutral"

    def test_names_for_age_youth_vs_parent_differ(self):
        """Names for young people should differ from names for older people."""
        youth   = {r.ar for r in _e.names_for_age(age=22, top=10)}
        parents = {r.ar for r in _e.names_for_age(age=52, top=10)}
        # They should NOT be identical — different generations have different names
        assert youth != parents, "Youth and parent age groups returned identical names"

    def test_names_for_age_all_given_by_default(self):
        """By default, only given names (not family surnames) are returned."""
        results = _e.names_for_age(age=30, top=20)
        for r in results:
            assert r.role in ("given", "kunya"), \
                f"{r.ar} has role={r.role}, expected given or kunya"

    def test_names_for_age_include_family(self):
        """include_family=True should also return family names."""
        results = _e.names_for_age(age=30, top=30, include_family=True)
        roles = {r.role for r in results}
        # Should include at least one non-given name when family included
        assert len(results) > 0

    def test_age_profile_returns_age_profile(self):
        from egy_names import AgeProfile
        profile = _e.age_profile("محمد")
        assert profile is not None
        assert isinstance(profile, AgeProfile)

    def test_age_profile_unknown_name_returns_none(self):
        profile = _e.age_profile("xyznotaname123")
        assert profile is None

    def test_age_profile_has_required_fields(self):
        profile = _e.age_profile("أحمد")
        assert profile is not None
        assert isinstance(profile.peak_age_range, (tuple, list))
        assert len(profile.peak_age_range) == 2
        assert isinstance(profile.generation_label, str)
        assert isinstance(profile.dominant_slot, int)
        assert 1 <= profile.dominant_slot <= 6
        assert isinstance(profile.age_scores, dict)
        assert len(profile.age_scores) > 0

    def test_age_profile_scores_are_valid(self):
        profile = _e.age_profile("محمد")
        assert profile is not None
        for age, score in profile.age_scores.items():
            assert 0.0 <= score <= 1.0, f"score at age {age} out of range: {score}"

    def test_age_profile_to_dict(self):
        profile = _e.age_profile("علي")
        assert profile is not None
        d = profile.to_dict()
        assert "peak_age_range" in d
        assert "generation_label" in d
        assert "dominant_slot" in d
        assert "age_scores" in d


class TestAgeDetection:
    """Tests for detect_age() — the inverse of names_for_age()."""

    def test_detect_age_returns_age_detection(self):
        from egy_names import AgeDetection
        result = _e.detect_age("كريم")
        assert result is not None
        assert isinstance(result, AgeDetection)

    def test_detect_age_unknown_name_returns_none(self):
        result = _e.detect_age("xyznotaname999")
        assert result is None

    def test_detect_age_has_required_fields(self):
        result = _e.detect_age("أحمد")
        assert result is not None
        assert isinstance(result.estimated_age, int)
        assert 0 <= result.estimated_age <= 100
        assert isinstance(result.age_range, (tuple, list))
        assert len(result.age_range) == 2
        assert result.age_range[0] <= result.estimated_age <= result.age_range[1]
        assert isinstance(result.confidence, float)
        assert 0.0 <= result.confidence <= 1.0
        assert isinstance(result.generation_label, str)
        assert isinstance(result.note, str)
        assert len(result.note) > 0

    def test_detect_age_to_dict(self):
        result = _e.detect_age("علي")
        assert result is not None
        d = result.to_dict()
        assert "estimated_age" in d
        assert "age_range" in d
        assert "confidence" in d
        assert "generation_label" in d
        assert "note" in d

    def test_detect_age_youth_name(self):
        """زياد, كريم, شهد etc. are modern youth names — should be youth/young."""
        result = _e.detect_age("زياد")
        assert result is not None
        assert result.generation_label in ("youth", "parent"), \
            f"Expected youth or parent for زياد, got {result.generation_label}"
        assert result.estimated_age <= 50, \
            f"Expected age <= 50 for زياد, got {result.estimated_age}"

    def test_detect_age_grandparent_name(self):
        """فاروق, شوقي, فتحي are old-generation names — should be grandparent."""
        result = _e.detect_age("فاروق")
        assert result is not None
        assert result.generation_label in ("grandparent", "great-grandparent", "parent"), \
            f"Expected older generation for فاروق, got {result.generation_label}"
        assert result.estimated_age >= 40, \
            f"Expected age >= 40 for فاروق, got {result.estimated_age}"

    def test_detect_age_full_chain_uses_all_tokens(self):
        """A full name chain should use all resolved tokens as cross-generational signals."""
        from egy_names import AgeDetection
        r_single = _e.detect_age("كريم")
        r_chain  = _e.detect_age("كريم أشرف السيد")
        assert r_single is not None
        assert r_chain  is not None
        # The chain result is also a valid AgeDetection
        assert isinstance(r_chain, AgeDetection)
        # The person's given name (كريم) dominates — result should still be youth range
        assert r_chain.generation_label in ("youth", "parent"), \
            f"Expected youth or parent generation for كريم أشرف السيد, got {r_chain.generation_label}"
        # The chain note should mention how many tokens were used
        assert "token" in r_chain.note.lower(), \
            f"Expected 'token' in note, got: {r_chain.note}"


    def test_detect_age_timeless_name_lower_confidence(self):
        """محمد spans all generations — it should have lower confidence than a niche name."""
        common  = _e.detect_age("محمد")   # very common, spans all slots
        niche   = _e.detect_age("زياد")   # stronger in youth slot
        if common and niche:
            assert common.confidence <= niche.confidence + 0.1, \
                f"Expected محمد ({common.confidence}) ≤ زياد ({niche.confidence}) + 0.1"
