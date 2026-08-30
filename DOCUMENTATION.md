# Egyptian Names (`egy-names`) — Complete API Reference & Documentation

Welcome to the definitive developer guide for **Egyptian Names (`egy-names`)**, the production-grade onomastic intelligence engine for Egyptian names — offline across eight languages, with a Faker companion and Hugging Face datasets.

The full product page — origin, process, insights, interactive lab, examples, and demo — is at **[afify.co/egy-names](https://afify.co/egy-names)**.

The story of the 14-dimensional engine: **[The Secret Code of Egyptian Names](https://medium.com/@abdullah.afify/the-secret-code-of-egyptian-names-how-we-engineered-a-14-dimensional-nlp-engine-5205db7f04f4)**.

The book comes from real records, not invention. It is as tight as those records allow. Some names will still come back wrong — a rare spelling, a name the catalog has never seen, an edge we have not hit yet. Names outside the book go through the [fallback model](https://huggingface.co/Abdullah-afify/egy-names-fallback-classifier). Every guess is marked `inferred`. If it is not sure, it abstains. We keep tightening the book and the model. If you find one, [open an issue](https://github.com/AbdullahAfifyKhalil/egy-names/issues).

---

## Table of Contents

1. [Architectural Overview & 14D Schema](#1-architectural-overview--14d-schema)
2. [Multi-Language Installation](#2-multi-language-installation)
3. [Core Feature API Reference](#3-core-feature-api-reference)
   - [3.1 Name Generation & Grounded Patronymics (`generate`)](#31-name-generation--grounded-patronymics)
   - [3.2 Bidirectional Egyptian Transliteration (`translate`)](#32-bidirectional-egyptian-transliteration)
   - [3.3 Dynamic Programming Splitting (`split`)](#33-dynamic-programming-splitting)
   - [3.4 Orthographic & Typo Correction (`correct`)](#34-orthographic--typo-correction)
   - [3.5 Dual Arabic Vocalization (`tashkeel`, `tashkeel_standard`, `tashkeel_eg`)](#35-dual-arabic-vocalization)
   - [3.6 International Phonetic Alphabet (`ipa`, `ipa_standard`, `ipa_eg`)](#36-international-phonetic-alphabet-ipa)
   - [3.7 Authentic Egyptian Pet Names (`dallaa`, `dallaa_info`)](#37-authentic-egyptian-pet-names-أسماء-الدلع)
   - [3.8 Iconic Egyptian Public Figures (`famous_figures`)](#38-iconic-egyptian-public-figures-الأسماء-المشهورة)
   - [3.9 Generational Age Intelligence (`detect_age`, `names_for_age`, `age_profile`)](#39-generational-age-intelligence)
   - [3.10 Bayesian Gender & Religion Detection (`detect_gender`, `detect_religion`)](#310-bayesian-gender--religion-detection)
   - [3.11 Deep Morphological Etymology & Annotation (`annotate`, `info`, `meaning`)](#311-deep-morphological-etymology--annotation)
   - [3.12 Multi-Criteria Onomastic Search (`search`)](#312-multi-criteria-onomastic-search)
   - [3.13 Patronymic Chain Decomposition & Formatting (`analyze_chain`, `format_name`)](#313-patronymic-chain-decomposition--formatting)
   - [3.14 Frequency Ranking & Rarity Metrics (`rank`, `uniqueness`)](#314-frequency-ranking--rarity-metrics)
   - [3.15 High-Throughput Batch Processing (`batch`)](#315-high-throughput-batch-processing)
   - [3.16 Validity, compounds, and fallback identification (`is_valid`, `identify`, `identify_all`)](#316-validity-compounds-and-fallback-identification)
4. [Cross-Language SDK Code Reference (Python, TS, PHP, Dart, Swift, Java, C#, C++, Faker)](#4-cross-language-sdk-code-reference)
5. [Data Types & Models Reference](#5-data-types--models-reference)
6. [Performance, Concurrency & Security](#6-performance-concurrency--security)
7. [Faker Companion (`faker-egy-names`)](#7-faker-companion-faker-egy-names)
8. [Hugging Face dataset and fallback model](#8-hugging-face-dataset-and-fallback-model)

---

## 1. Architectural Overview & 14D Schema

Unlike Western personal names (*Given + Surname*), Egyptian naming is governed by an **unbroken patronymic genealogical chain**:
$$\text{Full Legal Name} = \text{Personal Name} \to \text{Father} \to \text{Grandfather} \to \text{Great-Grandfather} \to \text{Family Surname / Clan}$$

`egy-names` is trained on an empirical national corpus of **15.88M+ verified records** across all 27 Egyptian Governorates, yielding a canonical dictionary of **44,626 unique master lemmas** annotated with 14 linguistic and demographic dimensions:

| Dimension | Key | Type | Description | Example (`محمد`) |
| :--- | :--- | :--- | :--- | :--- |
| **Arabic Lemma** | `ar` | `string` | Canonical Arabic surface form | `محمد` |
| **English Transliteration** | `en` | `string` | Official Egyptian passport transliteration | `Mohamed` |
| **Gender** | `gender` | `enum` | Empirical demographic classification (`male`, `female`, `neutral`) | `male` |
| **Religion** | `religion` | `enum` | Cultural religious marker (`muslim`, `christian`, `neutral`) | `muslim` |
| **Name Role** | `role` | `enum` | Onomastic role (`given`, `family`, `kunya`, `tribal`) | `given` |
| **Standard Tashkeel** | `tashkeel_standard` | `string` | Modern Standard Arabic full diacritization | `مُحَمَّد` |
| **Egyptian Tashkeel** | `tashkeel_eg` | `string` | Egyptian Colloquial Arabic vocalization | `مُحَمَّدْ` |
| **Standard IPA** | `ipa_standard` | `string` | Modern Standard Arabic IPA phonetics | `/muħamːad/` |
| **Egyptian IPA** | `ipa_eg` | `string` | Egyptian Colloquial Arabic IPA phonetics | `[moˈħamːæd]` |
| **Arabic Meaning** | `meaning_ar` | `string` | Morphological root, pattern weight & context definition | *المحمود؛ كثير الخصال المحمودة (من الجذر ح م د)* |
| **English Meaning** | `meaning_en` | `string` | Etymology, root and literal translation in English | *The praised one; frequently praised* |
| **Dalla' (Pet Names)** | `dallaa` | `PetName[]` | Authentic Egyptian pet names (Arabic, Tashkeel, EN, IPA) | `مِيدُو [ˈmiːdu]`, `حَمُّو [ˈħæm.mu]` |
| **Famous Figures** | `famous_figures` | `string[]` | Authentic Egyptian public figures & concise role summaries | *محمد صلاح (قائد منتخب مصر وهداف ليفربول العالمي)* |
| **Morphological Root** | `root` | `string` | Semitic/Coptic morphological root | `ح-م-د` |
| **Origin Strata** | `origin_type` | `string` | Etymological stratum (`arabic_classical`, `coptic_pharaonic`, etc.) | `arabic_classical` |
| **Generation Trend** | `trend_category` | `string` | Cultural era trend (`classic_timeless`, `rising_modern`, etc.) | `classic_timeless` |
| **Slot Percentages** | `slot_pcts` | `float[8]` | Probability distribution across genealogical slots 1 to 8 | `[26.91, 31.77, 28.84, 7.19, ...]` |
| **Corpus Share** | `corpus_share` | `float` | Exact national frequency percentage | `0.179624` |

---

## 2. Multi-Language Installation

### Python
```bash
pip install egy-names==0.3.6
```

Faker test suites can install the companion instead of calling `generate()` directly:

```bash
pip install faker-egy-names==0.1.2
```

See [§7 Faker Companion](#7-faker-companion-faker-egy-names).

### PHP (8.1+)
```bash
composer require afify/egy-names:^0.3.6
```

Packagist: [`afify/egy-names`](https://packagist.org/packages/afify/egy-names).

Faker test suites:

```bash
composer require afify/faker-egy-names:^0.1.2
```

See [§4 PHP](#php-81) and [§7.5 PHP](#75-php-fakerphp).

### TypeScript / JavaScript (Node.js & Browsers)
```bash
npm install egy-names@0.3.6
# or: yarn add egy-names / pnpm add egy-names
```

### Dart / Flutter
```bash
dart pub add egy_names:^0.3.6
# or: flutter pub add egy_names:^0.3.6
# or in pubspec.yaml: egy_names: ^0.3.6
```

### Swift (iOS, macOS, watchOS, visionOS)
In Xcode: **File → Add Package Dependencies...** with `https://github.com/AbdullahAfifyKhalil/egy-names.git` (Version `0.3.6`).
Or in `Package.swift`:
```swift
dependencies: [
    .package(url: "https://github.com/AbdullahAfifyKhalil/egy-names.git", from: "0.3.6")
]
```

### Java / Kotlin (Maven / Gradle via JitPack)
**Gradle:**
```groovy
repositories { maven { url 'https://jitpack.io' } }
dependencies { implementation 'com.github.AbdullahAfifyKhalil.egy-names:egy-names:v0.3.6' }
```
**Maven:**
```xml
<dependency>
    <groupId>com.github.AbdullahAfifyKhalil.egy-names</groupId>
    <artifactId>egy-names</artifactId>
    <version>v0.3.6</version>
</dependency>
```

### .NET / C#
```bash
dotnet add package egy-names --version 0.3.6
```

### C++ (Modern C++17/C++20 via CMake FetchContent)
```cmake
include(FetchContent)
FetchContent_Declare(
    egy_names
    GIT_REPOSITORY https://github.com/AbdullahAfifyKhalil/egy-names.git
    GIT_TAG v0.3.7
    SOURCE_SUBDIR cpp/egy_names
)
FetchContent_MakeAvailable(egy_names)
target_link_libraries(your_app PRIVATE egy_names)
```

---

## 3. Core Feature API Reference

### 3.1 Name Generation & Grounded Patronymics

Generates culturally authentic Egyptian full names using a **joint multi-variate transition graph over 6 genealogical positions**.

#### Signature:
- **Python**: `en.generate(count=1, gender=None, religion=None, length=None, family_name=True, frequency=None, seed=None) -> List[GeneratedName]`
- **TypeScript**: `en.generate({ count?: number, gender?: Gender, religion?: Religion, length?: number, familyName?: boolean, frequency?: FrequencyClass, seed?: number }) -> GeneratedName[]`
- **Dart**: `en.generate({ int count = 1, String? gender, String? religion, int? length, bool familyName = true, String? frequency, int? seed }) -> List<GeneratedName>`
- **Swift**: `en.generate(count: Int = 1, gender: String? = nil, religion: String? = nil, length: Int? = nil, familyName: Bool = true, frequency: String? = nil, seed: Int? = nil) -> [GeneratedName]`
- **Java**: `en.generate(int count, String gender, String religion, Integer length, boolean familyName, String frequency, Integer seed) -> List<GeneratedName>`
- **C#**: `en.Generate(count: 1, gender: null, religion: null, length: null, familyName: true, frequency: null, seed: null) -> List<GeneratedName>`
- **C++**: `en.generate(count, gender, religion, length, family_name, frequency, seed) -> std::vector<GeneratedName>`

#### Parameters:
- `count` *(int, default=1)*: Number of full name chains to synthesize.
- `gender` *(string/enum, optional)*: `"male"` (`"m"`) or `"female"` (`"f"`). Determines Slot 1 personal name.
- `religion` *(string/enum, optional)*: `"muslim"` (`"m"`) or `"christian"` (`"c"`). Enforces religious continuity across all ancestral slots.
- `length` *(int, optional, 2–8)*: Number of patronymic slots in the chain (default varies organically between 3 and 5).
- `family_name` / `familyName` *(bool, default=True)*: When `True`, the final slot samples from verified Egyptian clan/toponymic surnames.
- `frequency` *(string/enum, optional)*: `"common"`, `"normal"`, or `"rare"`.
- `seed` *(int, optional)*: Deterministic pseudo-random seed for reproducible tests.

#### Example:
```python
# Generate 3 Female Christian Egyptian names of 4 parts
names = en.generate(count=3, gender="female", religion="christian", length=4)
for n in names:
    print(f"{n.ar}  |  {n.en}")
# Output:
# مريم فوزي سمعان الصايغ  |  Maryam Fawzy Semaan El Sayegh
# ساندرا نبيل كمال الشرقاوي  |  Sandra Nabil Kamal Elsharkawy
# دميانة إبراهيم فرج مرقص  |  Demyana Ibrahim Farag Morcos
```

---

### 3.2 Bidirectional Egyptian Transliteration

Translates full patronymic names and single tokens bidirectionally between Arabic and English adhering strictly to **Egyptian Civil Registry phonetic conventions** (`ج` $\to$ `G`, `ح` $\to$ `H`, `الـ` $\to$ `El-`, `عبد` $\to$ `Abdel-`, `أبو` $\to$ `Abou-`).

#### Signature:
- `en.translate(name, to=None)`
- `en.translate_token(token, to=None)`

#### Parameters:
- `name` *(string)*: Name chain in Arabic or English.
- `to` *(string, optional)*: Target language (`"ar"` or `"en"`). If omitted, automatically detects source language and translates to the opposite.

#### Example:
```python
# Arabic to Egyptian English:
en.translate("محمد عبد الحميد الشاذلي")  # "Mohamed Abdelhamid Elshazly"
en.translate("جمال جورج عبد المسيح")    # "Gamal George Abdelmassih"

# English to Arabic:
en.translate("Youssef Hesham Mahmoud Elmasry")  # "يوسف هشام محمود المصري"
```

---

### 3.3 Dynamic Programming Splitting

Decomposes unspaced Arabic text strings into their constituent patronymic tokens using **Unicode codepoint lattice shortest-path optimization** in **$< 0.05\text{ ms}$**.

#### Signature:
- `en.split(name) -> List[str]`

#### Example:
```python
# Unspaced legacy bank/civil registry string:
en.split("محمدأحمدعليحسنالشناوي")
# Returns: ['محمد', 'أحمد', 'علي', 'حسن', 'الشناوي']

# Handles unspaced compounds seamlessly:
en.split("عبدالرحمننورالدينالبسيوني")
# Returns: ['عبدالرحمن', 'نورالدين', 'البسيوني']
```

---

### 3.4 Orthographic & Typo Correction

Applies an $O(1)$ in-memory hash trie of **23,457 deterministic spelling and OCR correction rules** extracted from 15.88M+ real-world records.

#### Signature:
- `en.correct(name) -> str`

#### Corrects:
- **Alif Maqsura vs. Ya**: <code><bdi>مصطفا</bdi></code>&lrm; → <code><bdi>مصطفى</bdi></code>
- **Alif Maqsura vs. Ya**: <code><bdi>يحي</bdi></code>&lrm; → <code><bdi>يحيى</bdi></code>
- **Hamza Normalization**: <code><bdi>احمد</bdi></code>&lrm; → <code><bdi>أحمد</bdi></code>
- **Hamza Normalization**: <code><bdi>اسماعيل</bdi></code>&lrm; → <code><bdi>إسماعيل</bdi></code>
- **Ta Marbuta vs. Ha**: <code><bdi>فاطمه</bdi></code>&lrm; → <code><bdi>فاطمة</bdi></code>
- **Ta Marbuta vs. Ha**: <code><bdi>مروه</bdi></code>&lrm; → <code><bdi>مروة</bdi></code>
- **Compound Fusion**: <code><bdi>عبد الرحمن</bdi></code>&lrm; → <code><bdi>عبدالرحمن</bdi></code>
- **Typographical Slips**: <code><bdi>محمودد</bdi></code>&lrm; → <code><bdi>محمود</bdi></code>
- **Typographical Slips**: <code><bdi>ابراهم</bdi></code>&lrm; → <code><bdi>إبراهيم</bdi></code>

#### Example:
```python
en.correct("احمد مصطفا عبد الرحيم يحي")
# Returns: "أحمد مصطفى عبدالرحيم يحيى"
```

---

### 3.5 Dual Arabic Vocalization

Provides two distinct phonetic Tashkeel diacritizations:
1. **Standard Tashkeel (`tashkeel_standard`)**: Modern Standard Arabic (Classical Fusha).
2. **Egyptian Tashkeel (`tashkeel_eg`)**: Contemporary Egyptian Colloquial vocalization.

#### Signature:
- `en.tashkeel(name) -> str` (Default standard vocalization)
- `en.tashkeel_standard(name) -> str`
- `en.tashkeel_eg(name) -> str`

#### Example:
```python
en.tashkeel("محمد عبدالرحمن الشرقاوي")
# -> "مُحَمَّد عَبْدُ الرَّحْمَن الشَّرْقَاوِيّ"

en.tashkeel_eg("محمد")
# -> "مُحَمَّدْ" (Egyptian voweling with final sukun/cadence)
```

---

### 3.6 International Phonetic Alphabet (IPA)

Generates precision International Phonetic Alphabet transcriptions designed for **AI Text-to-Speech (TTS)**, linguistic research, and non-native pronunciation assistance.

#### Signature:
- `en.ipa(name, dialect="eg") -> str`
- `en.ipa_standard(name) -> str`
- `en.ipa_eg(name) -> str`

#### Example:
```python
en.ipa_standard("جمال")  # "/d͡ʒamaːl/" (Modern Standard Arabic)
en.ipa_eg("جمال")        # "[ɡæˈمæːl]" (Egyptian Colloquial Arabic)

en.ipa_eg("محمد")        # "[moˈħamːæd]"
en.ipa_eg("آيات")        # "[ʔæˈjæːt]"
```

---

### 3.7 Authentic Egyptian Pet Names (أسماء الدلع)

Returns culturally authentic Egyptian pet names formatted in plain Arabic, vocalized Tashkeel, English transliteration, or Egyptian IPA.

#### Signature:
- `en.dallaa(name, format="plain") -> List[str]` (`format`: `"plain"` | `"tashkeel"` | `"en"` | `"ipa"`)
- `en.dallaa_info(name) -> List[PetName]`

#### Example:
```python
# Plain Arabic:
en.dallaa("محمد")
# -> ['ميدو', 'حمو', 'حمودة']

# Egyptian Vocalized Tashkeel:
en.dallaa("محمد", format="tashkeel")
# -> ['مِيدُو', 'حَمُّو', 'حَمُّودَة']

# Transliterated English:
en.dallaa("محمد", format="en")
# -> ['Mido', 'Hamou', 'Hamouda']

# Egyptian Colloquial IPA:
en.dallaa("محمد", format="ipa")
# -> ['[ˈmiːdu]', '[ˈħæm.mu]', '[ħæmˈmuːdæ]']

# Structured Objects:
for pet in en.dallaa_info("محمد"):
    print(pet.ar, pet.tashkeel, pet.en, pet.ipa)
# ميدو مِيدُو Mido [ˈmiːdu]
# حمو حَمُّو Hamou [ˈħæm.mu]
# حمودة حَمُّودَة Hamouda [ħæmˈmuːdæ]
```

---

### 3.8 Iconic Egyptian Public Figures (الأسماء المشهورة)

Retrieves notable historic and contemporary Egyptian icons sharing the name, complete with structured role descriptions in Arabic or English.

#### Signature:
- `en.famous_figures(name, lang="ar") -> List[str]` (`lang`: `"ar"` | `"en"`)

#### Example:
```python
en.famous_figures("محمد", lang="ar")
# Output:
# [
#   'محمد صلاح (قائد منتخب مصر وهداف ليفربول العالمي)',
#   'محمد علي باشا (مؤسس مصر الحديثة)',
#   'محمد أنور السادات (رئيس جمهورية مصر العربية الأسبق وبطل الحرب والسلام)',
#   'محمد عبد الوهاب (موسيقار الأجيال ورائد الموسيقى العربية الحديثة)'
# ]

en.famous_figures("محمد", lang="en")
# Output:
# [
#   'Mohamed Salah (Egyptian National Football Captain & Global Icon)',
#   'Mohamed Ali Pasha (Founder of Modern Egypt)',
#   'Mohamed Anwar El Sadat (Former Egyptian President & Nobel Peace Laureate)',
#   'Mohamed Abdel Wahab (Legendary Composer & Pioneer of Modern Arabic Music)'
# ]
```

---

### 3.9 Generational Age Intelligence

Leverages a continuous Gaussian demographic model over 5 national examination cohorts to estimate birth cohorts, generations, and ages.

#### Signature:
- `en.detect_age(chain) -> AgeDetection`
- `en.names_for_age(target_age, gender=None, top=10) -> List[NameInfo]`
- `en.age_profile(name) -> AgeProfile`

#### Example:
```python
# Estimate person age from full patronymic chain:
det = en.detect_age("كريم أشرف فاروق")
print(det.estimated_age)     # ~25
print(det.age_range)         # (13, 37)
print(det.generation_label)  # "youth generation (Gen Z / Millennials)"
print(det.confidence)        # 0.641 (boosted by cross-generational alignment)

# Find top names for a specific age cohort:
top_youth = en.names_for_age(24, gender="female", top=3)
# -> [NameInfo(ar='شهد', ...), NameInfo(ar='يارا', ...), NameInfo(ar='مريم', ...)]
```

---

### 3.10 Bayesian Gender & Religion Detection

Reads the first personal, non-lineage token. A father's or family's community does not outvote the person. Two-word compounds (kunya `أبو X`, `أحمد سعدالدين`) count as one token.

#### Signature:
- `en.detect_gender(name) -> GenderDetection`
- `en.detect_religion(name) -> ReligionDetection`

#### Example:
```python
# Gender: first given name wins
en.detect_gender("فاطمة محمد علي حسن")
# -> GenderDetection(gender='female', ...)

en.detect_gender("مريم إبراهيم حسن")
# -> GenderDetection(gender='female', confidence=0.98, method='slot_weighted')

# Religion: first distinctive token wins
en.detect_religion("جورج علاءالدين عبدالمسيح دغيدي")
# -> ReligionDetection(religion='christian', ...)

en.detect_religion("جورج بطرس سمير ميخائيل")
# -> ReligionDetection(religion='christian', confidence=0.99)

en.detect_religion("محمد أحمد علي")
# -> ReligionDetection(religion='muslim', confidence=0.99)
```

---

### 3.11 Deep Morphological Etymology & Annotation

Retrieves full onomastic metadata (`NameInfo`) for any Arabic or English name.

#### Signature:
- `en.annotate(name) -> Union[NameInfo, List[NameInfo], None]`
- `en.info(name) -> Optional[NameInfo]`
- `en.meaning(name) -> Dict[str, str]`

#### Example:
```python
info = en.info("محمد")
print(info.ar)                # "محمد"
print(info.en)                # "Mohamed"
print(info.gender)            # Gender.MALE
print(info.religion)          # Religion.MUSLIM
print(info.role)              # NameRole.GIVEN
print(info.tashkeel_standard) # "مُحَمَّد"
print(info.tashkeel_eg)       # "مُحَمَّدْ"
print(info.ipa_standard)      # "/muħamːad/"
print(info.ipa_eg)            # "[moˈħamːæd]"
print(info.root)              # "ح-م-د"
print(info.origin_type)       # "arabic_classical"
print(info.trend_category)    # "classic_timeless"
print(info.meaning_ar)        # "المحمود؛ كثير الخصال المحمودة..."
print(info.meaning_en)        # "The praised one; frequently praised..."
print(info.slot_pcts)         # [26.91, 31.77, 28.84, 7.19, 4.54, 0.72, 0.04, 0.0]
print(info.corpus_share)      # 0.179624
```

---

### 3.12 Multi-Criteria Onomastic Search

Searches the 44,626 canonical entries with filtering by prefix, infix, suffix, gender, religion, origin, and trend.

#### Signature:
- `en.search(query=None, starts_with=None, ends_with=None, contains=None, gender=None, religion=None, origin_type=None, trend_category=None, max_results=50) -> List[NameInfo]`

#### Example:
```python
# Search for female Coptic names:
results = en.search(gender="female", religion="christian", max_results=5)

# Search names starting with "عبد":
results = en.search(starts_with="عبد", max_results=10)
```

---

### 3.13 Patronymic Chain Decomposition & Formatting

Assigns explicit patronymic roles (`person`, `father`, `grandfather`, `ancestor`, `family_name`) to every slot in a full name chain.

#### Signature:
- `en.analyze_chain(chain) -> List[ChainPart]`
- `en.format_name(chain, pattern="{person} {father} {family}") -> str`

#### Example:
```python
parts = en.analyze_chain("محمد أحمد علي حسن الشاذلي")
for p in parts:
    print(f"Slot {p.slot_index}: {p.name} ({p.role.value})")
# Slot 1: محمد (person)
# Slot 2: أحمد (father)
# Slot 3: علي (grandfather)
# Slot 4: حسن (ancestor)
# Slot 5: الشاذلي (family_name)

# Custom formatting:
en.format_name("محمد أحمد علي حسن الشاذلي", "{person} {father} {family}")
# -> "محمد أحمد الشاذلي"
```

---

### 3.14 Frequency Ranking & Rarity Metrics

Calculates national corpus frequency rank, rarity percentile, and classification (`common`, `normal`, `rare`).

#### Signature:
- `en.rank(name) -> Optional[RankInfo]`
- `en.uniqueness(name) -> Optional[UniquenessScore]`

#### Example:
```python
rank = en.rank("محمد")
print(f"Rank #{rank.national_rank} of 44,626 (Top {rank.percentile}%)")
# -> Rank #1 of 44,626 (Top 99.99%)

uniq = en.uniqueness("مهرائيل")
print(f"Uniqueness score: {uniq.score}/100 | {uniq.classification}")
# -> Uniqueness score: 87.4/100 | rare heritage name
```

---

### 3.15 High-Throughput Batch Processing

Vectorized processing for large datasets and dataframe ingestion:

```python
en.batch.translate(["محمد أحمد", "يارا عادل", "مينا بطرس"])
# -> ['Mohamed Ahmed', 'Yara Adel', 'Mina Boutros']

en.batch.correct(["احمد مصطفا", "اسماعيل فاطمه"])
# -> ['أحمد مصطفى', 'إسماعيل فاطمة']

en.batch.tashkeel(["محمد", "فاطمة", "علي"])
# -> ['مُحَمَّد', 'فَاطِمَة', 'عَلِيّ']
```

---

### 3.16 Validity, compounds, and fallback identification

`is_valid` is true only for a personal, attested lemma. Non-person catalog rows (`الله`) and low-confidence filler stay in the index for `split` / lookup, but they are not valid names and `generate` will not emit them.

`identify` / `identify_all` try the book first. On a miss, the Python SDK runs the [fallback classifier](https://huggingface.co/Abdullah-afify/egy-names-fallback-classifier). Every fallback answer is marked `inferred: true`. Below the calibrated threshold it returns `unknown` / `neutral` instead of guessing.

#### Signature:
- `en.is_valid(name) -> bool`
- `en.identify(name) -> Optional[InferredName]` *(Python)*
- `en.identify_all(full_name) -> List[InferredName]` *(Python; always a list)*

#### Example:
```python
en.is_valid("محمد")   # True
en.is_valid("الله")   # False — in the index, not a person's name
en.lookup("الله")     # still resolves, so compounds can split

# Book hit: inferred is False
en.identify("محمد")

# Book miss: fallback model, marked inferred
en.identify_all("محمد زوكرمانوفيتش")
```

---

## 4. Cross-Language SDK Code Reference

### PHP (8.1+)
```php
use Afify\EgyNames\EgyNames;

$en = new EgyNames();
$names = $en->generate(count: 5, gender: 'female', religion: 'muslim');
echo $en->translate('محمد أحمد علي');
print_r($en->split('محمدأحمدعليحسنالشناوي'));
echo $en->tashkeel('محمد عبدالرحمن');
echo $en->correct('احمد مصطفا');
print_r($en->dallaa('محمد', 'tashkeel'));
```

Source: [`php/egy-names/`](php/egy-names/) · [GitHub](https://github.com/AbdullahAfifyKhalil/egy-names-php) · [Packagist](https://packagist.org/packages/afify/egy-names).

### TypeScript / JavaScript (Node.js & ESM/CJS)
```typescript
import { EgyNames, Gender, Religion } from "egy-names";
const en = new EgyNames();

// 1. Generation
const names = en.generate({ count: 5, gender: Gender.FEMALE, religion: Religion.MUSLIM });

// 2. Transliteration & Splitting
console.log(en.translate("محمد أحمد علي")); // "Mohamed Ahmed Ali"
console.log(en.split("محمدأحمدعليحسنالشناوي")); // ["محمد", "أحمد", "علي", "حسن", "الشناوي"]

// 3. Tashkeel & IPA
console.log(en.tashkeel("محمد عبدالرحمن")); // "مُحَمَّد عَبْدُ الرَّحْمَن"
console.log(en.ipaEg("محمد")); // "[moˈħamːæd]"

// 4. Pet Names & Figures
console.log(en.dallaa("محمد", "tashkeel")); // ['مِيدُو', 'حَمُّو', 'حَمُّودَة']
console.log(en.famousFigures("محمد", "en")); // ['Mohamed Salah (Egyptian National Football Captain & Global Icon)', ...]
```

### Dart / Flutter
```dart
import 'package:egy_names/egy_names.dart';
final en = EgyNames();

// Generation & Transliteration
final names = en.generate(count: 3, gender: 'female');
final translated = en.translate('محمد أحمد علي');

// 14D Features
final petNames = en.dallaa('محمد', format: 'ipa'); // ['[ˈmiːdu]', '[ˈħæm.mu]', '[ħæmˈmuːdæ]']
final figures = en.famousFigures('محمد', lang: 'ar');
final ipa = en.ipaEg('محمد'); // '[moˈħamːæd]'
```

### Swift (iOS / macOS)
```swift
import EgyNames
let en = EgyptianNames()

let generated = en.generate(count: 3, gender: "male", religion: "muslim")
let translated = en.translate("محمد أحمد علي")
let parts = en.split("محمدأحمدعليحسن")

let petNames = en.dallaa("محمد", format: "tashkeel")
let figures = en.famousFigures("محمد", lang: "en")
```

### Java / Kotlin (Android / Spring)
```java
import com.afify.egynames.EgyptianNames;
import com.afify.egynames.model.Models.*;

EgyptianNames en = new EgyptianNames();
List<GeneratedName> names = en.generate(5, "female", "muslim", 4, true, null, null);
List<String> dallaa = en.dallaa("محمد", "tashkeel");
List<String> figures = en.famousFigures("محمد", "en");
```

### C# (.NET Core / ASP.NET)
```csharp
using EgyNames;

var en = new EgyptianNamesEngine();
var names = en.Generate(count: 3, gender: "female");
var translated = en.Translate("محمد أحمد علي");
var petNames = en.Dallaa("محمد", "tashkeel");
var figures = en.FamousFigures("محمد", "en");
```

### C++ (Modern C++17/C++20)
```cpp
#include <egy_names/egy_names.hpp>
#include <iostream>

egy_names::EgyptianNames en;
auto names = en.generate(3, "female", "muslim");
auto translation = en.translate("محمد أحمد علي");
auto pet_names = en.dallaa("محمد", "tashkeel");
auto figures = en.famous_figures("محمد", "en");
```

### Faker (Python companion)
```python
from faker_egy_names import egyptian_faker

fake = egyptian_faker()
name = fake.egyptian_name(gender="female", religion="muslim", length=4)
print(name.ar, name.en)
print(fake.egyptian_full_name("ar"))
print(fake.egyptian_person(), fake.egyptian_father(), fake.egyptian_family())
```

See [§7 Faker Companion](#7-faker-companion-faker-egy-names) for the full method reference.

---

## 5. Data Types & Models Reference

### `PetName`
```typescript
interface PetName {
  ar: string;        // 'ميدو'
  tashkeel: string;  // 'مِيدُو'
  en: string;        // 'Mido'
  ipa: string;       // '[ˈmiːdu]'
}
```

### `NameInfo`
```typescript
interface NameInfo {
  ar: string;
  en: string;
  gender: Gender;
  religion: Religion;
  role: NameRole;
  arVariants: string[];
  enVariants: string[];
  slotPcts: number[];
  corpusShare: number;
  frequency: FrequencyClass;
  tashkeelStandard: string;
  tashkeelEg: string;
  ipaStandard: string;
  ipaEg: string;
  meaningAr: string;
  meaningEn: string;
  dallaa: string[];
  dallaaAr: string[];
  dallaaTashkeel: string[];
  dallaaEn: string[];
  dallaaIpa: string[];
  root: string;
  originType: string;
  famousFigures: string[];
  famousFiguresAr: string[];
  famousFiguresEn: string[];
  trendCategory: string;
}
```

---

## 6. Performance, Concurrency & Security

- **In-Memory Zero-Allocation Engine**: All 44,626 entries and 23,457 correction rules are loaded from a compact, gzip-compressed hash trie (~6.89 MB compressed, ~18 MB in-memory).
- **Sub-Microsecond Latency**: Lookups, translations, and DP splits execute in $< 0.05\text{ ms}$.
- **Thread-Safe**: Fully read-only, immutable singleton design across all 8 language SDKs. Safe for high-concurrency HTTP servers, multi-threaded pipelines, and mobile apps.
- **100% Offline & Private**: Zero external API calls, zero telemetry, zero data collection. Meets strict enterprise, banking, and GDPR privacy standards.

---

## 7. Faker Companion (`faker-egy-names`)

Python: [`faker-egy-names`](https://pypi.org/project/faker-egy-names/) **0.1.2** is a separate PyPI package. It does **not** add Faker as a dependency of `egy-names`. Every method forwards to `EgyNames.generate()` from `egy-names>=0.3.6,<0.4`.

PHP: [`afify/faker-egy-names`](https://packagist.org/packages/afify/faker-egy-names) is the same API for [FakerPHP](https://fakerphp.github.io/). The engine is [`afify/egy-names`](https://packagist.org/packages/afify/egy-names). The Faker companion still ships a generate-only catalog so test suites do not have to load the full book. Same methods, same arguments, no `first_name` / `last_name` mapping.

**Install:** `pip install faker-egy-names==0.1.2` · `composer require afify/faker-egy-names:^0.1.2`  
**Source:** [`faker-egy-names/`](faker-egy-names/) · [`faker-egy-names-php/`](faker-egy-names-php/) · [Packagist](https://packagist.org/packages/afify/faker-egy-names)

### 7.1 Registration

```python
from faker import Faker
from faker_egy_names import Provider, egyptian_faker

fake = Faker()
fake.add_provider(Provider)

# or
fake = egyptian_faker()
```

`Faker.seed_instance(n)` is honored unless you pass `seed=` yourself.

### 7.2 Method Reference

| Method | Returns | Description |
| :--- | :--- | :--- |
| `egyptian_name(...)` | `GeneratedName` | One grounded chain: `ar`, `en`, `parts_ar`, `parts_en` |
| `egyptian_full_name(lang="en", ...)` | `str` or `(ar, en)` | Full patronymic name |
| `egyptian_person(lang="en", ...)` | `str` or `(ar, en)` | Slot 1 — the person's given name |
| `egyptian_father(lang="en", ...)` | `str` or `(ar, en)` | Slot 2 — father. Empty if the chain has no father slot |
| `egyptian_grandfather(lang="en", ...)` | `str` or `(ar, en)` | Slot 3 — grandfather. Empty if the chain is too short |
| `egyptian_family(lang="en", ...)` | `str` or `(ar, en)` | Final clan / toponymic surname. Empty when `family_name=False` |

Slot helpers on separate calls are **not** the same person. For one fixture, call `egyptian_name()` once and read `parts_ar` / `parts_en`.

### 7.3 Parameters

Passed through to `egy-names.generate()`:

- `gender` *(string, optional)*: `"male"` or `"female"`.
- `religion` *(string, optional)*: `"muslim"` or `"christian"`.
- `length` *(int, optional, 2–8)*: Number of patronymic slots.
- `family_name` *(bool, default=True)*: When `True`, the final slot is a verified Egyptian surname.
- `frequency` *(string, optional)*: `"common"`, `"normal"`, or `"rare"`.
- `seed` *(int, optional)*: Overrides Faker's RNG for that call.

`lang` is `"en"` (default), `"ar"`, or `"both"` (returns a `(ar, en)` tuple). It is **not** forwarded to the engine — the provider always generates both scripts and selects the requested one.

### 7.4 Example

```python
from faker_egy_names import egyptian_faker

fake = egyptian_faker()
name = fake.egyptian_name(gender="female", religion="muslim", length=4, seed=1)
print(name.ar)        # شهد هاشم نبيل الديب
print(name.en)        # Shahd Hashem Nabil Eldeeb
print(name.parts_en)  # ['Shahd', 'Hashem', 'Nabil', 'Eldeeb']

fake.egyptian_full_name()                 # English full name
fake.egyptian_full_name("ar")             # Arabic full name
fake.egyptian_full_name(lang="both")      # (ar, en)
fake.egyptian_person(gender="male")
fake.egyptian_father()
fake.egyptian_grandfather()
fake.egyptian_family()
```

### 7.5 PHP (FakerPHP)

```php
$fake = egyptian_faker();
$name = $fake->egyptian_name(gender: 'female', religion: 'muslim', length: 4, seed: 1);
echo $name->ar;
echo $name->en;
print_r($name->parts_en);

$fake->egyptian_full_name();
$fake->egyptian_full_name('ar');
$fake->egyptian_full_name(lang: 'both'); // [ar, en]
$fake->egyptian_person(gender: 'male');
$fake->egyptian_father();
$fake->egyptian_grandfather();
$fake->egyptian_family();
```

CamelCase aliases (`egyptianName`, `egyptianFullName`, …) are identical. `$fake->seed(n)` uses FakerPHP's process-wide `mt_srand`. Seeds are not aligned with the Python companion.

---

## 8. Hugging Face dataset and fallback model

Dataset: [Abdullah-afify/egyptian-names](https://huggingface.co/datasets/Abdullah-afify/egyptian-names) — 44,626 canonical lemmas plus the raw/segmented pipeline. Audit columns `is_personal_name` and `is_low_confidence` match what `is_valid` / `generate` use.

Fallback model: [Abdullah-afify/egy-names-fallback-classifier](https://huggingface.co/Abdullah-afify/egy-names-fallback-classifier) — trained on that catalog. Used only when lookup misses. Local cards live in [`huggingface/`](huggingface/) and [`huggingface_model/`](huggingface_model/).

```python
from datasets import load_dataset

dataset = load_dataset("Abdullah-afify/egyptian-names")
print(dataset["train"][0])
```

---

## License

Released under the **MIT License**. Free for commercial, academic, government, and personal use.
© 2026 Abdullah Afify. An Afify open-source project. [afify.co/egy-names](https://afify.co/egy-names)
