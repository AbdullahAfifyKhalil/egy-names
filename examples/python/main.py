"""egy-names v0.3.2 — Python showcase."""

from egy_names import EgyNames

en = EgyNames()

print("=" * 60)
print(" Egyptian Names (egy-names) v0.3.2 — Python Showcase")
print("=" * 60)

print("\n1. Name Generation:")
for n in en.generate(count=3, length=4, gender="female", religion="muslim"):
    print(f"   {n.ar}  ({n.en})")

print("\n2. Transliteration:")
print(f"   'محمد أحمد علي الشناوي' -> {en.translate('محمد أحمد علي الشناوي')}")

print("\n3. Orthographic Correction:")
print(f"   'احمد مصطفا عبد الرحيم' -> {en.correct('احمد مصطفا عبد الرحيم')}")

print("\n4. Dual Tashkeel & IPA:")
print(f"   Standard: {en.tashkeel_standard('محمد عبدالرحمن')}")
print(f"   Egyptian: {en.tashkeel_eg('محمد عبدالرحمن')}")
print(f"   IPA std:  {en.ipa_standard('جمال')}")
print(f"   IPA eg:   {en.ipa_eg('جمال')}")

print("\n5. Splitting concatenated names:")
print(f"   {en.split('محمدأحمدعليحسنالشناوي')}")

print("\n6. Pet names & famous figures:")
print(f"   dallaa: {en.dallaa('محمد', format='tashkeel')}")
print(f"   figures: {en.famous_figures('محمد', lang='en')[:2]}")

print("\n7. 14D lookup:")
info = en.info("محمد")
print(f"   {info.ar} / {info.en} | root={en.root('محمد')} | origin={en.origin('محمد')} | trend={en.trend('محمد')}")
print(f"   meaning: {en.meaning('محمد')['en']}")

print("\n8. Demographics:")
print(f"   {en.detect_gender('فاطمة الزهراء')}")
print(f"   {en.detect_religion('مينا جرجس بطرس')}")

print("\n9. Chain analysis, rank, uniqueness:")
for p in en.analyze_chain("محمد أحمد علي الشناوي"):
    print(f"   Slot {p.slot}: {p.name} — {p.role}")
rank = en.rank("محمد")
uniq = en.uniqueness("محمد أحمد علي الشناوي")
print(f"   rank=#{rank.rank}  uniqueness={uniq.score} ({uniq.label})")

print("\n10. Age intelligence:")
age = en.detect_age("كريم أشرف فاروق")
print(f"   detect_age: ~{age.estimated_age} ({age.generation_label})")
print(f"   names_for_age(25): {[n.ar for n in en.names_for_age(age=25, gender='m', top=5)]}")
