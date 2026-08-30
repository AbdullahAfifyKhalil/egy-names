## 0.3.5

- Fix: English and Arabic-variant key collisions — a rare misspelling could shadow a common lemma's own canonical spelling or steal its English key. The higher corpus-share lemma always wins now.
- Fix: `detect_gender`/`detect_religion` now key off the first personal, non-lineage token instead of a whole-name majority vote; a father's or family's community can no longer outvote the person.
- Fix: multi-word compound lemmas (kunya "Abu X", "Ahmed Saad-El-Din") are recognized as one token by `split`/`detect_gender`/`detect_religion`, not two meaningless fragments.
- Fix: `is_valid`/`generate` now exclude non-personal catalog rows (e.g. "الله") and low-confidence/fabricated filler entries.
- Fix: corrected ~100 malformed compound spellings and one mislabeled gender in the catalog.
- New: shared `logic_config.json` — every threshold/rule list is now data, synced across SDKs from one source.

## 0.3.4

- Catalog: `Youakeem` is an English spelling of يواقيم.

## 0.3.3

- Resolve `names.json.gz` from the installed package, not the app working directory.

## 0.3.2

- Edge-case hardening, whitespace safety, and full stress-test validation.

## 0.3.1

- Expanded canonical dataset to 44,626 Egyptian names derived from 15.88M+ records.
- Added 14-dimensional onomastic intelligence features.
- Bilingual authentic Egyptian pet names (أسماء الدلع) with Arabic lemmas, full Egyptian Tashkeel, English transliteration, and IPA phonetics.
- Added structured descriptions for iconic Egyptian public figures (الاسماء المشهورة) in Arabic and English.
- Added Semitic/Coptic root extraction, origin stratification, and sociological generation trends.
- Added Modern Standard & Egyptian Colloquial IPA phonetic transcriptions.

## 0.1.1

- Comprehensive onomastic dataset with 33,117 Egyptian name lemmas and 134,000+ lookup keys.
- Culturally authentic name generation with slot-weighted sampling.
- Bidirectional Arabic <-> English name translation.
- Dynamic programming segmentation for concatenated Arabic names.
- Orthographic correction with 54,000+ correction pairs and phonetic alif maqsura normalization.
- Full diacritization (tashkeel) with compound name support.
- Linguistic and demographic metadata annotation (gender, religion, frequency, etymology).
- Patronymic chain analysis, generational slot role identification, and uniqueness scoring.
