"""
Egyptian Names (egy-names) Python Demo
Run: pip install egy-names && python demo.py
"""

from egy_names import EgyptianNames, Gender, Religion, NameRole

def main():
    en = EgyptianNames()

    print("=" * 60)
    print(" Egyptian Names (egy-names) - Python Showcase")
    print("=" * 60)

    # 1. Realistic Patronymic Generation
    print("\n1. Generating realistic Egyptian full names:")
    names = en.generate(count=3, length=4, gender=Gender.MALE, religion=Religion.MUSLIM)
    for name in names:
        print(f"   AR: {name.ar}")
        print(f"   EN: {name.en}\n")

    # 2. Transliteration (Arabic <-> English)
    print("2. Bidirectional Transliteration:")
    print("   'محمد أحمد علي' ->", en.translate("محمد أحمد علي"))
    print("   'Mohamed Ahmed Ali' ->", en.translate("Mohamed Ahmed Ali"))

    # 3. Spelling & Orthographic Correction
    print("\n3. Orthographic Correction:")
    print("   'احمد مصطفا عبد الرحيم' ->", en.correct("احمد مصطفا عبد الرحيم"))

    # 4. Full Diacritization (Tashkeel)
    print("\n4. Tashkeel:")
    print("   'محمد عبدالرحمن' ->", en.tashkeel("محمد عبدالرحمن"))

    # 5. Concatenated Name Segmentation (DP Splitter)
    print("\n5. Splitting unspaced name:")
    print("   'محمدأحمدعليحسنالشاذلي' ->", en.split("محمدأحمدعليحسنالشاذلي"))

    # 6. Demographics Inference
    print("\n6. Demographics:")
    print("   'مريم إبراهيم حسن' ->", en.detect_gender("مريم إبراهيم حسن"))
    print("   'جورج بطرس ميخائيل' ->", en.detect_religion("جورج بطرس ميخائيل"))

    # 7. Patronymic Chain Analysis
    print("\n7. Patronymic Lineage Chain:")
    for part in en.analyze_chain("محمد أحمد علي حسن الشاذلي"):
        print(f"   Slot {part.slot}: {part.name} ({part.detail})")

if __name__ == "__main__":
    main()
