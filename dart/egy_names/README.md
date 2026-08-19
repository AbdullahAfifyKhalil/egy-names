# Egyptian Names (`egy_names`)

A production-grade Egyptian onomastic intelligence library for Dart and Flutter.

Powered by **33,117 verified Egyptian name lemmas** and **134,000+ lookup keys**, derived from an engineered dataset of 2.46 million Egyptian student records (11 million+ name tokens) from the Thanawiya Amma cohorts (2024–2026).

Developed by **Abdullah Afify** / **Afify**.

---

## Features

- **Culturally Authentic Generation**: Generate realistic Egyptian full names using a slot-weighted probabilistic engine grounded in actual national naming distributions.
- **Instant Translation**: Translate full names between Arabic and English with high accuracy, handling over 134,000 variant spellings.
- **Intelligent Segmentation**: Split concatenated, space-less Arabic text (e.g., `محمدأحمدعلي`) into correct individual name tokens using dynamic programming.
- **Deep Annotation**: Get rich metadata for any name including gender, religion, frequency class, national rank, and etymological meaning.
- **Orthographic Correction**: Correct misspelled or variant-form names to their canonical Arabic forms using a 54,000-entry correction index.
- **Creative AI Features**: Infer gender and religion from full patronymic chains, analyze chain structure (person, father, grandfather, family), and compute uniqueness scores.

---

## Usage (Dart / Flutter)

Add `egy_names` to your `pubspec.yaml`:

```yaml
dependencies:
  egy_names: ^0.1.0
```

```dart
import 'package:egy_names/egy_names.dart';

void main() {
  final en = EgyNames();

  // 1. Generate Authentic Egyptian Names
  final names = en.generate(count: 3, gender: 'male', religion: 'muslim');
  for (final n in names) {
    print('${n.ar}  --  ${n.en}');
  }

  // 2. Translate
  print(en.translate('محمد أحمد علي')); // Mohamed Ahmed Ali
  print(en.translate('Mohamed Ahmed Ali')); // محمد أحمد علي

  // 3. Split Concatenated Space-less Names
  print(en.split('محمدأحمدعليحسنالشاذلي')); // ['محمد', 'أحمد', 'علي', 'حسن', 'الشاذلي']

  // 4. Correct & Tashkeel
  print(en.correct('احمد')); // أحمد
  print(en.tashkeel('محمد عبدالرحمن')); // مُحَمَّد عَبْدُالرَّحْمَن

  // 5. Annotate & Meaning
  final info = en.annotate('محمد') as NameInfo?;
  print(info?.meaningAr);

  // 6. Chain Analysis & Inferences
  print(en.detectGender('مريم إبراهيم حسن'));
  print(en.detectReligion('جورج بطرس سمير ميخائيل'));
}
```

---

## License & Copyright

**MIT License**

Copyright (c) 2026 **Afify by Abdullah Afify**
