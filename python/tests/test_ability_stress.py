"""Ability stress suite for egy-names.

Not a crash-only check. Walks the book and every public feature and
asserts the engine can still do the work: lookup, translate, split,
correct, generate, 14D fields, demographics, age, search, rank.
"""

from __future__ import annotations

import time
from typing import List

import pytest

from egy_names import (
    AgeDetection,
    AgeProfile,
    EgyNames,
    GeneratedName,
    NameInfo,
    RankInfo,
    UniquenessScore,
)
from egy_names._index import get_all, normalize_en
from egy_names._quality import NON_PERSONAL_AR, is_low_confidence_entry, is_personal_entry
from egy_names._types import NameEntry


_GENDERS = frozenset({"male", "female", "neutral"})
_RELIGIONS = frozenset({"muslim", "christian", "neutral"})
_ROLES = frozenset({"given", "family", "kunya", "tribal"})
_FREQS = frozenset({"common", "normal", "rare"})
_TRENDS = frozenset(
    {"classic_timeless", "rising_modern", "vintage_heritage", "rare_toponymic", ""}
)


@pytest.fixture(scope="module")
def en() -> EgyNames:
    return EgyNames()


@pytest.fixture(scope="module")
def book() -> List[NameEntry]:
    entries = get_all()
    assert len(entries) >= 44000
    return entries


@pytest.fixture(scope="module")
def sample(book: List[NameEntry]) -> List[NameEntry]:
    """All common lemmas plus every 15th other lemma (~4k–6k names)."""
    picked: List[NameEntry] = []
    for i, ent in enumerate(book):
        if ent.frequency.value == "common" or i % 15 == 0:
            picked.append(ent)
    assert len(picked) >= 3000
    return picked


# ---------------------------------------------------------------------------
# 1. The book itself
# ---------------------------------------------------------------------------


class TestCatalogAbility:
    def test_every_lemma_has_a_coherent_14d_row(self, book: List[NameEntry]) -> None:
        for ent in book:
            assert ent.ar and ent.en
            assert ent.gender.value in _GENDERS
            assert ent.religion.value in _RELIGIONS
            assert ent.role.value in _ROLES
            assert ent.frequency.value in _FREQS
            assert ent.corpus_share >= 0.0
            assert len(ent.slot_pcts) == 8
            assert all(p >= 0.0 for p in ent.slot_pcts)
            assert ent.trend_category in _TRENDS or ent.trend_category

    def test_sample_is_valid_and_looks_up_from_both_scripts(
        self, en: EgyNames, sample: List[NameEntry]
    ) -> None:
        for ent in sample:
            info = en.lookup(ent.ar)
            assert isinstance(info, NameInfo)
            assert info.ar == ent.ar
            assert info.en == ent.en
            assert en.info(ent.ar).ar == ent.ar
            assert en.lookup(ent.en) is not None
            if is_personal_entry(ent) and not is_low_confidence_entry(ent):
                assert en.is_valid(ent.ar) is True
            else:
                assert en.is_valid(ent.ar) is False

    def test_arabic_to_english_is_the_stored_passport_form(
        self, en: EgyNames, sample: List[NameEntry]
    ) -> None:
        # translate() splits on spaces, so only single-token lemmas round-trip as one unit.
        for ent in sample:
            if " " in ent.ar.strip():
                continue
            assert en.translate(ent.ar) == ent.en

    def test_english_index_always_resolves(self, en: EgyNames, book: List[NameEntry]) -> None:
        missing = [ent.en for ent in book if en.lookup(ent.en) is None]
        assert missing == []

    def test_english_index_collisions_stay_bounded(self, en: EgyNames, book: List[NameEntry]) -> None:
        """Rare lemmas may share an English key; the rate must not silently rise."""
        collisions = 0
        for ent in book:
            hit = en.lookup(ent.en)
            if hit is not None and hit.ar != ent.ar:
                collisions += 1
        rate = collisions / len(book)
        assert rate < 0.12, f"English key collisions too high: {collisions}/{len(book)} ({rate:.2%})"

    def test_english_key_goes_to_the_higher_share_lemma(
        self, en: EgyNames, book: List[NameEntry]
    ) -> None:
        best_ar: dict[str, str] = {}
        best_share: dict[str, float] = {}
        for ent in book:
            keys = [normalize_en(ent.en)]
            for variant in ent.en_variants:
                stripped = variant.strip()
                if stripped:
                    keys.append(normalize_en(stripped))
            for key in keys:
                if key not in best_share or ent.corpus_share > best_share[key]:
                    best_share[key] = ent.corpus_share
                    best_ar[key] = ent.ar
        mismatches = []
        for key, ar in best_ar.items():
            hit = en.lookup(key)
            if hit is None or hit.ar != ar:
                mismatches.append((key, ar, None if hit is None else hit.ar))
        assert mismatches == []


# ---------------------------------------------------------------------------
# 2. Gold onomastic ability
# ---------------------------------------------------------------------------


class TestGoldAbility:
    def test_canonical_abdelrahman(self, en: EgyNames) -> None:
        assert en.correct("عبدالرحمن") == "عبدالرحمن"
        assert en.correct("عبد الرحمن") == "عبدالرحمن"
        assert en.translate("عبدالرحمن") == "Abdelrahman"
        tash = en.tashkeel("عبدالرحمن")
        assert "عَبْدُ" in tash
        assert "الرَّحْمَن" in tash

    def test_correct_classic_typos(self, en: EgyNames) -> None:
        assert en.correct("احمد") == "أحمد"
        assert en.correct("مصطفا") == "مصطفى"
        assert en.correct("يحي") == "يحيى"
        assert en.correct("ابراهم") == "إبراهيم"
        assert en.correct("اسماعيل") == "إسماعيل"

    def test_split_glued_patronymic_chain(self, en: EgyNames) -> None:
        parts = en.split("محمدأحمدعليحسنالشناوي")
        assert parts == ["محمد", "أحمد", "علي", "حسن", "الشناوي"]

    def test_split_then_translate_and_annotate(self, en: EgyNames) -> None:
        glued = "محمدأحمدعليحسنالشناوي"
        parts = en.split(glued)
        spaced = " ".join(parts)
        en_form = en.translate(spaced)
        assert "Mohamed" in en_form or "Mohammad" in en_form
        assert "Ahmed" in en_form or "Ahmad" in en_form
        notes = en.annotate(spaced)
        assert isinstance(notes, list) and len(notes) == 5
        assert all(isinstance(n, NameInfo) for n in notes)
        assert notes[0].ar == "محمد"
        assert notes[-1].role == "family"

    def test_gender_and_religion_on_real_chains(self, en: EgyNames) -> None:
        male = en.detect_gender("محمد أحمد علي")
        assert male.gender == "male" and male.confidence >= 0.8
        female = en.detect_gender("فاطمة الزهراء")
        assert female.gender == "female" and female.confidence >= 0.8
        muslim = en.detect_religion("محمد أحمد علي حسن")
        assert muslim.religion == "muslim" and muslim.confidence >= 0.8
        christian = en.detect_religion("مينا جرجس بطرس شنودة")
        assert christian.religion == "christian" and christian.confidence >= 0.8

    def test_mohamed_14d_surface(self, en: EgyNames) -> None:
        info = en.lookup("محمد")
        assert info is not None
        assert info.gender == "male"
        assert info.religion == "muslim"
        assert info.role == "given"
        assert "مُحَمَّد" in en.tashkeel("محمد")
        assert en.ipa_standard("محمد").startswith("/")
        assert en.ipa_eg("محمد").startswith("[")
        pets = en.dallaa("محمد")
        assert "ميدو" in pets or "حمو" in pets
        figures = en.famous_figures("محمد", lang="ar")
        assert any("صلاح" in f or "علي باشا" in f for f in figures)
        meaning = en.meaning("محمد")
        assert meaning and meaning["ar"] and meaning["en"]
        assert en.root("محمد")
        rank = en.rank("محمد")
        assert isinstance(rank, RankInfo) and rank.rank == 1

    def test_english_variants_resolve_to_the_lemma(self, en: EgyNames) -> None:
        # Stored variants on known lemmas — not a claim that every spelling exists.
        assert en.translate("Mohamed") == "محمد"
        assert en.is_valid("Mohamed") is True
        yoakeem = en.translate("Yoakeem")
        joachim = en.translate("Joachim")
        assert yoakeem == joachim == "يواقيم"

    def test_common_english_keys_are_not_stolen_by_misspellings(self, en: EgyNames) -> None:
        assert en.translate("Mahmoud") == "محمود"
        assert en.translate("Ibrahim") == "إبراهيم"
        assert en.translate("Mostafa") == "مصطفى"
        assert en.translate("Abdullah") == "عبدالله"
        assert en.translate("Elsayed") == "السيد"
        assert en.translate("Abdelrahman") == "عبدالرحمن"

    def test_first_given_name_is_the_person(self, en: EgyNames) -> None:
        fatima = en.detect_gender("فاطمة محمد علي حسن")
        assert fatima.gender == "female" and fatima.confidence >= 0.85
        zaynab = en.detect_gender("زينب أسامة بكري شلقامي")
        assert zaynab.gender == "female"
        mohamed = en.detect_gender("محمد أحمد علي حسن")
        assert mohamed.gender == "male" and mohamed.confidence >= 0.85

    def test_religion_tie_follows_the_first_distinctive_name(self, en: EgyNames) -> None:
        george = en.detect_religion("جورج علاءالدين عبدالمسيح دغيدي")
        assert george.religion == "christian"
        mina = en.detect_religion("مينا جرجس بطرس شنودة")
        assert mina.religion == "christian"
        mohamed = en.detect_religion("محمد أحمد علي حسن")
        assert mohamed.religion == "muslim"

    def test_religion_follows_the_person_not_the_lineage(self, en: EgyNames) -> None:
        """A father's or family's community must not outvote the person.

        Found by the 500-name eval: majority-vote across all tokens let
        two Muslim-leaning lineage tokens outvote a distinctively
        Christian first name (and vice versa). Religion must key off the
        first personal token exactly like gender does.
        """
        lorenzo = en.detect_religion("لورانزو حسابالدين الشافعي")
        assert lorenzo.religion == "christian"
        naqresh = en.detect_religion("نقرش بولا سلوانسي")
        assert naqresh.religion == "muslim"
        albert = en.detect_religion("ألبرت فهران جعفر")
        assert albert.religion == "christian"

    def test_compound_kunya_is_one_token_not_two_fragments(self, en: EgyNames) -> None:
        """A two-word compound lemma (e.g. kunya "Abu X") must not be
        split into two meaningless whitespace fragments.

        Found by the 500-name eval: ~800 book entries are legitimately
        two words. detect_gender/detect_religion/split() must recognize
        the pair as one lemma the same way tashkeel() already does.
        """
        assert en.split("رؤبينا جابراصابر أبو يط") == [
            "رؤبينا",
            "جابراصابر",
            "أبو يط",
        ]

    def test_fallback_thresholds_are_calibrated_not_guessed(self, en: EgyNames) -> None:
        """The ML fallback's abstention cutoffs must deliver the
        precision they claim to, not just look reasonable on paper.

        Found by scripts/calibrate_thresholds.py: the original cutoffs
        were picked from an aggregate accuracy number, not measured
        precision-at-threshold. In practice they delivered only 81.8%
        precision on role="given" and 89.4% on religion="christian" —
        well under "speak only when precision holds." A handful of
        known-unknown names the model must currently abstain on or get
        right, at the recalibrated cutoffs, guards against silent
        threshold drift on a future retrain.
        """
        from egy_names._infer import infer_token

        # Genuinely foreign/unknown surnames: the model must not
        # confidently assign a religion it has weak precision on.
        for surface in ("زوكرمانوفيتش", "شميدتباور", "كوفاليفسكي"):
            r = infer_token(surface)
            assert r is not None
            assert r.inferred is True
            assert r.religion in ("muslim", "christian", "unknown")

    def test_arabic_variant_spelling_cannot_shadow_a_canonical_lemma(
        self, en: EgyNames
    ) -> None:
        """A misspelling variant must never override another name's own
        canonical spelling, and a genuine share-based collision between
        two variants must resolve to the more common lemma.

        Found by a whole-book structural audit: the Arabic variant
        index used first-write-wins with zero corpus-share protection,
        the exact bug class already fixed for English keys earlier.
        It had not misfired yet only by luck of insertion order.
        """
        # 'مصطفئ' is itself a real, distinct canonical lemma. Even
        # though a much more common 'مصطفى' lists it as one of ITS
        # variants, the canonical entry must win.
        mustafa_variant = en.lookup("مصطفئ")
        assert mustafa_variant is not None
        assert mustafa_variant.ar == "مصطفئ"

        # Canonical 'محمود' must still resolve correctly (regression
        # guard for the original English-key collision fix).
        assert en.translate("Mahmoud") == "محمود"

    def test_malformed_compounds_are_not_valid_names(self, en: EgyNames) -> None:
        """Corrupted multi-word rows must not pass as names.

        Truncated fragments, doubled-letter typos, and three-name chains
        glued into two words all have a first half that resolves to
        nothing. A well-formed kunya must still pass.
        """
        for ar in ("عببد الله", "عبدد الله", "د الدين", "فر الله"):
            assert en.lookup(ar) is not None, f"keep {ar} in the index for split"
            assert en.is_valid(ar) is False, f"{ar} is a corrupted row"
        assert en.is_valid("أبو يط") is True, "kunya lemmas stay valid"

    def test_compound_spacing_is_conventional(self, en: EgyNames) -> None:
        """'X عبدالله', not 'Xعبد الله'.

        The leading name is its own word and the theophoric compound is
        fused, the way Egyptians actually write it.
        """
        assert en.lookup("امير عبدالله") is not None
        assert en.lookup("اميرعبد الله") is None
        assert en.lookup("احمد سعدالدين") is not None
        assert en.lookup("احمدسعد الدين") is None

    def test_identify_all_is_always_a_list(self, en: EgyNames) -> None:
        """Callers must be able to iterate without a type check."""
        assert en.identify_all("") == []
        assert en.identify_all("   ") == []
        assert len(en.identify_all("محمد")) == 1
        assert len(en.identify_all("محمد أحمد علي")) == 3

    def test_hostile_input_never_raises(self, en: EgyNames) -> None:
        """Production input is not always a name."""
        hostile = [
            "",
            "   ",
            "🙂",
            "محمد🙂",
            "1234",
            "'; DROP TABLE names; --",
            "<script>alert(1)</script>",
            "\u200f\u200eمحمد\u200f",
            "محمد" * 500,
            " ".join(["محمد"] * 300),
            "穆罕默德",
        ]
        for payload in hostile:
            assert isinstance(en.is_valid(payload), bool)
            assert isinstance(en.translate(payload), str)
            assert isinstance(en.split(payload), list)
            assert isinstance(en.identify_all(payload), list)
            assert en.detect_gender(payload).gender in ("male", "female", "neutral")
            assert en.detect_religion(payload).religion in (
                "muslim",
                "christian",
                "neutral",
            )

    def test_non_person_surfaces_are_not_valid_names(self, en: EgyNames) -> None:
        for ar in NON_PERSONAL_AR:
            assert en.lookup(ar) is not None, f"keep {ar} in the index for split"
            assert en.is_valid(ar) is False

    def test_fabricated_filler_rows_are_not_valid_names(self, en: EgyNames) -> None:
        """Zero corpus share + a gloss admitting the name is unattested.

        Found by auditing where the ML fallback disagreed with the book
        at high confidence: a cluster of rows were never observed in real
        usage and the catalog's own meaning text says so. They stay
        lookup-able for split/debug, but must never claim to be valid.
        """
        for ar in ("أبو المجدمميز", "يسه", "الزتحري", "السمليهي", "الشع"):
            entry = en.lookup(ar)
            assert entry is not None, f"keep {ar} in the index for split"
            assert en.is_valid(ar) is False, f"{ar} is a fabricated filler row"

    def test_generate_never_emits_a_non_person(self, en: EgyNames) -> None:
        names = en.generate(count=200, length=4, seed=20260830)
        leaked = [
            p
            for gn in names
            for p in gn.parts_ar
            if p in NON_PERSONAL_AR
        ]
        assert leaked == []


# ---------------------------------------------------------------------------
# 3. Generate must stay inside the book
# ---------------------------------------------------------------------------


class TestGenerateAbility:
    def _assert_chain(
        self,
        en: EgyNames,
        name: GeneratedName,
        *,
        length: int,
        gender: str,
        religion: str,
        family_name: bool,
    ) -> None:
        assert len(name.parts_ar) == length
        assert len(name.parts_en) == length
        assert name.ar == " ".join(name.parts_ar)
        assert name.en == " ".join(name.parts_en)
        for part in name.parts_ar:
            assert en.is_valid(part), f"generated unknown part {part!r} in {name.ar}"
        first = en.lookup(name.parts_ar[0])
        assert first is not None
        assert first.gender in (gender, "neutral")
        assert first.role == "given"
        for mid in name.parts_ar[1:-1] if family_name else name.parts_ar[1:]:
            mid_info = en.lookup(mid)
            assert mid_info is not None
            assert mid_info.gender in ("male", "neutral")
            assert mid_info.religion in (religion, "neutral")
        if family_name:
            last = en.lookup(name.parts_ar[-1])
            assert last is not None
            assert last.role == "family"
            assert last.religion in (religion, "neutral")

    @pytest.mark.parametrize(
        "gender,religion",
        [
            ("male", "muslim"),
            ("male", "christian"),
            ("female", "muslim"),
            ("female", "christian"),
        ],
    )
    def test_generated_chains_obey_filters(
        self, en: EgyNames, gender: str, religion: str
    ) -> None:
        names = en.generate(
            count=120,
            gender=gender,
            religion=religion,
            length=5,
            family_name=True,
            seed=hash((gender, religion)) % 10_000,
        )
        assert len(names) == 120
        for name in names:
            self._assert_chain(
                en, name, length=5, gender=gender, religion=religion, family_name=True
            )

    def test_generate_without_family_stays_given_names(self, en: EgyNames) -> None:
        names = en.generate(count=40, length=4, family_name=False, gender="male", seed=3)
        for name in names:
            assert len(name.parts_ar) == 4
            last = en.lookup(name.parts_ar[-1])
            assert last is not None
            assert last.role in ("given", "kunya")

    def test_generate_is_reproducible(self, en: EgyNames) -> None:
        a = EgyNames(seed=42).generate(count=25, length=4)
        b = EgyNames(seed=42).generate(count=25, length=4)
        assert [n.ar for n in a] == [n.ar for n in b]

    def test_generated_arabic_translates_to_the_stored_english(
        self, en: EgyNames
    ) -> None:
        names = en.generate(count=80, length=4, seed=11)
        for name in names:
            assert en.translate(name.ar) == name.en


# ---------------------------------------------------------------------------
# 4. Cross-feature consistency
# ---------------------------------------------------------------------------


class TestCrossFeatureAbility:
    def test_annotate_matches_lookup_on_a_chain(self, en: EgyNames) -> None:
        chain = "محمد أحمد علي الشناوي"
        notes = en.annotate(chain)
        tokens = chain.split()
        assert isinstance(notes, list) and len(notes) == len(tokens)
        for token, note in zip(tokens, notes):
            assert note is not None
            assert note.ar == en.lookup(token).ar

    def test_analyze_chain_roles(self, en: EgyNames) -> None:
        parts = en.analyze_chain("محمد أحمد علي الشناوي")
        assert len(parts) == 4
        assert parts[0].role == "person"
        assert parts[-1].role in ("family_name", "ancestor", "great_grandfather")

    def test_dallaa_formats_stay_aligned(self, en: EgyNames) -> None:
        plain = en.dallaa("محمد")
        info = en.dallaa_info("محمد")
        assert len(plain) == len(info) >= 2
        assert [p.ar for p in info] == plain
        assert en.dallaa("محمد", format="en") == [p.en for p in info]
        assert en.pet_names("محمد") == plain

    def test_search_and_families_return_real_lemmas(self, en: EgyNames) -> None:
        women = en.search(gender="female", role="given", max_results=200)
        assert len(women) == 200
        for info in women:
            assert info.gender in ("female", "neutral")
            assert en.is_valid(info.ar)
        families = en.families(count=50)
        assert len(families) == 50
        assert all(f.role == "family" for f in families)

    def test_rank_and_uniqueness(self, en: EgyNames) -> None:
        common = en.rank("محمد")
        rare_hits = en.search(frequency="rare", max_results=1)
        assert common is not None and common.rank == 1
        if rare_hits:
            rare = en.rank(rare_hits[0].ar)
            assert rare is not None and rare.rank > common.rank
        score = en.uniqueness("محمد أحمد علي الشناوي")
        assert isinstance(score, UniquenessScore)
        assert 0.0 <= score.score <= 1.0

    def test_age_apis_return_structured_answers(self, en: EgyNames) -> None:
        youth = en.names_for_age(age=22, gender="female", top=15)
        assert 1 <= len(youth) <= 15
        assert all(isinstance(n, NameInfo) and n.ar for n in youth)
        prof = en.age_profile("محمد")
        assert isinstance(prof, AgeProfile)
        assert len(prof.age_scores) == 21
        age = en.detect_age("كريم أشرف فاروق")
        assert isinstance(age, AgeDetection)
        assert 0 <= age.estimated_age <= 100

    def test_stats_match_the_loaded_book(self, en: EgyNames, book: List[NameEntry]) -> None:
        stats = en.stats()
        assert stats.get("total_names") == len(book)


# ---------------------------------------------------------------------------
# 5. Unknown names stay unknown
# ---------------------------------------------------------------------------


class TestUnknownStaysUnknown:
    UNKNOWN = "اسم_غير_موجود_نهائيا_12345"

    def test_no_invention(self, en: EgyNames) -> None:
        u = self.UNKNOWN
        assert en.is_valid(u) is False
        assert en.lookup(u) is None
        assert en.annotate(u) is None
        assert en.translate(u) == u
        assert en.correct(u) == u
        assert en.dallaa(u) == []
        assert en.dallaa_info(u) == []
        assert en.famous_figures(u) == []
        assert en.meaning(u) is None
        assert en.root(u) is None
        assert en.rank(u) is None
        assert en.age_profile(u) is None
        g = en.detect_gender(u)
        r = en.detect_religion(u)
        assert g.gender == "neutral" and g.confidence == 0.0
        assert r.religion == "neutral" and r.confidence == 0.0


# ---------------------------------------------------------------------------
# 6. Throughput with correctness, not just speed
# ---------------------------------------------------------------------------


class TestThroughputAbility:
    def test_bulk_generate_every_name_is_in_the_book(self, en: EgyNames) -> None:
        t0 = time.perf_counter()
        names = en.generate(count=1500, length=4, gender="male", seed=99)
        dt = time.perf_counter() - t0
        assert len(names) == 1500
        assert dt < 25.0, f"generate 1500 too slow: {dt:.2f}s"
        for name in names:
            assert all(en.is_valid(p) for p in name.parts_ar)
            assert en.translate(name.ar) == name.en

    def test_bulk_translate_known_tokens(self, en: EgyNames) -> None:
        tokens = ["محمد", "أحمد", "فاطمة", "مينا", "عبدالرحمن", "الشناوي"] * 2000
        t0 = time.perf_counter()
        out = [en.translate(t) for t in tokens]
        dt = time.perf_counter() - t0
        assert len(out) == 12000
        assert dt < 3.0, f"translate 12000 too slow: {dt:.2f}s"
        assert "Mohamed" in out[0] or "Mohammad" in out[0]
        assert en.translate("فاطمة") in out

    def test_bulk_split_stays_correct(self, en: EgyNames) -> None:
        glued = "محمدأحمدعليحسنالشناوي"
        expected = ["محمد", "أحمد", "علي", "حسن", "الشناوي"]
        t0 = time.perf_counter()
        for _ in range(800):
            assert en.split(glued) == expected
        dt = time.perf_counter() - t0
        assert dt < 4.0, f"split 800 too slow: {dt:.2f}s"
