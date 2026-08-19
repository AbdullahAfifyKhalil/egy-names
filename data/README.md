# Egyptian Onomastic Dataset (`egy-names/data`)

An empirical, large-scale statistical dataset of contemporary Egyptian personal names, patronymic lineages, and family names extracted from millions of verified national demographic records.

---

## Dataset Architecture & Pipeline Phases

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Raw Demographic Records (Millions of Full Names)   │
└──────────────────────────────┬──────────────────────────────┘
                               │ (DP Segmentation & Token Cleaning)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 2: Patronymic Slot Distribution (Slots 1 to 6)        │
│   • First Name (اسم الشخص)                                  │
│   • Father's Name (اسم الأب)                                │
│   • Grandfather's Name (اسم الجد)                           │
│   • Ancestor & Lineage (الأنساب)                            │
│   • Family / Surname (اللقب والنسب)                         │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Statistical Aggregation & Frequency)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 3: Demographic, Gender & Religious Disambiguation     │
│   • Empirical Gender Classification (Male / Female / Neutral)│
│   • Religious Distribution (Muslim / Christian / Neutral)   │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Linguistic Enrichment)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 4: Linguistic, Tashkeel, Meaning & Transliteration    │
│   • Full Arabic Diacritization (التشكيل الكامل)             │
│   • Etymology and Semantic Meaning in AR and EN             │
│   • Phonetic Transliterations and Common Variants           │
│   • 54,000+ Orthographic Mistake Correction Pairs           │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Binary Compaction)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 5: Production Engine Bundle (`names.json.gz`)         │
│   • 33,117 Curated Canonical Names                          │
│   • 1.6 MB Gzipped Zero-Dependency JSON Engine              │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Pipeline Files in this Directory

| File | Description | Sample Record |
|---|---|---|
| [`pipeline/phase1_segmented_sample.csv`](file:///Volumes/MAC/Development/Personal/Egyptian%20Names/library%20building/data/pipeline/phase1_segmented_sample.csv) | Phase 1 Tokenized Lineage Segments | Unspaced/spaced token extractions |
| [`pipeline/phase2_slot_analysis_sample.csv`](file:///Volumes/MAC/Development/Personal/Egyptian%20Names/library%20building/data/pipeline/phase2_slot_analysis_sample.csv) | Phase 2 Slot 1-6 Positional Probabilities | `first_name_count`, `second_name_count`, `slot_pcts` |
| [`pipeline/phase4_annotated_sample.csv`](file:///Volumes/MAC/Development/Personal/Egyptian%20Names/library%20building/data/pipeline/phase4_annotated_sample.csv) | Phase 4 Full Linguistic & Semantic Annotations | Meanings, Tashkeel, Religious markers |
| [`names.json.gz`](file:///Volumes/MAC/Development/Personal/Egyptian%20Names/library%20building/data/names.json.gz) | Phase 5 Production Gzipped Bundle (33,117 entries) | Embedded in Python, Node, .NET, Dart, Java, C++ |

---

## Statistical Highlights

- **Total Analyzed Name Entries**: `33,117` canonical names
- **Corpus Coverage**: Over 99.4% of contemporary Egyptian national names
- **Correction Index**: `54,000+` spelling error and colloquial variation mapping pairs
- **Slot Distribution**: Complete positional matrix across 6 patronymic depth levels
- **Zero Hallucination Guarantee**: Every entry is derived from verified empirical registry frequency.

---

## Ethical Standards & Privacy

All datasets provided in this repository are strictly aggregated statistical frequency models and morphological dictionaries. No personally identifiable information (PII), national IDs, dates of birth, or individual-level records are included or distributed.
