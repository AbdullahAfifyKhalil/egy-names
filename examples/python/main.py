"""egy-names 0.3.6 — Python showcase."""

from egy_names import EgyNames

en = EgyNames()

print("=" * 60)
print(" Egyptian Names (egy-names) 0.3.6 — Python")
print("=" * 60)

print("\n1. Generate a grounded chain:")
for n in en.generate(count=3, length=4, gender="female", religion="muslim"):
    print(f"   {n.ar}  ({n.en})")

print("\n2. Translate:")
print(f"   {en.translate('محمد أحمد علي الشناوي')}")

print("\n3. Correct:")
print(f"   {en.correct('احمد مصطفا عبد الرحيم')}")

print("\n4. Tashkeel and IPA:")
print(f"   Standard: {en.tashkeel_standard('محمد عبدالرحمن')}")
print(f"   Egyptian: {en.tashkeel_eg('محمد عبدالرحمن')}")
print(f"   IPA std:  {en.ipa_standard('جمال')}")
print(f"   IPA eg:   {en.ipa_eg('جمال')}")

print("\n5. Split a concatenated dump:")
print(f"   {en.split('محمدأحمدعليحسنالشناوي')}")

print("\n6. Pet names and figures:")
print(f"   dallaa: {en.dallaa('محمد', format='tashkeel')}")
print(f"   figures: {en.famous_figures('محمد', lang='en')[:2]}")

print("\n7. Lookup:")
info = en.info("محمد")
print(f"   {info.ar} / {info.en} | root={en.root('محمد')} | origin={en.origin('محمد')}")
print(f"   meaning: {en.meaning('محمد')['en']}")

print("\n8. Validity — personal names only:")
print(f"   is_valid('محمد')  = {en.is_valid('محمد')}")
print(f"   is_valid('Mahmoud') = {en.is_valid('Mahmoud')}")
print(f"   is_valid('الله')   = {en.is_valid('الله')}  # in the index, not a person")

print("\n9. First personal token wins:")
print(f"   {en.detect_gender('فاطمة محمد علي')}")
print(f"   {en.detect_religion('مينا جرجس بطرس')}")

print("\n10. Chain, rank, uniqueness:")
for p in en.analyze_chain("محمد أحمد علي الشناوي"):
    print(f"   Slot {p.slot}: {p.name} — {p.role}")
rank = en.rank("محمد")
uniq = en.uniqueness("محمد أحمد علي الشناوي")
print(f"   rank=#{rank.rank}  uniqueness={uniq.score} ({uniq.label})")

print("\n11. Age:")
age = en.detect_age("كريم أشرف فاروق")
print(f"   ~{age.estimated_age} ({age.generation_label})")
print(f"   names_for_age(25): {[n.ar for n in en.names_for_age(age=25, gender='m', top=5)]}")

print("\n12. Identify — book first, then the fallback model:")
book = en.identify("محمد")
print(f"   محمد → {book.ar} / {book.en}  inferred={book.inferred}  source={book.source}")
for tok in en.identify_all("محمد زوكرمانوفيتش"):
    print(
        f"   {tok.surface} → gender={tok.gender}  inferred={tok.inferred}  "
        f"source={tok.source}  valid={tok.is_valid}"
    )
