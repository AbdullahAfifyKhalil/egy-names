import Foundation
import EgyNames

let en = EgyptianNames()
let rule = String(repeating: "=", count: 60)

print(rule)
print(" Egyptian Names (EgyNames) 0.3.6 — Swift")
print(rule)

print("\n1. Generate a grounded chain:")
for n in en.generate(count: 3, length: 4, gender: "female", religion: "muslim") {
    print("   \(n.ar)  (\(n.en))")
}

print("\n2. Translate:")
print("   \(en.translate("محمد أحمد علي الشناوي"))")

print("\n3. Correct:")
print("   \(en.correct("احمد مصطفا عبد الرحيم"))")

print("\n4. Tashkeel and IPA:")
print("   Standard: \(en.tashkeel("محمد عبدالرحمن"))")
print("   Egyptian: \(en.tashkeelEg("محمد عبدالرحمن"))")
print("   IPA std:  \(en.ipa("جمال"))")
print("   IPA eg:   \(en.ipaEg("جمال"))")

print("\n5. Split a concatenated dump:")
print("   \(en.split("محمدأحمدعليحسنالشناوي"))")

print("\n6. Pet names and figures:")
print("   dallaa: \(en.dallaa("محمد", format: "tashkeel"))")
print("   figures: \(en.famousFigures("محمد", lang: "en").prefix(2))")

print("\n7. Lookup:")
print("   root=\(en.root("محمد") ?? "nil") | origin=\(en.origin("محمد") ?? "nil") | trend=\(en.trend("محمد") ?? "nil")")
if let meaning = en.meaning("محمد") {
    print("   meaning: \(meaning["en"] ?? "")")
}

print("\n8. Validity — personal names only:")
print("   isValid(\"محمد\")  = \(en.isValid("محمد"))")
print("   isValid(\"Mahmoud\") = \(en.isValid("Mahmoud"))")
print("   isValid(\"الله\")   = \(en.isValid("الله"))  // in the index, not a person")

print("\n9. First personal token wins:")
let gender = en.detectGender("فاطمة محمد علي")
let religion = en.detectReligion("مينا جرجس بطرس")
print("   \(gender.gender) (\(gender.confidence))")
print("   \(religion.religion) (\(religion.confidence))")

print("\n10. Chain, rank, uniqueness:")
for p in en.analyzeChain("محمد أحمد علي الشناوي") {
    print("   Slot \(p.slot): \(p.name) — \(p.role)")
}
if let rank = en.rank("محمد") {
    let uniq = en.uniqueness("محمد أحمد علي الشناوي")
    print("   rank=#\(rank.rank)  uniqueness=\(uniq.score) (\(uniq.label))")
}
