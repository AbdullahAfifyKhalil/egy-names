import time, sys, os, traceback, gc

sys.path.insert(0, "/Volumes/MAC/Development/Personal/Egyptian Names/library building/python/src")
from egy_names import EgyNames, NameInfo, PetName
from egy_names._index import get_all

en = EgyNames()
all_entries = get_all()
print(f"Total names in memory: {len(all_entries)}")

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
    assert_eq(en.meaning(""), None)
run_test("1.1 Empty string input across all core APIs", test_1_1)

def test_1_2():
    assert_eq(en.translate("   \t\n   "), "")
    assert_eq(en.tashkeel("   \t\n   "), "")
    assert_eq(en.tashkeel_eg("   \t\n   "), "")
    assert_eq(en.ipa_eg("   \t\n   "), "")
    assert_eq(en.ipa_standard("   \t\n   "), "")
    assert_eq(en.correct("   \t\n   "), "")
    assert_eq(en.split("   \t\n   "), [])
    assert_eq(en.dallaa("   \t\n   "), [])
    assert_eq(en.famous_figures("   \t\n   "), [])
run_test("1.2 Whitespace-only input (spaces, tabs, newlines)", test_1_2)

def test_1_3():
    assert_eq(len(en.generate(count=0)), 0)
    assert_eq(len(en.generate(count=1)), 1)
    assert_eq(len(en.generate(count=100)), 100)
    assert_eq(len(en.search(prefix="zzzzzzzz_non_existent")), 0)
run_test("1.3 Generation bounds and empty search returns", test_1_3)

print("\n=======================================================")
print("SUITE 2: MALICIOUS, SPECIAL CHARS & NOISE INJECTION")
print("=======================================================")

def test_2_1():
    en.translate("'; DROP TABLE names; -- <script>alert(1)</script>")
    en.tashkeel("'; DROP TABLE names; --")
    en.correct("'; DROP TABLE names; --")
    en.split("'; DROP TABLE names; --")
    en.search(prefix="'; DROP TABLE")
run_test("2.1 SQL Injection / Script payload injection safety", test_2_1)

def test_2_2():
    en.translate("\u200b\u200c\u200d\ufeff\u200e\u200fمحمد\u200b")
    en.tashkeel("محمد 😊 🔥 🎉")
    en.correct("احمد 👍")
    en.split("محمد🎉أحمد🔥علي")
run_test("2.2 Unicode Control Characters, Zero-Width & Emojis", test_2_2)

def test_2_3():
    en.translate("محــــــــــــــمد")
    en.tashkeel("محــــــــــــــمد")
    en.correct("محــــــــــــــمد")
    en.translate("محمممممممد")
    en.split("محمممممد")
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
    assert_eq(en.dallaa("اسم_غير_موجود_نهائيا_12345"), [])
    assert_eq(en.dallaa_info("اسم_غير_موجود_نهائيا_12345"), [])
    assert_eq(en.famous_figures("اسم_غير_موجود_نهائيا_12345"), [])
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
    assert 10 <= age_det.estimated_age <= 50, f"Unexpected age estimation: {age_det}"
    print(f"      'كريم أشرف فاروق' -> Age ~{age_det.estimated_age} ({age_det.age_range}) | Conf: {age_det.confidence} | {age_det.generation_label}")
run_test("7.3 Generational Age Intelligence estimation", test_7_3)

print("\n=======================================================")
print("SUITE 8: HIGH-THROUGHPUT STRESS TEST & BENCHMARK")
print("=======================================================")

def test_8_1():
    t0 = time.perf_counter()
    names = en.generate(count=10000, length=4)
    dt = time.perf_counter() - t0
    assert len(names) == 10000, f"Expected 10,000 names, got {len(names)}"
    print(f"      Generated 10,000 names in {dt:.3f}s ({10000/dt:.0f} names/sec)")
run_test("8.1 Generate 10,000 patronymic names in bulk", test_8_1)

def test_8_2():
    sample_names = ["محمد", "أحمد", "فاطمة", "الشناوي", "عبد الرحمن", "مهرائيل", "جرجس", "بوادقجي"] * 6250
    t0 = time.perf_counter()
    for name in sample_names:
        en.translate(name)
    dt = time.perf_counter() - t0
    print(f"      Transliterated 50,000 tokens in {dt:.3f}s ({50000/dt:.0f} lookups/sec)")
run_test("8.2 Transliterate 50,000 tokens", test_8_2)

def test_8_3():
    test_str = "محمدأحمدعليحسنالشناوي"
    t0 = time.perf_counter()
    for _ in range(5000):
        en.split(test_str)
    dt = time.perf_counter() - t0
    print(f"      Split 5,000 unspaced chains in {dt:.3f}s ({5000/dt:.0f} splits/sec)")
run_test("8.3 DP Split 5,000 concatenated strings", test_8_3)

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
else:
    print("\nALL STRESS AND ADVERSARIAL EDGE-CASE TESTS PASSED WITH 100% SUCCESS!")
