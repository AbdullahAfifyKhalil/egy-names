import Foundation
import EgyNames

let en = EgyptianNames()

print("=" * 60)
print(" Egyptian Names (EgyNames) - Swift Package Showcase")
print("=" * 60)

// 1. Generation
print("\n1. Name Generation:")
let names = en.generate(count: 3, length: 3, gender: "female")
for n in names {
    print("   \(n.ar)  (\(n.en))")
}

// 2. Translation
print("\n2. Transliteration:")
print("   'محمد أحمد علي' -> \(en.translate("محمد أحمد علي"))")

// 3. Correction
print("\n3. Orthographic Correction:")
print("   'احمد مصطفا عبد الرحيم' -> \(en.correct("احمد مصطفا عبد الرحيم"))")

// 4. Tashkeel
print("\n4. Tashkeel:")
print("   'محمد عبدالرحمن' -> \(en.tashkeel("محمد عبدالرحمن"))")

// 5. Splitting
print("\n5. Splitting unspaced name:")
print("   'محمدأحمدعليحسن' -> \(en.split("محمدأحمدعليحسن"))")

// 6. Chain Analysis
print("\n6. Patronymic Chain:")
for p in en.analyzeChain("محمد أحمد علي حسن الشاذلي") {
    print("   Slot \(p.slot): \(p.name) - \(p.detail)")
}
