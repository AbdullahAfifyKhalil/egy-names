/**
 * egy-names v0.3.2 — TypeScript / JavaScript showcase.
 */
import { EgyNames } from "egy-names";

const en = new EgyNames();

console.log("=".repeat(60));
console.log(" Egyptian Names (egy-names) v0.3.2 — TypeScript Showcase");
console.log("=".repeat(60));

console.log("\n1. Name Generation:");
for (const n of en.generate({ count: 3, length: 4, gender: "female", religion: "muslim" })) {
  console.log(`   ${n.ar}  (${n.en})`);
}

console.log("\n2. Transliteration:");
console.log(`   'محمد أحمد علي الشناوي' -> ${en.translate("محمد أحمد علي الشناوي")}`);

console.log("\n3. Orthographic Correction:");
console.log(`   'احمد مصطفا عبد الرحيم' -> ${en.correct("احمد مصطفا عبد الرحيم")}`);

console.log("\n4. Dual Tashkeel & IPA:");
console.log(`   Standard: ${en.tashkeelStandard("محمد عبدالرحمن")}`);
console.log(`   Egyptian: ${en.tashkeelEg("محمد عبدالرحمن")}`);
console.log(`   IPA std:  ${en.ipaStandard("جمال")}`);
console.log(`   IPA eg:   ${en.ipaEg("جمال")}`);

console.log("\n5. Splitting concatenated names:");
console.log(`   ${JSON.stringify(en.split("محمدأحمدعليحسنالشناوي"))}`);

console.log("\n6. Pet names & famous figures:");
console.log(`   dallaa: ${JSON.stringify(en.dallaa("محمد", "tashkeel"))}`);
console.log(`   figures: ${en.famousFigures("محمد", "en").slice(0, 2).join(" | ")}`);

console.log("\n7. 14D lookup:");
const info = en.info("محمد");
console.log(`   ${info?.ar} / ${info?.en} | root=${en.root("محمد")} | origin=${en.origin("محمد")} | trend=${en.trend("محمد")}`);
console.log(`   meaning: ${en.meaning("محمد")?.en}`);

console.log("\n8. Demographics:");
console.log("  ", en.detectGender("فاطمة الزهراء"));
console.log("  ", en.detectReligion("مينا جرجس بطرس"));

console.log("\n9. Chain analysis, rank, uniqueness:");
for (const p of en.analyzeChain("محمد أحمد علي الشناوي")) {
  console.log(`   Slot ${p.slot}: ${p.name} — ${p.role}`);
}
const rank = en.rank("محمد");
const uniq = en.uniqueness("محمد أحمد علي الشناوي");
console.log(`   rank=#${rank?.rank}  uniqueness=${uniq.score} (${uniq.label})`);
