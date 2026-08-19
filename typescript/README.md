# Egyptian Names (`egy-names`)

A production-grade Egyptian onomastic intelligence library for TypeScript and JavaScript (Node.js).

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

## Installation

```bash
npm install egy-names
```

---

## Quick Start (TypeScript / JavaScript)

```typescript
import { EgyNames } from "egy-names";

const en = new EgyNames();

// 1. Generate Egyptian full names
const names = en.generate({ count: 5, gender: "male", religion: "muslim", familyName: true });
for (const n of names) {
  console.log(`${n.ar}  --  ${n.en}`);
  // e.g. "محمد محمود علي أبوهشيمة  --  Mohamed Mahmoud Ali Abuheshima"
}

// 2. Translation
console.log(en.translate("محمد أحمد علي"));
// -> "Mohamed Ahmed Ali"
console.log(en.translate("Mohamed Ahmed Ali"));
// -> "محمد أحمد علي"

// 3. Intelligent Splitting (DP Segmentation for concatenated names)
console.log(en.split("محمدأحمدعليحسنالشاذلي"));
// -> ["محمد", "أحمد", "علي", "حسن", "الشاذلي"]

// 4. Correction & Tashkeel
console.log(en.correct("احمد"));
// -> "أحمد"
console.log(en.tashkeel("محمد عبدالرحمن"));
// -> "مُحَمَّد عَبْدُالرَّحْمَن"

// 5. Annotation & Meaning
const info = en.annotate("محمد");
console.log(info);

// 6. Chain Analysis & Inferences
console.log(en.detectGender("مريم إبراهيم حسن"));
// -> { gender: 'female', confidence: 0.57 }

console.log(en.detectReligion("جورج بطرس سمير ميخائيل"));
// -> { religion: 'christian', confidence: 0.75 }
```

---

## License & Copyright

**MIT License**

Copyright (c) 2026 **Afify by Abdullah Afify**
