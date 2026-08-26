import Foundation
import EgyNames

let en = EgyptianNames()
let rule = String(repeating: "=", count: 60)

print(rule)
print(" Egyptian Names (EgyNames) v0.3.2 — Swift Showcase")
print(rule)

print("\n1. Name Generation:")
for n in en.generate(count: 3, length: 4, gender: "female", religion: "muslim") {
    print("   \(n.ar)  (\(n.en))")
}

print("\n2. Transliteration:")
print("   'محمد أحمد علي الشناوي' -> \(en.translate("محمد أحمد علي الشناوي"))")

print("\n3. Orthographic Correction:")
print("   'احمد مصطفا عبد الرحيم' -> \(en.correct("احمد مصطفا عبد الرحيم"))")

print("\n4. Dual Tashkeel & IPA:")
print("   Standard: \(en.tashkeel("محمد عبدالرحمن"))")
print("   Egyptian: \(en.tashkeelEg("محمد عبدالرحمن"))")
print("   IPA std:  \(en.ipa("جمال"))")
print("   IPA eg:   \(en.ipaEg("جمال"))")

print("\n5. Splitting concatenated names:")
print("   \(en.split("محمدأحمدعليحسنالشناوي"))")

print("\n6. Pet names & famous figures:")
print("   dallaa: \(en.dallaa("محمد", format: "tashkeel"))")
print("   figures: \(en.famousFigures("محمد", lang: "en").prefix(2))")

print("\n7. 14D lookup:")
print("   root=\(en.root("محمد") ?? "nil") | origin=\(en.origin("محمد") ?? "nil") | trend=\(en.trend("محمد") ?? "nil")")
if let meaning = en.meaning("محمد") {
    print("   meaning: \(meaning["en"] ?? "")")
}

print("\n8. Demographics:")
let gender = en.detectGender("فاطمة الزهراء")
let religion = en.detectReligion("مينا جرجس بطرس")
print("   \(gender.gender) (\(gender.confidence))")
print("   \(religion.religion) (\(religion.confidence))")

print("\n9. Chain analysis, rank, uniqueness:")
for p in en.analyzeChain("محمد أحمد علي الشناوي") {
    print("   Slot \(p.slot): \(p.name) — \(p.role)")
}
if let rank = en.rank("محمد") {
    let uniq = en.uniqueness("محمد أحمد علي الشناوي")
    print("   rank=#\(rank.rank)  uniqueness=\(uniq.score) (\(uniq.label))")
}
