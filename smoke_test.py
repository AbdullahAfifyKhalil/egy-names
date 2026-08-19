"""Smoke tests for the egyptian-names library."""

import sys
from pathlib import Path

# Add src to python path to test without installing
sys.path.insert(0, str(Path(__file__).resolve().parent / "python" / "src"))

from egy_names import EgyNames as EgyptianNames, Gender, Religion, NameRole, FrequencyClass

def run_tests():
    print("Initializing EgyptianNames...")
    en = EgyptianNames(seed=42)
    
    print("\n1. Data Stats:")
    stats = en.stats()
    print(f"Loaded {stats['total_names']} names.")
    assert stats['total_names'] > 30000

    print("\n2. Generation (10 random names):")
    names = en.generate(count=10, family_name=True)
    for i, n in enumerate(names, 1):
        print(f"  {i}. {n.ar}  --  {n.en}")
    
    print("\n3. Generating Female Christian Names:")
    c_names = en.generate(count=3, gender="female", religion="christian")
    for n in c_names:
        print(f"  {n.ar} ({n.en})")

    print("\n4. Translation:")
    t1 = en.translate("محمد أحمد علي")
    t2 = en.translate("Mohamed Ahmed Ali")
    print(f"  محمد أحمد علي -> {t1}")
    print(f"  Mohamed Ahmed Ali -> {t2}")

    print("\n5. Splitting:")
    s1 = en.split("محمد أحمد علي حسن الشاذلي")
    s2 = en.split("محمدأحمدعليحسنالشاذلي")  # Concatenated
    s3 = en.split("حسناء")
    print(f"  Spaced: {s1}")
    print(f"  Concatenated: {s2}")
    print(f"  Single name check: {s3}")
    
    print("\n6. Tashkeel:")
    tk = en.tashkeel("محمد عبدالرحمن")
    print(f"  محمد عبدالرحمن -> {tk}")

    print("\n7. Correction:")
    c1 = en.correct("احمد")
    c2 = en.correct("مصطفا")
    print(f"  احمد -> {c1}")
    print(f"  مصطفا -> {c2}")

    print("\n8. Annotation & Meaning:")
    info = en.annotate("محمد")
    print(f"  محمد: {info.meaning_ar}")
    
    print("\n9. Creative: Gender & Religion Detection")
    g1 = en.detect_gender("مريم إبراهيم حسن")
    r1 = en.detect_religion("جورج بطرس سمير ميخائيل")
    print(f"  مريم إبراهيم حسن -> {g1}")
    print(f"  جورج بطرس سمير ميخائيل -> {r1}")

    print("\n10. Creative: Chain Analysis")
    chain = en.analyze_chain("محمد أحمد علي حسن الشاذلي")
    for c in chain:
        print(f"  Slot {c.slot}: {c.name} ({c.role})")

    print("\n11. Search:")
    res = en.search(starts_with="عبد", max_results=3)
    print(f"  Starts with عبد:")
    for r in res:
        print(f"    {r.ar}")

    print("\nAll smoke tests passed!")

if __name__ == "__main__":
    run_tests()
