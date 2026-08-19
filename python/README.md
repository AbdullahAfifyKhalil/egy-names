# Egyptian Names (`egy-names`)

A production-grade Egyptian onomastic intelligence library for Python.

Powered by **33,117 verified Egyptian name lemmas** and **134,000+ lookup keys**, derived from an engineered dataset of 2.46 million Egyptian student records (11 million+ name tokens) from the Thanawiya Amma cohorts (2024–2026).

Developed by **Abdullah Afify** / **Afify**.

## Features

- **Culturally Authentic Generation**: Generate realistic Egyptian full names using a slot-weighted probabilistic engine grounded in actual national naming distributions.
- **Instant Translation**: Translate full names between Arabic and English with high accuracy, handling over 134,000 variant spellings.
- **Intelligent Segmentation**: Split concatenated, space-less Arabic text (e.g., `محمدأحمدعلي`) into correct individual name tokens using dynamic programming.
- **Deep Annotation**: Get rich metadata for any name including gender, religion, frequency class, national rank, and etymological meaning.
- **Orthographic Correction**: Correct misspelled or variant-form names to their canonical Arabic forms using a 54,000-entry correction index.
- **Creative AI Features**: Infer gender and religion from full patronymic chains, analyze chain structure (person, father, grandfather, family), and compute uniqueness scores.

## Installation

```bash
pip install egy-names
```

## Quick Start

### 1. Generating Names

```python
from egy_names import EgyNames

en = EgyNames()

# Generate 5 male Muslim full names (default length: 4-5 parts)
names = en.generate(count=5, gender="male", religion="muslim", family_name=True)

for name in names:
    print(name.ar)  # e.g., "محمد محمود علي أبوهشيمة"
    print(name.en)  # e.g., "Mohamed Mahmoud Ali Abuheshima"
```

### 2. Translation & Correction

```python
en.translate("محمد أحمد علي")
# -> "Mohamed Ahmed Ali"

en.correct("احمد")
# -> "أحمد"
```

### 3. Annotation & Meaning

```python
info = en.annotate("محمد")
print(info.gender)      # "male"
print(info.religion)    # "muslim"
print(info.meaning_ar)  # "المحمود؛ كثير الخصال المحمودة"
```

### 4. Intelligent Splitting

Handles fully concatenated Arabic text gracefully:

```python
en.split("محمدأحمدعليحسنالشاذلي")
# -> ["محمد", "أحمد", "علي", "حسن", "الشاذلي"]
```

### 5. Advanced Analysis

```python
# Infer gender from a full name string
en.detect_gender("مريم إبراهيم حسن")
# -> GenderDetection(gender='female', confidence=0.85)

# Infer religion based on theophoric patterns
en.detect_religion("جورج بطرس سمير")
# -> ReligionDetection(religion='christian', confidence=0.92)

# Analyze the patronymic chain
chain = en.analyze_chain("محمد أحمد علي حسن الشاذلي")
# Slot 1: محمد (person)
# Slot 2: أحمد (father)
# Slot 3: علي (grandfather)
# Slot 4: حسن (great_grandfather)
# Slot 5: الشاذلي (family_name)
```

## Data Assets

The library embeds a highly compressed `~1.5MB` JSON data bundle directly inside the package. It loads lazily and thread-safely on first use, keeping the memory footprint exceptionally low while providing instant lookups.

## License & Copyright

**MIT License**

Copyright (c) 2026 **Afify by Abdullah Afify**
