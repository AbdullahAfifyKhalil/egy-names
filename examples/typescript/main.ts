/**
 * egy-names 0.3.6 — TypeScript / JavaScript showcase.
 */
import { EgyNames } from "egy-names";

const en = new EgyNames();

console.log("=".repeat(60));
console.log(" Egyptian Names (egy-names) 0.3.6 — TypeScript");
console.log("=".repeat(60));

console.log("\n1. Generate a grounded chain:");
for (const n of en.generate({ count: 3, length: 4, gender: "female", religion: "muslim" })) {
  console.log(`   ${n.ar}  (${n.en})`);
}

console.log("\n2. Translate:");
console.log(`   ${en.translate("محمد أحمد علي الشناوي")}`);

console.log("\n3. Correct:");
console.log(`   ${en.correct("احمد مصطفا عبد الرحيم")}`);

console.log("\n4. Tashkeel and IPA:");
console.log(`   Standard: ${en.tashkeelStandard("محمد عبدالرحمن")}`);
console.log(`   Egyptian: ${en.tashkeelEg("محمد عبدالرحمن")}`);
console.log(`   IPA std:  ${en.ipaStandard("جمال")}`);
console.log(`   IPA eg:   ${en.ipaEg("جمال")}`);

console.log("\n5. Split a concatenated dump:");
console.log(`   ${JSON.stringify(en.split("محمدأحمدعليحسنالشناوي"))}`);

console.log("\n6. Pet names and figures:");
console.log(`   dallaa: ${JSON.stringify(en.dallaa("محمد", "tashkeel"))}`);
console.log(`   figures: ${en.famousFigures("محمد", "en").slice(0, 2).join(" | ")}`);

console.log("\n7. Lookup:");
const info = en.info("محمد");
console.log(`   ${info?.ar} / ${info?.en} | root=${en.root("محمد")} | origin=${en.origin("محمد")}`);
console.log(`   meaning: ${en.meaning("محمد")?.en}`);

console.log("\n8. Validity — personal names only:");
console.log(`   isValid("محمد")  = ${en.isValid("محمد")}`);
console.log(`   isValid("Mahmoud") = ${en.isValid("Mahmoud")}`);
console.log(`   isValid("الله")   = ${en.isValid("الله")}  // in the index, not a person`);

console.log("\n9. First personal token wins:");
console.log("  ", en.detectGender("فاطمة محمد علي"));
console.log("  ", en.detectReligion("مينا جرجس بطرس"));

console.log("\n10. Chain, rank, uniqueness:");
for (const p of en.analyzeChain("محمد أحمد علي الشناوي")) {
  console.log(`   Slot ${p.slot}: ${p.name} — ${p.role}`);
}
const rank = en.rank("محمد");
const uniq = en.uniqueness("محمد أحمد علي الشناوي");
console.log(`   rank=#${rank?.rank}  uniqueness=${uniq.score} (${uniq.label})`);
