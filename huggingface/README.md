---
language:
- ar
- en
multilinguality:
- multilingual
size_categories:
- 10M<n<100M
source_datasets:
- original
task_categories:
- text-classification
- token-classification
- feature-extraction
- table-to-text
task_ids:
- named-entity-recognition
- text-scoring
- linguistic-analysis
pretty_name: Egyptian Names & Onomastic Intelligence Dataset
tags:
- arabic
- nlp
- egypt
- onomastics
- patronymics
- names
- names-corpus
- demographics
- full-names
- lineage
license: mit
configs:
- config_name: default
  data_files: "data/final_canonical_names.parquet"
- config_name: final_canonical
  data_files: "data/final_canonical_names.parquet"
- config_name: phase0_raw
  data_files: "data/phase0_raw_full_names.parquet"
- config_name: phase1_segmented
  data_files: "data/phase1_segmented_chains.parquet"
- config_name: phase2_frequencies
  data_files: "data/phase2_token_frequencies.parquet"
- config_name: phase3_corrections
  data_files: "data/phase3_spelling_corrections.parquet"
- config_name: slot_distributions
  data_files: "data/slot_distributions.parquet"
---

# 🇪🇬 Egyptian Names & Onomastic Intelligence Dataset
### *From 15.88M+ Raw National Records to an Empirical Onomastic and Linguistic Engine*

This repository hosts the complete, multi-phase statistical and linguistic dataset powering **`egy-names`**, the production onomastic intelligence engine for contemporary Egyptian naming traditions.

---

## 📊 Dataset Pipeline Overview

Egyptian names follow an unbroken patronymic lineage chain ($Personal + Father + Grandfather + Ancestor + Family/Tribe$). This dataset provides the full transformation pipeline across all developmental phases:

```
[ Phase 0: 15.88M+ Raw Full Name Chains (30M+ Records) ]
              │
              ▼
[ Phase 1: 63.5M+ Segmented Patronymic Tokens & Positions ]
              │
              ▼
[ Phase 2: 43.3K Unique Raw Token Frequencies ]
              │
              ▼
[ Phase 3: 23.4K+ Orthographic & Spelling Corrections ]
              │
              ▼
[ Phase 4: 44.6K Master Annotated Canonical Names ]
(Gender + Religion + Generational Slot Probabilities + Tashkeel + Meanings + Transliterations)
```

---

## 📊 Full Data vs. Single Names Breakdown

| Metric | Count | Description |
| :--- | :--- | :--- |
| **Total Raw Exam Records** | **~15,875,535** | Total individual student & citizen exam rows across 494 dataset files |
| **Total Full Name Occurrences** | **~15.88 Million** | Total full patronymic name chains (e.g., `"محمد أحمد علي حسن الشرقاوي"`) |
| **Unique Full Name Strings** | **1,545,970+** | Distinct full 3-to-5-part name combinations |
| **Total Single Name Occurrences** | **~63,500,000** | Total individual name occurrences across all slots (averaging 4 names per chain) |
| **Raw Distinct Single Tokens** | **43,333** | Distinct raw word tokens before typo cleaning |
| **Typo & Spelling Corrections** | **23,457** | Mappings for misspellings and unspaced compound names (`عبدالرحمن` $\to$ `عبد الرحمن`) |
| **Final Canonical Master Lexicon** | **44,626** | **The complete clean dictionary of unique Egyptian names** |

### Understanding Population Records vs. Onomastic Lexicon
In an Egyptian population of **~16–30 Million records**, names repeat extensively across generations:
* Highly common given names like **محمد**, **أحمد**, **محمود**, **علي**, **فاطمة**, **مريم** occur millions of times.
* Family surnames like **الشرقاوي**, **السيد**, **إبراهيم** occur tens of thousands of times.
* When every patronymic chain is decomposed and deduplicated, the **complete onomastic vocabulary of Egypt consists of 44,626 unique canonical lemmas**, capturing >99.9% of all contemporary and historical Egyptian personal and family names.

---

## 🚀 Quick Start with Hugging Face `datasets`

### 1. Load Final Canonical Master Dataset (Default — 44,626 Names)
```python
from datasets import load_dataset

# Load 44,626 annotated canonical names
dataset = load_dataset("Abdullah-afify/egyptian-names")
print(dataset["train"][0])
```

### 2. Load Raw Unprocessed Full Names (Phase 0 — 1.54M Sample / 15.88M Corpus)
```python
raw_dataset = load_dataset("Abdullah-afify/egyptian-names", "phase0_raw")
print(f"Total raw names: {len(raw_dataset['train']):,}")
# Example: 'احمد باسم لينان محمد سليمان'
```

### 3. Load Segmented Patronymic Chains (Phase 1)
```python
chains_dataset = load_dataset("Abdullah-afify/egyptian-names", "phase1_segmented")
# Inspect token-by-token genealogical position
print(chains_dataset["train"][:3])
```

### 4. Load Unique Token Frequency Analysis (Phase 2)
```python
freq_dataset = load_dataset("Abdullah-afify/egyptian-names", "phase2_frequencies")
# Top names by frequency across the national corpus
print(freq_dataset["train"][:5])
```

### 5. Load Spelling & Typo Correction Rules (Phase 3 — 23,457 Rules)
```python
corr_dataset = load_dataset("Abdullah-afify/egyptian-names", "phase3_corrections")
# Map misspelling to canonical form: 'احمد مصطفا' -> 'أحمد مصطفى'
```

---

## 🧬 Configurations & Data Schemas

### 1. `final_canonical` (Default — 44,626 Rows)
The core enriched onomastic dictionary:

| Field | Type | Description | Example |
|---|---|---|---|
| `name_ar` | string | Canonical Arabic surface form | `محمد` |
| `name_en` | string | Standard Egyptian English transliteration | `Mohamed` |
| `gender` | string | Empirical gender (`male`, `female`, `neutral`) | `male` |
| `religion` | string | Cultural/religious marker (`muslim`, `christian`, `neutral`) | `muslim` |
| `role` | string | Onomastic role (`given`, `family`, `kunya`, `tribal`) | `given` |
| `tashkeel` | string | Full Arabic vowel diacritization | `مُحَمَّد` |
| `meaning_ar` | string | Morphological root & etymological definition in Arabic | `المحمود؛ كثير الخصال المحمودة (من الجذر ح م د)` |
| `meaning_en` | string | English translation & linguistic origin | `The praised one; frequently praised` |
| `slot1_pct` | float | Probability weight in Slot 1 (Person's own name) | `32.4` |
| `slot2_pct` | float | Probability weight in Slot 2 (Father's name) | `28.6` |
| `slot3_pct` | float | Probability weight in Slot 3 (Grandfather's name) | `22.1` |
| `slot4_pct` | float | Probability weight in Slot 4 (Great-grandfather's name) | `14.2` |
| `slot5_pct` | float | Probability weight in Slot 5 (Family surname) | `2.1` |
| `slot6_pct` | float | Probability weight in Slot 6 (Clan/tribal name) | `0.6` |
| `corpus_share_pct` | float | Overall percentage share of all name tokens in Egypt | `0.068` |

---

## 🏛️ Research Citations & Licensing

This dataset is released under the **MIT License** and is free for academic, commercial, and research use.

```bibtex
@dataset{afify2026egyptian_names,
  author       = {Abdullah Afify},
  title        = {Egyptian Names & Onomastic Intelligence Dataset},
  year         = {2026},
  publisher    = {Hugging Face},
  howpublished = {\url{https://huggingface.co/datasets/Abdullah-afify/egyptian-names}}
}
```
