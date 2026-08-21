import { EgyptianNames, PetName, Gender, Religion } from '../src/index';

const en = new EgyptianNames();
console.log("Initialized TypeScript EgyNames successfully.");

let passed = 0;
let failed = 0;

function runTest(name: string, fn: () => void) {
  const t0 = performance.now();
  try {
    fn();
    const dt = (performance.now() - t0).toFixed(2);
    console.log(`  [PASS] ${name} (${dt}ms)`);
    passed++;
  } catch (err: any) {
    const dt = (performance.now() - t0).toFixed(2);
    console.error(`  [FAIL] ${name} (${dt}ms) -> ${err.message || err}`);
    failed++;
  }
}

function assertEq<T>(actual: T, expected: T, msg?: string) {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`${msg || 'Assertion failed'}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

console.log("\n=======================================================");
console.log("SUITE 1: NULL, EMPTY, WHITESPACE & TYPE SAFETY");
console.log("=======================================================");

runTest("1.1 Empty string input across all APIs", () => {
  assertEq(en.translate(""), "");
  assertEq(en.tashkeel(""), "");
  assertEq(en.tashkeelEg(""), "");
  assertEq(en.ipaEg(""), "");
  assertEq(en.ipaStandard(""), "");
  assertEq(en.correct(""), "");
  assertEq(en.split(""), []);
  assertEq(en.dallaa(""), []);
  assertEq(en.famousFigures(""), []);
});

runTest("1.2 Whitespace-only input (spaces, tabs, newlines)", () => {
  assertEq(en.translate("   \t\n   "), "");
  assertEq(en.tashkeel("   \t\n   "), "");
  assertEq(en.correct("   \t\n   "), "");
  assertEq(en.split("   \t\n   "), []);
});

runTest("1.3 Generation bounds and empty search returns", () => {
  assertEq(en.generate({ count: 0 }).length, 0);
  assertEq(en.generate({ count: 1 }).length, 1);
  assertEq(en.generate({ count: 100 }).length, 100);
  assertEq(en.search({ prefix: "zzzzzzzz_non_existent" }).length, 0);
});

console.log("\n=======================================================");
console.log("SUITE 2: MALICIOUS, SPECIAL CHARS & NOISE INJECTION");
console.log("=======================================================");

runTest("2.1 SQL Injection / Script payload injection safety", () => {
  en.translate("'; DROP TABLE names; -- <script>alert(1)</script>");
  en.tashkeel("'; DROP TABLE names; --");
  en.correct("'; DROP TABLE names; --");
  en.split("'; DROP TABLE names; --");
  en.search({ prefix: "'; DROP TABLE" });
});

runTest("2.2 Unicode Control Characters, Zero-Width & Emojis", () => {
  en.translate("\u200b\u200c\u200d\ufeff\u200e\u200fمحمد\u200b");
  en.tashkeel("محمد 😊 🔥 🎉");
  en.correct("احمد 👍");
  en.split("محمد🎉أحمد🔥علي");
});

console.log("\n=======================================================");
console.log("SUITE 3: DYNAMIC PROGRAMMING SPLITTING ADVERSARIAL CASES");
console.log("=======================================================")

runTest("3.1 Highly concatenated multi-token chains (6+ tokens)", () => {
  const res = en.split("محمدأحمدعليحسنمحمودالشناوي");
  if (res.length < 5) throw new Error(`Expected >= 5 tokens, got ${JSON.stringify(res)}`);
  console.log(`      'محمدأحمدعليحسنمحمودالشناوي' -> ${JSON.stringify(res)}`);
});

runTest("3.2 Chained compound names", () => {
  const res = en.split("عبدالرحمنعبداللهعبدالعزيزنورالدينفاطمةالزهراء");
  console.log(`      Multiple unspaced compounds -> ${JSON.stringify(res)}`);
  if (res.length < 4) throw new Error(`Failed: ${JSON.stringify(res)}`);
});

console.log("\n=======================================================");
console.log("SUITE 4: DETERMINISTIC SPELLING & ORTHOGRAPHY CORRECTIONS");
console.log("=======================================================");

runTest("4.1 Classic Alif Maqsura vs Ya edge cases", () => {
  assertEq(en.correct("مصطفا"), "مصطفى");
  assertEq(en.correct("يحي"), "يحيى");
  assertEq(en.correct("مني"), "منى");
});

runTest("4.2 Compound Spacing Normalization", () => {
  const c1 = en.correct("عبدالرحمن");
  if (!["عبدالرحمن", "عبد الرحمن"].includes(c1)) throw new Error(`Unexpected: ${c1}`);
  const c2 = en.correct("عبدالله");
  if (!["عبدالله", "عبد الله"].includes(c2)) throw new Error(`Unexpected: ${c2}`);
});

console.log("\n=======================================================");
console.log("SUITE 5: PET NAMES & PUBLIC FIGURES 14D ENGINE");
console.log("=======================================================");

runTest("5.1 Pet Names multi-format extraction", () => {
  const plain = en.dallaa("محمد", "plain");
  const tash = en.dallaa("محمد", "tashkeel");
  const ipa = en.dallaa("محمد", "ipa");
  const info = en.dallaaInfo("محمد");
  if (plain.length < 3) throw new Error(`Expected pet names, got ${plain}`);
  if (tash.length < 3) throw new Error(`Expected tashkeel pet names, got ${tash}`);
  if (ipa.length < 3) throw new Error(`Expected ipa pet names, got ${ipa}`);
  if (info.length < 3) throw new Error(`Expected PetName objects, got ${info.length}`);
  console.log(`      'محمد' Pet Names: ${info.map(p => `${p.ar} (${p.tashkeel}) [${p.ipa}]`).join(', ')}`);
});

runTest("5.2 Famous Figures bilingual extraction & filtering", () => {
  const arFigs = en.famousFigures("محمد", "ar");
  const enFigs = en.famousFigures("محمد", "en");
  if (arFigs.length < 1) throw new Error(`Expected AR figures, got ${arFigs}`);
  if (enFigs.length < 1) throw new Error(`Expected EN figures, got ${enFigs}`);
  console.log(`      'محمد' Figures (EN): ${enFigs.slice(0, 2).join(' | ')}`);
});

console.log("\n=======================================================");
console.log("SUITE 6: HIGH-THROUGHPUT STRESS TEST & BENCHMARK");
console.log("=======================================================");

runTest("6.1 Generate 10,000 patronymic names in bulk", () => {
  const t0 = performance.now();
  const names = en.generate({ count: 10000, length: 4 });
  const dt = (performance.now() - t0) / 1000;
  if (names.length !== 10000) throw new Error(`Expected 10,000 names, got ${names.length}`);
  console.log(`      Generated 10,000 names in ${dt.toFixed(3)}s (${(10000 / dt).toFixed(0)} names/sec)`);
});

runTest("6.2 Transliterate 50,000 tokens", () => {
  const sampleNames = ["محمد", "أحمد", "فاطمة", "الشناوي", "عبد الرحمن", "مهرائيل", "جرجس", "بوادقجي"];
  const t0 = performance.now();
  for (let i = 0; i < 50000; i++) {
    en.translate(sampleNames[i % sampleNames.length]);
  }
  const dt = (performance.now() - t0) / 1000;
  console.log(`      Transliterated 50,000 tokens in ${dt.toFixed(3)}s (${(50000 / dt).toFixed(0)} lookups/sec)`);
});

console.log("\n=======================================================");
console.log("SUMMARY REPORT");
console.log("=======================================================");
console.log(`Total Tests Run: ${passed + failed} | Passed: ${passed} | Failed: ${failed}`);
if (failed > 0) {
  process.exit(1);
} else {
  console.log("\nALL TYPESCRIPT STRESS AND ADVERSARIAL TESTS PASSED WITH 100% SUCCESS!");
}
