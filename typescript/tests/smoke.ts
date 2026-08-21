import { EgyptianNames } from "../src/index";

function runTests() {
  console.log("Initializing EgyptianNames...");
  const en = new EgyptianNames({ seed: 42 });

  console.log("\n1. Data Stats:");
  const stats = en.stats();
  console.log(`Loaded ${stats.total_names} names.`);
  if (stats.total_names < 30000) throw new Error("Not enough names loaded");

  console.log("\n2. Generation (5 random names):");
  const names = en.generate({ count: 5, familyName: true });
  names.forEach((n, i) => {
    console.log(`  ${i + 1}. ${n.ar}  --  ${n.en}`);
  });

  console.log("\n3. Generating Female Christian Names:");
  const cNames = en.generate({ count: 3, gender: "female", religion: "christian" });
  cNames.forEach((n) => {
    console.log(`  ${n.ar} (${n.en})`);
  });

  console.log("\n4. Translation:");
  const t1 = en.translate("محمد أحمد علي");
  const t2 = en.translate("Mohamed Ahmed Ali");
  console.log(`  محمد أحمد علي -> ${t1}`);
  console.log(`  Mohamed Ahmed Ali -> ${t2}`);

  console.log("\n5. Splitting:");
  const s1 = en.split("محمد أحمد علي حسن الشاذلي");
  const s2 = en.split("محمدأحمدعليحسنالشاذلي"); // Concatenated
  const s3 = en.split("حسناء");
  console.log(`  Spaced:`, s1);
  console.log(`  Concatenated:`, s2);
  console.log(`  Single name check:`, s3);

  console.log("\n6. Tashkeel:");
  const tk = en.tashkeel("محمد عبدالرحمن");
  console.log(`  محمد عبدالرحمن -> ${tk}`);

  console.log("\n7. Correction:");
  const c1 = en.correct("احمد");
  const c2 = en.correct("مصطفا");
  console.log(`  احمد -> ${c1}`);
  console.log(`  مصطفا -> ${c2}`);

  console.log("\n8. Annotation & Meaning:");
  const info = en.annotate("محمد");
  // @ts-ignore
  console.log(`  محمد: ${info.meaning_ar}`);

  console.log("\n9. Creative: Gender & Religion Detection");
  const g1 = en.detectGender("مريم إبراهيم حسن");
  const r1 = en.detectReligion("جورج بطرس سمير ميخائيل");
  console.log(`  مريم إبراهيم حسن ->`, g1);
  console.log(`  جورج بطرس سمير ميخائيل ->`, r1);

  console.log("\n10. Creative: Chain Analysis");
  const chain = en.analyzeChain("محمد أحمد علي حسن الشاذلي");
  chain.forEach((c) => {
    console.log(`  Slot ${c.slot}: ${c.name} (${c.role})`);
  });

  console.log("\n11. Search:");
  const res = en.search({ startsWith: "عبد", maxResults: 3 });
  console.log(`  Starts with عبد:`);
  res.forEach((r) => {
    console.log(`    ${r.ar}`);
  });

  console.log("\n12. 11D Features (Tashkeel Eg, IPA, Dallaa, Roots, Origins, Trends):");
  const tkEg = en.tashkeelEg("محمد");
  const ipaStd = en.ipa("جمال", "standard");
  const ipaEg = en.ipaEg("جمال");
  const dl = en.dallaa("محمد");
  const rt = en.root("محمد");
  const ot = en.origin("محمد");
  const ff = en.famousFigures("محمد");
  const tr = en.trend("محمد");

  console.log(`  Tashkeel Egyptian: ${tkEg}`);
  console.log(`  IPA Standard: ${ipaStd}`);
  console.log(`  IPA Egyptian: ${ipaEg}`);
  console.log(`  Dallaa (Pet names):`, dl);
  console.log(`  Root: ${rt} | Origin: ${ot} | Trend: ${tr}`);
  console.log(`  Famous Figures:`, ff);

  console.log("\nAll smoke tests passed!");
}

runTests();
