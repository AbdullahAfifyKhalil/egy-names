---
language:
- ar
- en
multilinguality:
- multilingual
size_categories:
- 1M<n<10M
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
### *From 1.5M+ Raw National Records to an Empirical Onomastic and Linguistic Engine*

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

### 1. Load Final Canonical Master Dataset (Default)
```python
from datasets import load_dataset

# Load 33,117 annotated canonical names
dataset = load_dataset("<YOUR_HF_USERNAME>/egyptian-names")
print(dataset["train"][0])
```

### 2. Load Raw Unprocessed Full Names (Phase 0 — 1.54M Records)
```python
raw_dataset = load_dataset("<YOUR_HF_USERNAME>/egyptian-names", "phase0_raw")
print(f"Total raw names: {len(raw_dataset['train']):,}")
# Example: 'احمد باسم لينان محمد سليمان'
```

### 3. Load Segmented Patronymic Chains (Phase 1)
```python
chains_dataset = load_dataset("<YOUR_HF_USERNAME>/egyptian-names", "phase1_segmented")
# Inspect token-by-token genealogical position
print(chains_dataset["train"][:3])
```

### 4. Load Unique Token Frequency Analysis (Phase 2)
```python
freq_dataset = load_dataset("<YOUR_HF_USERNAME>/egyptian-names", "phase2_frequencies")
# Top names by frequency across the national corpus
print(freq_dataset["train"][:5])
```

### 5. Load Spelling & Typo Correction Rules (Phase 3)
```python
corr_dataset = load_dataset("<YOUR_HF_USERNAME>/egyptian-names", "phase3_corrections")
# Map misspelling to canonical form: 'احمد مصطفا' -> 'أحمد مصطفى'
```

---

## 🧬 Configurations & Data Schemas

### 1. `final_canonical` (Default — 33,117 Rows)
The core enriched onomastic dictionary:

| Field | Type | Description | Example |
|---|---|---|---|
| `ar_name` | string | Canonical Arabic surface form | `محمد` |
| `en_name` | string | Standard English transliteration | `Mohamed` |
| `gender` | string | Empirical gender (`male`, `female`, `neutral`) | `male` |
| `religion` | string | Cultural/religious marker (`muslim`, `christian`, `neutral`) | `muslim` |
| `name_role` | string | Role classification (`given`, `family`) | `given` |
| `frequency_class` | string | Relative corpus frequency (`common`, `normal`, `rare`) | `common` |
| `corpus_share_pct` | float | Percentage share across national demographic corpus | `4.2264` |
| `tashkeel` | string | Complete Arabic diacritization | `مُحَمَّد` |
| `meaning_ar` | string | Arabic etymological meaning and semantic root | `المحمود؛ كثير الخصال المحمودة` |
| `meaning_en` | string | English translation of the name's meaning | `The Praised One` |
| `slot_1_person_pct` | float | Probability of name occurring in Slot 1 (Person) | `56.66` |
| `slot_2_father_pct` | float | Probability of name occurring in Slot 2 (Father) | `108.82` |
| `slot_3_grandfather_pct`| float | Probability of name occurring in Slot 3 (Grandfather) | `109.69` |
| `slot_4_ancestor_pct` | float | Probability of name occurring in Slot 4 (Ancestor) | `88.42` |
| `slot_5_family_pct` | float | Probability of name occurring in Slot 5 (Family/Surname)| `39.05` |
| `slot_6_clan_pct` | float | Probability of name occurring in Slot 6 (Clan/Tribe)| `12.10` |
| `ar_variants` | list[str]| Common Arabic spelling and phonetic variations | `["محمد", "محمّد"]` |
| `en_variants` | list[str]| Common English transliteration variations | `["Mohamed", "Muhammad"]` |

---

### 2. `phase0_raw` (1,545,970 Rows)
Unprocessed, authentic raw full names as recorded in national records:

| Field | Type | Description | Example |
|---|---|---|---|
| `raw_full_name` | string | Raw full name sequence | `احمد باسم لينان محمد سليمان` |

---

### 3. `phase1_segmented` (1,000,000 Rows Sample / 6.9M Corpus)
Tokens extracted and indexed by genealogical slot position:

| Field | Type | Description | Example |
|---|---|---|---|
| `full_name` | string | Source full name string | `احمد باسم لينان محمد سليمان` |
| `slot_position` | int | Generational slot (1=Person, 2=Father, 3=Grandfather...) | `1` |
| `name_token` | string | Isolated name token | `احمد` |

---

### 4. `phase2_frequencies` (43,333 Rows)
Frequency distribution of unique name elements across the corpus:

| Field | Type | Description | Example |
|---|---|---|---|
| `name_token` | string | Name element | `محمد` |
| `occurrence_count` | int | Total occurrences in corpus | `873333` |
| `frequency_share_pct`| float | Percentage of all corpus tokens | `12.53%` |

---

### 5. `phase3_corrections` (8,616 Rows)
Comprehensive dictionary for orthographic normalization and error correction:

| Field | Type | Description | Example |
|---|---|---|---|
| `misspelled_surface_form` | string | Typo, non-standard spelling, or unspaced compound | `احمد مصطفا` |
| `canonical_ar_name` | string | Standardized canonical form | `أحمد مصطفى` |

---

## 🏛️ Empirical Methodology & Privacy

- **Data Sources**: Extracted and compiled from publicly accessible historical and administrative educational registers.
- **Aggregation**: All data is strictly aggregated statistical distributions, morphological entries, and frequency models. **No personally identifiable information (PII) or private individual records are included.**
- **DeterministicParity**: Compatible with the open-source **`egy-names`** engine across 7 programming ecosystems (Python, TypeScript, C#, Dart, Swift, Java, C++).

## 🏢 About Afify Corporation
This dataset is curated and released by **[Afify Corporation](https://afify.co)** (`afify.co`), a technology and media enterprise innovating across software, hardware systems, and digital media, leveraging advanced engineering and artificial intelligence.

- 🌐 **Corporate Portal**: [afify.co](https://afify.co)
- 🐙 **GitHub Organization**: [github.com/AbdullahAfifyKhalil](https://github.com/AbdullahAfifyKhalil)
- 👤 **Founder & Maintainer**: [Abdullah Afify](https://github.com/AbdullahAfifyKhalil)

---

## 📜 Citation & License

Licensed under the **MIT License**.

```bibtex
@dataset{egy_names_2026,
  author = {Abdullah Afify},
  title = {Egyptian Names & Onomastic Intelligence Dataset},
  year = {2026},
  publisher = {Hugging Face},
  url = {https://github.com/AbdullahAfifyKhalil/egy-names}
}
```
