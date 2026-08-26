"""
egy-names v0.3.2 — Adversarial Stress & Edge-Case Suite

Portable runner for the published GitHub repo. Exercises empty/malicious
input, DP splitting, 14D lookup, age intelligence, and high-throughput
paths without depending on a machine-specific install.
"""

import os
import sys
import time
import traceback

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "python", "src"))

from egy_names import (  # noqa: E402
    AgeDetection,
    AgeProfile,
    EgyNames,
    GeneratedName,
    NameInfo,
    PetName,
    __version__,
)
from egy_names._index import get_all  # noqa: E402

en = EgyNames()
all_entries = get_all()
print(f"egy-names {__version__}  |  Total names in memory: {len(all_entries)}")

test_results = []


def run_test(test_name, fn):
    t0 = time.perf_counter()
    try:
        fn()
        dt = (time.perf_counter() - t0) * 1000
        test_results.append((test_name, "PASS", f"{dt:.2f}ms", ""))
        print(f"  [PASS] {test_name} ({dt:.2f}ms)")
    except Exception as e:
        dt = (time.perf_counter() - t0) * 1000
        err = f"{type(e).__name__}: {str(e)}"
        test_results.append((test_name, "FAIL", f"{dt:.2f}ms", err))
        print(f"  [FAIL] {test_name} ({dt:.2f}ms) -> {err}")
        traceback.print_exc()


def assert_eq(a, b):
    assert a == b, f"Expected {b!r}, got {a!r}"


print("\n=======================================================")
print("SUITE 1: NULL, EMPTY, WHITESPACE & TYPE SAFETY")
print("=======================================================")


def test_1_1():
    assert_eq(en.translate(""), "")
    assert_eq(en.tashkeel(""), "")
    assert_eq(en.tashkeel_eg(""), "")
    assert_eq(en.ipa_eg(""), "")
    assert_eq(en.ipa_standard(""), "")
    assert_eq(en.correct(""), "")
    assert_eq(en.split(""), [])
    assert_eq(en.dallaa(""), [])
    assert_eq(en.famous_figures(""), [])
    assert_eq(en.info(""), None)
    assert_eq(en.lookup(""), None)
    assert_eq(en.meaning(""), None)
    assert_eq(en.root(""), None)
    assert_eq(en.origin(""), None)
    assert_eq(en.trend(""), None)
    assert_eq(en.rank(""), None)
    assert_eq(en.age_profile(""), None)
    assert_eq(en.detect_age(""), None)
    assert_eq(en.analyze_chain(""), [])
    assert en.is_valid("") is False
run_test("1.1 Empty string input across all core APIs", test_1_1)


def test_1_2():
    ws = "   \t\n   "
    assert_eq(en.translate(ws), "")
    assert_eq(en.tashkeel(ws), "")
    assert_eq(en.tashkeel_eg(ws), "")
    assert_eq(en.ipa_eg(ws), "")
    assert_eq(en.ipa_standard(ws), "")
    assert_eq(en.correct(ws), "")
    assert_eq(en.split(ws), [])
    assert_eq(en.dallaa(ws), [])
    assert_eq(en.famous_figures(ws), [])
    assert_eq(en.analyze_chain(ws), [])
    assert en.detect_age(ws) is None
run_test("1.2 Whitespace-only input (spaces, tabs, newlines)", test_1_2)


def test_1_3():
    assert_eq(len(en.generate(count=0)), 0)
    assert_eq(len(en.generate(count=1)), 1)
    assert_eq(len(en.generate(count=100)), 100)
    assert isinstance(en.generate(count=1, seed=7)[0], GeneratedName)
    assert_eq(len(en.search(prefix="zzzzzzzz_non_existent")), 0)
run_test("1.3 Generation bounds and empty search returns", test_1_3)


print("\n=======================================================")
print("SUITE 2: MALICIOUS, SPECIAL CHARS & NOISE INJECTION")
print("=======================================================")


def test_2_1():
    payload = "'; DROP TABLE names; -- <script>alert(1)</script>"
    en.translate(payload)
    en.tashkeel("'; DROP TABLE names; --")
    en.correct("'; DROP TABLE names; --")
    en.split("'; DROP TABLE names; --")
    en.search(prefix="'; DROP TABLE")
    en.lookup(payload)
    en.annotate(payload)
    en.detect_age(payload)
run_test("2.1 SQL Injection / Script payload injection safety", test_2_1)


def test_2_2():
    en.translate("\u200b\u200c\u200d\ufeff\u200e\u200fمحمد\u200b")
    en.tashkeel("محمد 😊 🔥 🎉")
    en.correct("احمد 👍")
    en.split("محمد🎉أحمد🔥علي")
    en.lookup("م\u200Cح\u200Dم\uFEFFد")
    en.annotate("محمد 🔥 أحمد")
run_test("2.2 Unicode Control Characters, Zero-Width & Emojis", test_2_2)


def test_2_3():
    en.translate("محــــــــــــــمد")
    en.tashkeel("محــــــــــــــمد")
    en.correct("محــــــــــــــمد")
    en.translate("محمممممممد")
    en.split("محمممممد")
    assert en.correct("مــــحــــمـــــد") == "محمد"
run_test("2.3 Excessive Arabic Tatweel (Kashida) & Repeated Characters", test_2_3)


print("\n=======================================================")
print("SUITE 3: DYNAMIC PROGRAMMING SPLITTING ADVERSARIAL CASES")
print("=======================================================")


def test_3_1():
    res = en.split("محمدأحمدعليحسنمحمودالشناوي")
    assert len(res) >= 5, f"Expected >= 5 tokens, got {res}"
    print(f"      'محمدأحمدعليحسنمحمودالشناوي' -> {res}")
run_test("3.1 Highly concatenated multi-token chains (6+ tokens)", test_3_1)


def test_3_2():
    res = en.split("عبدالرحمنعبداللهعبدالعزيزنورالدينفاطمةالزهراء")
    print(f"      Multiple unspaced compounds -> {res}")
    assert len(res) >= 4, f"Failed: {res}"
run_test("3.2 Chained compound names (Abdel- + Nour- + Abou- + Fatma-)", test_3_2)


def test_3_3():
    res = en.split("محمد123أحمد_Ali_علي")
    print(f"      Mixed script unspaced -> {res}")
    assert len(res) >= 2, f"Failed: {res}"
run_test("3.3 Unspaced name with embedded English and numeric noise", test_3_3)


def test_3_4():
    res = en.split("مي")
    assert len(res) == 1 and res[0] == "مي", f"Failed: {res}"
run_test("3.4 Single letter and 2-letter ambiguous sub-strings", test_3_4)


print("\n=======================================================")
print("SUITE 4: DETERMINISTIC SPELLING & ORTHOGRAPHY CORRECTIONS")
print("=======================================================")


def test_4_1():
    assert_eq(en.correct("مصطفا"), "مصطفى")
    assert_eq(en.correct("يحي"), "يحيى")
    assert_eq(en.correct("ابراهم"), "إبراهيم")
    assert_eq(en.correct("اسماعيل"), "إسماعيل")
run_test("4.1 Classic Alif Maqsura & Hamza normalization", test_4_1)


def test_4_2():
    c1 = en.correct("عبدالرحمن")
    assert c1 in ["عبدالرحمن", "عبد الرحمن"], f"Unexpected: {c1}"
    c2 = en.correct("عبدالله")
    assert c2 in ["عبدالله", "عبد الله"], f"Unexpected: {c2}"
    c3 = en.correct("عبدالعزيز")
    assert c3 in ["عبدالعزيز", "عبد العزيز"], f"Unexpected: {c3}"
run_test("4.2 Compound Spacing Normalization", test_4_2)


def test_4_3():
    raw = "  احمد  ,  مصطفا  ;  عبدالرحمن   يحي  ! "
    cleaned = en.correct(raw)
    print(f"      Raw: '{raw}' -> Cleaned: '{cleaned}'")
    assert "أحمد" in cleaned and "مصطفى" in cleaned and "يحيى" in cleaned
run_test("4.3 Complex multi-token string with mixed punctuation & typos", test_4_3)


print("\n=======================================================")
print("SUITE 5: PET NAMES & PUBLIC FIGURES 14D ENGINE")
print("=======================================================")


def test_5_1():
    plain = en.dallaa("محمد", format="plain")
    assert len(plain) >= 3, f"Expected pet names for محمد, got {plain}"
    tash = en.dallaa("محمد", format="tashkeel")
    assert len(tash) >= 3, f"Expected tashkeel pet names, got {tash}"
    ipa = en.dallaa("محمد", format="ipa")
    assert len(ipa) >= 3, f"Expected ipa pet names, got {ipa}"
    info = en.dallaa_info("محمد")
    assert len(info) >= 3, f"Expected PetName objects, got {info}"
    assert isinstance(info[0], PetName), f"Expected PetName instance, got {type(info[0])}"
    assert en.pet_names("محمد") == plain
    print(f"      'محمد' Pet Names: {[f'{p.ar} ({p.tashkeel}) [{p.ipa}]' for p in info]}")
run_test("5.1 Pet Names multi-format extraction", test_5_1)


def test_5_2():
    ar_figs = en.famous_figures("محمد", lang="ar")
    en_figs = en.famous_figures("محمد", lang="en")
    all_figs = en.famous_figures("محمد", lang="all")
    assert len(ar_figs) >= 1, f"Expected AR figures for محمد, got {ar_figs}"
    assert len(en_figs) >= 1, f"Expected EN figures for محمد, got {en_figs}"
    assert len(all_figs) >= len(ar_figs), f"Expected all figures >= AR figures"
    print(f"      'محمد' Figures (EN): {en_figs[:2]}")
run_test("5.2 Famous Figures bilingual extraction & filtering", test_5_2)


def test_5_3():
    unknown = "اسم_غير_موجود_نهائيا_12345"
    assert_eq(en.dallaa(unknown), [])
    assert_eq(en.dallaa_info(unknown), [])
    assert_eq(en.famous_figures(unknown), [])
    assert_eq(en.meaning(unknown), None)
    assert_eq(en.root(unknown), None)
    assert en.is_valid(unknown) is False
run_test("5.3 Unknown name Pet Names & Figures handling", test_5_3)


print("\n=======================================================")
print("SUITE 6: DUAL TASHKEEL & IPA PHONETICS")
print("=======================================================")


def test_6_1():
    std = en.tashkeel_standard("محمد")
    eg = en.tashkeel_eg("محمد")
    assert std != "", "Expected standard tashkeel for محمد"
    assert eg != "", "Expected egyptian tashkeel for محمد"
    print(f"      'محمد' Standard: '{std}' | Egyptian: '{eg}'")
run_test("6.1 Standard vs Egyptian Tashkeel comparison", test_6_1)


def test_6_2():
    std_ipa = en.ipa_standard("جمال")
    eg_ipa = en.ipa_eg("جمال")
    assert "ɡ" in eg_ipa or "g" in eg_ipa, f"Egyptian IPA should have [ɡ], got {eg_ipa}"
    print(f"      'جمال' Standard IPA: '{std_ipa}' | Egyptian IPA: '{eg_ipa}'")
run_test("6.2 Standard vs Egyptian IPA transcription", test_6_2)


def test_6_3():
    chain = "محمد أحمد علي حسن الشناوي"
    chain_tash = en.tashkeel(chain)
    chain_ipa = en.ipa_eg(chain)
    assert len(chain_tash.split()) == 5, f"Expected 5 vocalized words, got '{chain_tash}'"
    print(f"      Full chain Tashkeel: '{chain_tash}'")
    print(f"      Full chain Egyptian IPA: '{chain_ipa}'")
run_test("6.3 Multi-token sentence Tashkeel and IPA", test_6_3)


print("\n=======================================================")
print("SUITE 7: DEMOGRAPHIC INFERENCES & GENERATIONAL AGE")
print("=======================================================")


def test_7_1():
    g_female = en.detect_gender("فاطمة الزهراء")
    assert g_female.gender == "female" and g_female.confidence > 0.8, f"Failed female: {g_female}"
    g_male = en.detect_gender("محمد أحمد علي")
    assert g_male.gender == "male" and g_male.confidence > 0.8, f"Failed male: {g_male}"
    print(f"      'فاطمة الزهراء' -> {g_female}")
    print(f"      'محمد أحمد علي' -> {g_male}")
run_test("7.1 Gender inference on distinct and compound names", test_7_1)


def test_7_2():
    r_c = en.detect_religion("مينا جرجس بطرس شنودة")
    assert r_c.religion == "christian" and r_c.confidence > 0.9, f"Failed christian: {r_c}"
    r_m = en.detect_religion("محمد أحمد عبد الرحمن")
    assert r_m.religion == "muslim" and r_m.confidence > 0.9, f"Failed muslim: {r_m}"
    r_n = en.detect_religion("إبراهيم يوسف سمير")
    print(f"      Christian chain: {r_c}")
    print(f"      Muslim chain: {r_m}")
    print(f"      Neutral chain: {r_n}")
run_test("7.2 Religion inference on Christian, Muslim & Neutral patronymics", test_7_2)


def test_7_3():
    age_det = en.detect_age("كريم أشرف فاروق")
    assert isinstance(age_det, AgeDetection), f"Expected AgeDetection, got {type(age_det)}"
    assert 10 <= age_det.estimated_age <= 50, f"Unexpected age estimation: {age_det}"
    print(f"      'كريم أشرف فاروق' -> Age ~{age_det.estimated_age} ({age_det.age_range}) | Conf: {age_det.confidence} | {age_det.generation_label}")
run_test("7.3 Generational Age Intelligence estimation", test_7_3)


print("\n=======================================================")
print("SUITE 8: 14D LOOKUP, ANNOTATION, RANK & CHAIN ANALYSIS")
print("=======================================================")


def test_8_1():
    info = en.info("محمد")
    lookup = en.lookup("محمد")
    assert isinstance(info, NameInfo) and isinstance(lookup, NameInfo)
    assert info.ar == lookup.ar == "محمد"
    assert "Mohamed" in info.en or "Mohammad" in info.en
    en_info = en.lookup("Mohamed")
    assert en_info is not None and en_info.ar == "محمد"
    assert en.is_valid("محمد") is True
    assert en.is_valid("فاطمة") is True
    annot_one = en.annotate("محمد")
    assert isinstance(annot_one, NameInfo)
    annot_chain = en.annotate("محمد أحمد")
    assert isinstance(annot_chain, list) and len(annot_chain) >= 2
run_test("8.1 Lookup, info, is_valid, and annotate (single + chain)", test_8_1)


def test_8_2():
    meaning = en.meaning("محمد")
    assert meaning is not None and meaning["ar"] and meaning["en"]
    root = en.root("محمد")
    assert root is not None and root != "N/A"
    origin = en.origin("محمد")
    assert origin is not None
    trend = en.trend("محمد")
    assert trend in ("classic_timeless", "rising_modern", "vintage_heritage", "rare_toponymic")
    print(f"      meaning/root/origin/trend -> {meaning['en'][:60]} | {root} | {origin} | {trend}")
run_test("8.2 Meaning, morphological root, origin, and trend", test_8_2)


def test_8_3():
    rank = en.rank("محمد")
    assert rank is not None and rank.rank >= 1
    chain = en.analyze_chain("محمد أحمد علي الشناوي")
    assert len(chain) == 4, f"Expected 4 chain parts, got {chain}"
    assert chain[0].role == "person"
    assert chain[-1].role in ("family_name", "ancestor", "great_grandfather")
    score = en.uniqueness("محمد أحمد علي الشناوي")
    assert 0.0 <= score.score <= 1.0
    families = en.families(count=10)
    assert len(families) == 10
    assert all(isinstance(f, NameInfo) for f in families)
    stats = en.stats()
    assert stats.get("total_names", 0) >= 44000
    print(f"      rank=#{rank.rank} uniqueness={score.score} ({score.label}) families={len(families)}")
run_test("8.3 Rank, analyze_chain, uniqueness, families, and stats", test_8_3)


print("\n=======================================================")
print("SUITE 9: AGE-AWARE GENERATION & PROFILE BOUNDARIES")
print("=======================================================")


def test_9_1():
    for age in (0, 1, 15, 24, 50, 75, 99, 100, -5, 150):
        res = en.names_for_age(age=age, top=10)
        assert isinstance(res, list) and len(res) <= 10
        for item in res:
            assert isinstance(item, NameInfo) and item.ar and item.en
    youth = en.names_for_age(age=25, gender="m", top=5)
    assert len(youth) <= 5
    print(f"      names_for_age(25, male) -> {[n.ar for n in youth]}")
run_test("9.1 names_for_age boundary ages and gender filters", test_9_1)


def test_9_2():
    prof = en.age_profile("محمد")
    assert isinstance(prof, AgeProfile)
    assert len(prof.age_scores) == 21
    assert prof.generation_label in (
        "youth", "parent", "grandparent", "great-grandparent", "timeless", "unknown"
    )
    single = en.detect_age("كريم")
    chain = en.detect_age("كريم أشرف فاروق")
    assert isinstance(single, AgeDetection) and isinstance(chain, AgeDetection)
    assert 0.0 <= chain.confidence <= 1.0
    print(f"      age_profile('محمد') -> {prof.generation_label} {prof.peak_age_range}")
run_test("9.2 age_profile completeness and chain corroboration", test_9_2)


print("\n=======================================================")
print("SUITE 10: HIGH-THROUGHPUT STRESS TEST & BENCHMARK")
print("=======================================================")


def test_10_1():
    t0 = time.perf_counter()
    names = en.generate(count=10000, length=4)
    dt = time.perf_counter() - t0
    assert len(names) == 10000, f"Expected 10,000 names, got {len(names)}"
    print(f"      Generated 10,000 names in {dt:.3f}s ({10000/dt:.0f} names/sec)")
run_test("10.1 Generate 10,000 patronymic names in bulk", test_10_1)


def test_10_2():
    sample_names = ["محمد", "أحمد", "فاطمة", "الشناوي", "عبد الرحمن", "مهرائيل", "جرجس", "بوادقجي"] * 6250
    t0 = time.perf_counter()
    for name in sample_names:
        en.translate(name)
    dt = time.perf_counter() - t0
    print(f"      Transliterated 50,000 tokens in {dt:.3f}s ({50000/dt:.0f} lookups/sec)")
run_test("10.2 Transliterate 50,000 tokens", test_10_2)


def test_10_3():
    test_str = "محمدأحمدعليحسنالشناوي"
    t0 = time.perf_counter()
    for _ in range(5000):
        en.split(test_str)
    dt = time.perf_counter() - t0
    print(f"      Split 5,000 unspaced chains in {dt:.3f}s ({5000/dt:.0f} splits/sec)")
run_test("10.3 DP Split 5,000 concatenated strings", test_10_3)


print("\n=======================================================")
print("SUMMARY REPORT")
print("=======================================================")
passed = sum(1 for _, status, _, _ in test_results if status == "PASS")
failed = sum(1 for _, status, _, _ in test_results if status == "FAIL")
print(f"Total Tests Run: {len(test_results)} | Passed: {passed} | Failed: {failed}")

if failed > 0:
    print("\nFAILURES:")
    for name, status, dt, err in test_results:
        if status == "FAIL":
            print(f"  - {name}: {err}")
    sys.exit(1)

print("\nALL STRESS AND ADVERSARIAL EDGE-CASE TESTS PASSED WITH 100% SUCCESS!")
