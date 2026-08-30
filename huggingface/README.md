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

# Egyptian Names & Onomastic Intelligence Dataset
### *From 15.88M+ Raw National Records to an Empirical Onomastic and Linguistic Engine*

This repository hosts the complete, multi-phase statistical and linguistic dataset powering **`egy-names`**, the production onomastic intelligence engine for contemporary Egyptian naming traditions.

---

## Dataset Pipeline Overview

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

## Full Data vs. Single Names Breakdown

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

## Quick Start with Hugging Face `datasets`

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

## Configurations & Data Schemas

### 1. `final_canonical` (Default — 44,626 Rows)
The master 14-dimensional enriched onomastic dictionary:

| Field | Type | Description | Example (`محمد`) |
|---|---|---|---|
| `name_ar` | string | Canonical Arabic surface form | `محمد` |
| `name_en` | string | Standard Egyptian English transliteration | `Mohamed` |
| `gender` | string | Empirical gender (`male`, `female`, `neutral`) | `male` |
| `religion` | string | Cultural/religious marker (`muslim`, `christian`, `neutral`) | `muslim` |
| `role` | string | Onomastic role (`given`, `family`, `kunya`, `tribal`) | `given` |
| `tashkeel_standard` | string | Modern Standard Arabic vowel diacritization | `مُحَمَّد` |
| `tashkeel_eg` | string | Egyptian Colloquial Arabic vocalization | `مُحَمَّدْ` |
| `ipa_standard` | string | Modern Standard Arabic IPA transcription | `/muħamːad/` |
| `ipa_eg` | string | Egyptian Colloquial Arabic IPA transcription | `[moˈħamːæd]` |
| `meaning_ar` | string | Root & etymological definition in Arabic | `المحمود؛ كثير الخصال المحمودة (من الجذر ح م د)` |
| `meaning_en` | string | Root & translation in English | `The praised one; frequently praised` |
| `dallaa_ar` | string | Authentic Egyptian pet names (pipe-separated) | `ميدو\|حمو\|حمودة` |
| `dallaa_tashkeel` | string | Vocalized Egyptian pet names with Tashkeel | `مِيدُو\|حَمُّو\|حَمُّودَة` |
| `dallaa_en` | string | Transliterated English pet names | `Mido\|Hamou\|Hamouda` |
| `dallaa_ipa` | string | Egyptian IPA transcription for pet names | `[ˈmiːdu]\|[ˈħæm.mu]\|[ħæmˈmuːdæ]` |
| `root` | string | Semitic/Coptic morphological root | `ح-م-د` |
| `origin_type` | string | Historical etymological stratum | `arabic_classical` |
| `famous_figures_ar` | string | Egyptian public figures & descriptions (Arabic) | `محمد صلاح (قائد منتخب مصر)\|محمد علي باشا (مؤسس مصر الحديثة)` |
| `famous_figures_en` | string | Egyptian public figures & descriptions (English) | `Mohamed Salah (Egyptian Football Captain)\|Mohamed Ali Pasha` |
| `trend_category` | string | Sociological generation trend | `classic_timeless` |
| `slot1_pct` ... `slot8_pct` | float | Generational slot distribution percentages | `26.91`, `31.77`, `28.84`, `7.19`, ... |
| `corpus_share_pct` | float | Overall percentage share of all tokens in Egypt | `0.179624` |

---

## Research Citations & Licensing

Published by **[Afify](https://afify.co)** and **[Abdullah Afify](https://github.com/AbdullahAfifyKhalil)**. Product page: **[afify.co/egy-names](https://afify.co/egy-names)**. Released under the **MIT License** and free for academic, commercial, and research use.

```bibtex
@dataset{afify2026egyptian_names,
  author       = {Abdullah Afify},
  title        = {Egyptian Names & Onomastic Intelligence Dataset},
  year         = {2026},
  publisher    = {Hugging Face},
  howpublished = {\url{https://huggingface.co/datasets/Abdullah-afify/egyptian-names}}
}
```
