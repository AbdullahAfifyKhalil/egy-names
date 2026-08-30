<div align="center">

<img src="https://raw.githubusercontent.com/AbdullahAfifyKhalil/egy-names/main/assets/banner.png" alt="Egyptian Names Banner" width="100%" style="border-radius: 14px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);" />

<img src="https://raw.githubusercontent.com/AbdullahAfifyKhalil/egy-names/main/assets/logo.png" alt="Egyptian Names Logo" width="130" style="border-radius: 28px; box-shadow: 0 12px 36px rgba(0,0,0,0.25); margin-bottom: 12px;" />

# Egyptian Names (`egy-names`)
### *The Production-Grade Onomastic Intelligence Engine for Egyptian Names — offline across 8 languages, plus Faker and Hugging Face*

**[afify.co/egy-names](https://afify.co/egy-names)** — origin, process, insights, interactive lab, examples, and demo.

**[The Secret Code of Egyptian Names](https://medium.com/@abdullah.afify/the-secret-code-of-egyptian-names-how-we-engineered-a-14-dimensional-nlp-engine-5205db7f04f4)** — how the 14-dimensional engine was built.

[![Afify](https://img.shields.io/badge/afify.co-Egy--Names-17191c)](https://afify.co/egy-names)
[![PyPI Version](https://img.shields.io/badge/PyPI-v0.3.5-3776AB)](https://pypi.org/project/egy-names/)
[![Packagist](https://img.shields.io/packagist/v/afify/egy-names.svg?label=Packagist)](https://packagist.org/packages/afify/egy-names)
[![Faker Provider](https://img.shields.io/badge/Faker-faker--egy--names_v0.1.0-563D7C)](https://pypi.org/project/faker-egy-names/)
[![FakerPHP](https://img.shields.io/badge/FakerPHP-afify/faker--egy--names-777BB4)](https://packagist.org/packages/afify/faker-egy-names)
[![npm Version](https://img.shields.io/badge/npm-v0.3.5-CB3837)](https://www.npmjs.com/package/egy-names)
[![pub.dev Version](https://img.shields.io/badge/pub.dev-v0.3.5-0175C2)](https://pub.dev/packages/egy_names)
[![Maven Central](https://img.shields.io/badge/Maven_Central-v0.3.5-C71A36)](https://central.sonatype.com/artifact/io.github.abdullahafifykhalil/egy-names)
[![JitPack](https://img.shields.io/badge/JitPack-v0.3.5-2ECC71)](https://jitpack.io/#AbdullahAfifyKhalil/egy-names/v0.3.5)
[![NuGet Version](https://img.shields.io/badge/NuGet-v0.3.5-004880)](https://www.nuget.org/packages/egy-names/)
[![Swift PM](https://img.shields.io/badge/Swift_PM-v0.3.5-FA7343)](https://github.com/AbdullahAfifyKhalil/egy-names)
[![Hugging Face](https://img.shields.io/badge/Hugging_Face-44.6K_Lexicon-FFD21E)](https://huggingface.co/datasets/Abdullah-afify/egyptian-names)
[![Fallback model](https://img.shields.io/badge/Model-egy--names--fallback--classifier-FFD21E)](https://huggingface.co/Abdullah-afify/egy-names-fallback-classifier)
[![Medium](https://img.shields.io/badge/Medium-14D_Engine-00AB6C)](https://medium.com/@abdullah.afify/the-secret-code-of-egyptian-names-how-we-engineered-a-14-dimensional-nlp-engine-5205db7f04f4)
[![Documentation](https://img.shields.io/badge/Documentation-Complete_API_Reference-blue.svg)](DOCUMENTATION.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Engineered with 100% Deterministic Parity across 8 Major Languages:**
<br />
**Python** | **TypeScript / JavaScript** | **PHP** | **.NET / C#** | **Flutter / Dart** | **Swift (iOS/macOS)** | **Java / Kotlin** | **C++ (C++20/17)** | **Faker** | **Hugging Face**

[Site · origin, lab, demo](https://afify.co/egy-names) | [Complete API Reference & Documentation](DOCUMENTATION.md) | [Why you need this](#why-you-need-this) | [Accuracy](#accuracy) | [Try it in 30 seconds](#try-it-in-30-seconds) | [Why Egyptian Names?](#why-egyptian-names-are-unique-and-computationally-complex) | [Feature Deep Dive](#feature-engineering-deep-dive) | [Grounded Generation Engine](#the-mathematics-of-grounded-patronymic-generation) | [Multi-Language Usage](#installation-and-multi-language-usage) | [Faker Companion](#faker-companion-faker-egy-names) | [Hugging Face](#hugging-face-datasets-and-model) | [Medium](https://medium.com/@abdullah.afify/the-secret-code-of-egyptian-names-how-we-engineered-a-14-dimensional-nlp-engine-5205db7f04f4) | [License](#license)

</div>

---

## Why you need this

Your signup form asks for *first name* and *last name*. An Egyptian user types **أحمد محمد حسن علي الشناوي**. KYC fails. The chatbot calls him *Mr. Shen*. A generic faker invents a girl as someone's father.

Egypt does not use Western surnames. A legal name is a **patronymic chain** — person → father → grandfather → family. Flatten it and you silently corrupt identity for **115 million** people.

`egy-names` is the offline engine trained on **15.8 million** official records. Same input, same output. No network. No hallucination. If you ship forms, KYC, OCR cleanup, test fixtures, or TTS for Egypt — you need this.

## Accuracy

The book comes from real records, not invention. It is as tight as the records allow. Some names will still come back wrong — a rare spelling, a name the catalog has never seen, an edge we have not hit yet. When we guess, we mark it. When we are not sure, we say so. We keep tightening the book and the fallback. If you find one, [open an issue](https://github.com/AbdullahAfifyKhalil/egy-names/issues).

## Try it in 30 seconds

```bash
pip install egy-names==0.3.5
```

```python
from egy_names import EgyNames

e = EgyNames()

# A bank / civil-registry dump with no spaces
print(e.split("محمدأحمدعليحسنالشناوي"))
# ['محمد', 'أحمد', 'علي', 'حسن', 'الشناوي']

# Egyptian passport spelling (Gamal, not Jamal)
print(e.translate("محمد أحمد علي الشناوي"))
# Mohamed Ahmed Ali Elshenawy

# A grounded test person — never a female father
name = e.generate(gender="female", religion="muslim", length=4)[0]
print(f"{name.ar}  —  {name.en}")
```

Need the same names inside existing Faker tests? `pip install faker-egy-names`.

---

## Why Egyptian Names Are Unique and Computationally Complex

Unlike Western naming conventions (*Given Name + Surname*), Egyptian personal naming is governed by an **unbroken patronymic genealogical chain** where an individual's full legal name is an ordered succession of ancestral personal names:

$$\text{Full Legal Name} = \text{Personal Name} \to \text{Father} \to \text{Grandfather} \to \text{Great-Grandfather} \to \text{Family Surname / Clan}$$

This ancient onomastic system—intertwined with **Pharaonic and Coptic substrates**, **Classical Arabic morphology**, **Ottoman Turkish guild surnames**, and **Nile Delta and Upper Egypt geographic toponyms**—presents extraordinary linguistic richness:

### The Egyptian Onomastic Spectrum

| Cultural Heritage | Example Names (Arabic) | Transliteration | Historical and Etymological Origin |
| :--- | :--- | :--- | :--- |
| **Ancient / Coptic Substrate** | مهرائيل , سوريال , بهنس , مينا | *Mehraeil, Soryal, Bahnas, Mina* | Pharaonic theophoric names and Coptic Christian heritage dating back millennia |
| **Classical Islamic / Arabic** | محمد , عبد الرحمن , فاطمة , نور الدين | *Mohamed, Abdelrahman, Fatma, Nour Eldin* | Pure Semitic triliteral roots (h-m-d, a-b-d, f-t-m) and honorific compounds |
| **Ottoman / Turkish Guilds** | بوادقجي , الجوهرجي , شلتوت , خاقان | *Bawadqgy, Gowharji, Shaltout, Khaqan* | Professional trade guilds, military titles, and aristocratic family surnames |
| **Nile Geographic Toponyms** | المنياوي , الطهطاوي , الشناوي , الدمياطي | *Elminyawy, Tahtawy, Elshenawy, Domyaty* | Surnames of geographic attribution across the 27 Governorates of Upper and Lower Egypt |

---

### The 5 Hard Problems Solved by `egy-names`

1. **Unspaced Concatenation in Legacy Databases**: Egyptian civil records and bank databases frequently compress full chains without spaces (`محمدأحمدعليحسنالشناوي`). Standard splitters fail; `egy-names` solves this via **Dynamic Programming shortest-path lattice segmentation**.
2. **Generational Slot Drift and Demographics**: The exact same name (`فاروق`, `شهد`, `كريم`) possesses radically different statistical probabilities depending on whether it occupies Slot 1 (Student/Child), Slot 2 (Father), or Slot 3 (Grandfather).
3. **Compound Name Integrity**: Prefix-bound names (`عبد الرحمن`, `أبو بكر`, `نور الدين`, `فاطمة الزهراء`, `ذو الفقار`) are recognized as atomic entities without corrupting patronymic slot counting.
4. **Phonetic Egyptian Passport Transliteration**: Standard Arabic transliterators use Levantine or Gulf phonetics (*Jamal*, *Hamid*). `egy-names` enforces authentic Egyptian Civil Registry phonetics (*Gamal*, *Hamed*, *El-*, *Abou-*).
5. **100% Arabic Vocalization and Deep Root Etymology**: Complete Tashkeel (diacritization) and root analysis across all **44,626 canonical entries**.

---

## Feature Engineering Deep Dive

`egy-names` is designed as a zero-hallucination, high-performance linguistic engine. Here is the architectural philosophy and execution behind each capability:

---

### 1. Grounded 6-Slot Patronymic Name Generation
* **The Problem with Generic Generators**: Tools like Faker randomly choose words from a flat list, creating culturally absurd chains (such as putting female names as fathers, pairing incompatible religious markers, or using archaic 19th-century surnames as first names for children).
* **Our Architecture**: We formulated name generation as a **joint multi-variate transition graph over 6 genealogical positions**:
  $$P(N_1, N_2, N_3, N_4, N_5) = P(N_1 \mid G, R, A) \times \left[ \prod_{k=2}^{4} P(N_k \mid \text{Male}, R, S_k) \right] \times P(N_5 \mid \text{Surname})$$
* **Why It Is Robust**:
  * $N_1$ respects requested gender ($G$), religion ($R$), and age cohort ($A$).
  * $N_2, N_3, N_4$ are mathematically bounded to authentic male given names matching religious continuity.
  * $N_5$ samples from real Egyptian clan and toponymic surname distributions.

---

### 2. Generational Gaussian Age Intelligence Engine
* **The Core Insight**: Names are temporal cultural artifacts. A name like `شهد` or `يارا` belongs overwhelmingly to Egyptian youth born in the 2000s, whereas `فاروق` or `بسيوني` belongs to grandfathers born in the 1930s–1940s.
* **Mathematical Modeling**: We anchored the national corpus to its mean examination year ($Y_{\text{data}} = 2020$) and graduation age ($A_{\text{grad}} = 18$), yielding a baseline birth center of **2002 for Slot 1**. Applying the national inter-generational span ($\Delta_{\text{gen}} = 30\text{ years}$):
  * $\text{Slot }1 \text{ (Student): Center } 2002 \ (\approx 24\text{ yrs in }2026)$
  * $\text{Slot }2 \text{ (Father): Center } 1972 \ (\approx 54\text{ yrs in }2026)$
  * $\text{Slot }3 \text{ (Grandfather): Center } 1942 \ (\approx 84\text{ yrs in }2026)$
  * $\text{Slot }4 \text{ (Great-Grandfather): Center } 1912 \ (\text{Historical})$
* **Continuous Gaussian Scoring**:
  $$w_i = \exp\left(-\frac{1}{2} \left(\frac{\text{Target Birth Year} - \text{Center}_i}{\sigma}\right)^2\right), \quad \sigma = 12\text{ years}$$
* **Multi-Token Cross-Generational Corroboration**: When analyzing a full name chain (e.g. `"كريم أشرف فاروق"`), the engine checks the person (`كريم`, youth) + father (`أشرف`, parent) + grandfather (`فاروق`, grandparent). When all generational vectors align, it triggers a Bayesian corroboration boost, elevating confidence to **`0.641`**.

---

### 3. Dynamic Programming (DP) Unspaced Text Segmentation
* **The Challenge**: Egyptian government and bank archives frequently contain concatenated strings without spaces (e.g. `محمدأحمدعليحسنالشناوي`).
* **Our Solution**: Formulated as a **Unicode codepoint shortest-path DAG optimization**:
  $$\text{Cost}(i) = \min_{j < i} \Big( \text{Cost}(j) + \text{BaseCost} + \text{Bonus}(\text{Freq}_{j..i}) + \lambda \cdot \text{Length}_{j..i} \Big)$$
* **Why It Is Robust**:
  * Splits 3-to-6-part unspaced chains in **$< 0.05\text{ ms}$**.
  * Intelligently preserves prefixed compound names (`عبد الرحمن`, `نور الدين`, `فاطمة الزهراء`).
  * Recovers smoothly if non-Arabic or foreign noise tokens are embedded.

---

### 4. 100% Arabic Tashkeel (Diacritization) and Vocalization
* **The Challenge**: Arabic without Tashkeel is ambiguous (`محمد` could theoretically be read as *Mohamed*, *Mahmad*, or *Mohamad*).
* **Our Solution**: Every single one of the **44,626 canonical lemmas** is 100% vocalized with classical diacritics (Fathah, Dammah, Kasrah, Shaddah, Sukun).
* **Compound Awareness**: Handles bound genitive constructs (<code><bdi>عبدالرحمن</bdi></code>&lrm; → <code><bdi>عَبْدُ الرَّحْمَن</bdi></code>).
* **Compound Awareness**: Bound iḍāfa (<code><bdi>حسام الدين</bdi></code>&lrm; → <code><bdi>حُسَامُ الدِّين</bdi></code>).

---

### 5. Authentic Egyptian Passport Transliteration
* **The Challenge**: Generic Arabic transliterators use Levantine or Gulf rules (producing *Jamal*, *Hamid*, *Jihan*).
* **Our Solution**: We engineered an authentic **Egyptian Civil Registry phonetic engine** enforcing the distinctive Egyptian pronunciation:
  * `ج` $\to$ **`G`** (*Gamal*, *Gihan*, *Magdy*)
  * `ح` $\to$ **`H`** (*Hassan*, *Hamed*)
  * Definite article $\to$ **`El-`** (*Elshazly*, *Elsayed*, *Elsharkawy*)
  * Theophoric compounds $\to$ **`Abdel-` / `Abou-`** (*Abdelrahman*, *Abdelhamid*, *Aboubakr*)

---

### 6. Deep Morphological Etymology, Roots, and Toponyms
* **100% Bilingual Coverage**: Every entry in the 44.6K lexicon includes rich Arabic and English linguistic definitions:
  * **Semitic Triliteral Roots**: e.g., `محمد` $\to$ *المحمود؛ كثير الخصال المحمودة (من الجذر ح م د)*.
  * **Coptic/Ancient Heritage**: e.g., `مهرائيل` $\to$ *اسم قبطي/سرياني مركب يعني هبة الله أو عطية النور*.
  * **Ottoman Guild Occupations**: e.g., `بوادقجي` $\to$ *صانع أو بائع البارود في العهد العثماني*.
  * **Nile Delta and Upper Egypt Toponyms**: e.g., `المنياوي` $\to$ *نسبة إلى مدينة المنيا في صعيد مصر*.

---

### 7. 23,457 Deterministic Typo and Orthographic Correction Rules
* **The Challenge**: Real-world citizen data entry is plagued by typos, keyboard slips, and OCR scanning noise.
* **Our Solution**: Extracted from 15.88M+ records to build an in-memory $O(1)$ lookup hash index covering:
  * Missing/Extra letters (<code><bdi>ابراهم</bdi></code>&lrm; → <code><bdi>إبراهيم</bdi></code>)
  * Compound fusion/spacing (<code><bdi>عبد الرحمن</bdi></code>&lrm; → <code><bdi>عبدالرحمن</bdi></code>)
  * Alif Maqsura vs. Ya (<code><bdi>مصطفا</bdi></code>&lrm; → <code><bdi>مصطفى</bdi></code>)
  * Alif Maqsura vs. Ya (<code><bdi>يحي</bdi></code>&lrm; → <code><bdi>يحيى</bdi></code>)
  * Hamza normalization (<code><bdi>اسماعيل</bdi></code>&lrm; → <code><bdi>إسماعيل</bdi></code>)
  * Ta Marbuta vs. Ha (<code><bdi>فاطمه</bdi></code>&lrm; → <code><bdi>فاطمة</bdi></code>)

---

### 8. Bayesian Demographic and Religion Inference
* **How It Works**: Applies empirical frequency marginalization over patronymic chains.
* **Lineage Continuity**: Distinguishes between neutral names shared across denominations (`إبراهيم`, `يوسف`, `سمير`, `عادل`) and distinct markers (`ميخائيل`, `جرجس`, `شنودة` vs `محمد`, `أحمد`, `مصطفى`), calculating calibrated Bayesian confidence scores.

---

### 9. Authentic Egyptian Pet Names (أسماء الدلع)
* **The Cultural Nuance**: Egyptian pet names follow deeply rooted morphological diminutive patterns (`فَعُّول`, `مَيْفُو`, `فَعُّودَة`) distinct from Levantine or Gulf nicknames.
* **4-Way Multi-Modal Representation**: Every pet name is provided in:
  1. Plain Arabic lemma (`ميدو`, `حمو`, `حمودة`)
  2. Full Egyptian vocalized Tashkeel (`مِيدُو`, `حَمُّو`, `حَمُّودَة`)
  3. Transliterated English (`Mido`, `Hamou`, `Hamouda`)
  4. Egyptian Colloquial IPA phonetics (`[ˈmiːdu]`, `[ˈħæm.mu]`, `[ħæmˈmuːdæ]`)

---

### 10. Iconic Egyptian Public Figures (الأسماء المشهورة)
* **Empirical Validation**: Filtered exclusively for notable Egyptian historical leaders, scientists, authors, athletes, artists, and Nobel laureates.
* **Bilingual Descriptions**: Provides concise historical context in both Arabic and English (e.g. *محمد صلاح - قائد منتخب مصر وهداف ليفربول العالمي* / *Mohamed Salah - Egyptian National Football Captain & Global Icon*).

---

### 11. Dual Vocalization (Standard vs. Egyptian Colloquial Tashkeel)
* **Standard Tashkeel (`tashkeel_standard`)**: Full Modern Standard Arabic / Classical Quranic vocalization (`مُحَمَّد`, `آيَات`).
* **Egyptian Tashkeel (`tashkeel_eg`)**: Real-world Egyptian colloquial vocalization with word-final sukun and dialectal vowel harmony (`مُحَمَّدْ`, `آيَاتْ`).

---

### 12. Standard & Egyptian IPA Phonetics (for AI TTS & Linguistics)
* **The Phonetic Bridge**: Built specifically for Speech Synthesis (TTS), Voice AI, and non-native learners.
* **Accurate Glottal & Velar Shifts**: Correctly reflects Egyptian `/d͡ʒ/` $\to$ `[ɡ]` (*Gamal* `[ɡæˈmæːl]`) and vowel elongation.

---

### 13. Multi-Criteria Onomastic Search & Lexical Filtering
* **High-Performance Search Engine**: Sub-millisecond filtering across all 44,626 names by prefix, infix, suffix, gender, religion, etymological origin, and sociological generation trend.

---

### 14. Patronymic Chain Role Assignment & Custom Formatting
* **Structural Decomposition**: Dynamically classifies every token in a multi-part chain into its exact genealogical position (`person`, `father`, `grandfather`, `ancestor`, `family_name`).
* **Custom Template Engine**: Format strings with arbitrary templates (e.g. `"{person} {father} {family}"` $\to$ `"محمد أحمد الشاذلي"`).

---

## The Mathematics of Grounded Patronymic Generation

### The 6-Slot Generational Model

| Slot | Role | Typical Demographics | Generation Era | Example Realization |
| :--- | :--- | :--- | :--- | :--- |
| **Slot 1** | **Person ($N_1$)** | Youth / Student (Male or Female) | Age ~24 in 2026 | `يارا` *(Yara)* |
| **Slot 2** | **Father ($N_2$)** | Direct Paternal Lineage (Male Only) | Age ~54 in 2026 | `عادل` *(Adel)* |
| **Slot 3** | **Grandfather ($N_3$)** | Paternal Grandfather (Male Only) | Age ~84 in 2026 | `فاروق` *(Farouk)* |
| **Slot 4** | **Ancestor ($N_4$)** | Ancestral Patriarch (Male Only) | Historical Era | `مخلوف` *(Makhlouf)* |
| **Slot 5** | **Family Surname ($N_5$)**| Clan / Toponymic Surname | All Generations | `الشناوي` *(Elshenawy)* |

---

## Comparison with Existing Systems

| Dimension | Standard Open-Source / LLMs | `egy-names` (v0.3.5) |
| :--- | :--- | :--- |
| **National Empirical Corpus** | Synthetic / web-scraped (<50K records) | **15.88M+ Verified Official Records** (30M+ total corpus) |
| **Master Lexicon Size** | 1,000–5,000 common names | **44,626 Unique Canonical Lemmas** (>99.9% population coverage) |
| **Spelling Typo Corrections** | Basic regex / none | **23,457 Deterministic Correction Rules** |
| **Execution Latency** | 500ms – 2,000ms (LLM API call) | **< 0.01 ms (Sub-microsecond In-Memory Hash Trie)** |
| **Dependencies and Privacy** | Cloud APIs / Internet required | **Zero Dependencies • 100% Offline and Deterministic** |
| **Arabic Diacritization (Tashkeel)**| Partial guessing | **100.0% Verified Arabic Tashkeel (44,626/44,626)** |
| **Morphological Etymology** | None | **100.0% Roots and Toponyms in Arabic and English** |
| **Age Intelligence Engine** | Non-existent | **Continuous Gaussian Generational Demographic Model** |
| **Cross-Language Parity** | Python-only | **8 Native SDKs** (Python, TS, PHP, Swift, C#, Dart, Java, C++) |

---

## National Corpus Genesis and Empirical Grounding

`egy-names` is extracted from **15,875,535 official examination records** spanning 5 nation-wide cohorts across all 27 Egyptian Governorates:

| Transformation Phase | Entity Count | Description |
| :--- | :--- | :--- |
| **Phase 0: Raw National Records** | **15,875,535 Records** | Official student and citizen examination rows across 494 national dataset files |
| **Phase 1: Patronymic Occurrences** | **~63,500,000 Tokens** | Individual name slot occurrences across all genealogical positions |
| **Phase 2: Raw Unique Word Tokens** | **43,333 Distinct Words** | Unique word forms before spelling normalization |
| **Phase 3: Typo and Orthography Rules** | **23,457 Rules** | Mappings for misspellings and unspaced compounds (<code><bdi>عبد الرحمن</bdi></code>&lrm; → <code><bdi>عبدالرحمن</bdi></code>) |
| **Phase 4: Master Canonical Lexicon** | **44,626 Master Lemmas** | **The complete verified onomastic dictionary of Egypt** |

---

## Installation and Multi-Language Usage

> **Full Documentation**: For exhaustive method signatures, parameter tables, and advanced configurations, see the [Complete API Reference](DOCUMENTATION.md).

The name book is one file: [`data/names.json.gz`](data/names.json.gz). Edit that, run [`scripts/sync-catalog.sh`](scripts/sync-catalog.sh), then publish.

### 1. Python (3.9+)

```bash
pip install --upgrade egy-names==0.3.5
```

```python
from egy_names import EgyNames

e = EgyNames()

# 1. Authentic Egyptian Pet Names (أسماء الدلع)
print(e.dallaa("محمد", format="tashkeel"))  # ['مِيدُو', 'حَمُّو', 'حَمُّودَة']
print(e.dallaa("محمد", format="ipa"))       # ['[ˈmiːdu]', '[ˈħæm.mu]', '[ħæmˈmuːdæ]']
print(e.dallaa_info("محمد"))                # [PetName(ar='ميدو', tashkeel='مِيدُو', en='Mido', ipa='[ˈmiːdu]'), ...]

# 2. Authentic Egyptian Public Figures (الأسماء المشهورة)
print(e.famous_figures("محمد", lang="en"))
# -> ['Mohamed Salah (Egyptian National Football Captain & Global Icon)', 'Mohamed Ali Pasha (Founder of Modern Egypt)', ...]

# 3. Dual Vocalization (Tashkeel) & IPA Transcriptions
print(e.tashkeel("محمد عبدالرحمن الشرقاوي")) # "مُحَمَّد عَبْدُ الرَّحْمَن الشَّرْقَاوِيّ"
print(e.tashkeel_eg("محمد"))                 # "مُحَمَّدْ"
print(e.ipa_eg("جمال"))                      # "[ɡæˈmæːl]" (Authentic Egyptian [ɡ])
print(e.ipa_standard("جمال"))                # "/d͡ʒamaːl/"

# 4. Concatenated Dynamic Programming Splitting
print(e.split("محمدأحمدعليحسنالشناوي"))
# -> ['محمد', 'أحمد', 'علي', 'حسن', 'الشناوي']

# 5. Deterministic Typo and OCR Correction
print(e.correct("احمد مصطفا عبد الرحيم يحي"))
# -> "أحمد مصطفى عبدالرحيم يحيى"

# 6. Morphological Roots and Etymology
print(e.info("محمد").root)                   # "ح-م-د"
print(e.meaning("المنياوي"))
# -> {'ar': 'نسبة إلى مدينة المنيا في صعيد مصر...', 'en': 'Attributed to Minya in Upper Egypt...'}

# 7. Grounded 6-Slot Patronymic Generation
names = e.generate(count=3, gender="female", religion="christian", length=4)
for n in names:
    print(f"{n.ar}  --  {n.en}")

# 8. Generational Age Intelligence
det = e.detect_age("كريم أشرف فاروق")
print(f"Age: ~{det.estimated_age} yrs | Conf: {det.confidence} | {det.generation_label}")
```

#### Faker companion (`faker-egy-names`)

Python and PHP packages for test suites that already use Faker. They do not invent a first name and a last name. Every call runs `generate()` — grounded patronymic chains. Offline.

```bash
pip install faker-egy-names
composer require afify/faker-egy-names
```

```python
from faker_egy_names import egyptian_faker

fake = egyptian_faker()
name = fake.egyptian_name(gender="female", religion="muslim")
print(name.ar)   # grounded chain
print(name.en)
```

```php
$fake = egyptian_faker();
$name = $fake->egyptian_name(gender: 'female', religion: 'muslim');
echo $name->ar;
echo $name->en;
```

There is no `first_name` / `last_name` mapping. For one coherent person, call `egyptian_name()` once and read `parts_ar` / `parts_en`. Source: [`faker-egy-names/`](faker-egy-names/) · [`faker-egy-names-php/`](faker-egy-names-php/) · [PyPI](https://pypi.org/project/faker-egy-names/) · [Packagist](https://packagist.org/packages/afify/faker-egy-names).

---

### PHP (8.1+)

```bash
composer require afify/egy-names
```

```php
use Afify\EgyNames\EgyNames;

$en = new EgyNames();
echo $en->translate('محمد أحمد علي');
print_r($en->split('محمدأحمدعليحسنالشناوي'));
echo $en->correct('احمد مصطفا');
$names = $en->generate(count: 3, gender: 'female', length: 4);
```

The engine is [`afify/egy-names`](https://packagist.org/packages/afify/egy-names). Source: [egy-names-php](https://github.com/AbdullahAfifyKhalil/egy-names-php).

---

### 2. TypeScript / JavaScript (Node.js & Modern Browsers)

```bash
npm install egy-names@0.3.5
```

```typescript
import { EgyNames, Gender, Religion } from 'egy-names';

const en = new EgyNames();

// 1. Pet Names & Figures
console.log(en.dallaa("محمد", "tashkeel")); // ['مِيدُو', 'حَمُّو', 'حَمُّودَة']
console.log(en.famousFigures("محمد", "en")); // ['Mohamed Salah (Egyptian National Football Captain & Global Icon)', ...]

// 2. Translation, Tashkeel & IPA
console.log(en.translate("محمد أحمد علي")); // "Mohamed Ahmed Ali"
console.log(en.tashkeel("محمد عبدالرحمن")); // "مُحَمَّد عَبْدُ الرَّحْمَن"
console.log(en.ipaEg("جمال")); // "[ɡæˈmæːl]"

// 3. Dynamic Programming Splitting
console.log(en.split("محمدأحمدعليحسن")); // ["محمد", "أحمد", "علي", "حسن"]

// 4. Demographic Inferences
console.log(en.detectGender("فاطمة الزهراء")); // { gender: 'female', confidence: 0.95 }
console.log(en.detectReligion("مينا جرجس بطرس")); // { religion: 'christian', confidence: 0.98 }
```

---

### 3. Swift (iOS / macOS / watchOS / visionOS)

Add in Xcode or `Package.swift`:
```swift
dependencies: [
    .package(url: "https://github.com/AbdullahAfifyKhalil/egy-names.git", from: "0.3.5")
]
```

```swift
import EgyNames

let en = EgyptianNames()

// Pet Names and Public Figures
let petNames = en.dallaa("محمد", format: "tashkeel") // ["مِيدُو", "حَمُّو", "حَمُّودَة"]
let figures = en.famousFigures("محمد", lang: "en")

// Splitting and Tashkeel
let parts = en.split("محمدأحمدعليحسن") // ["محمد", "أحمد", "علي", "حسن"]
print(en.tashkeel("محمد عبدالرحمن")) // "مُحَمَّد عَبْدُ الرَّحْمَن"
print(en.translate("محمد أحمد علي")) // "Mohamed Ahmed Ali"
```

---

### 4. .NET / C#

```bash
dotnet add package egy-names --version 0.3.5
```

```csharp
using EgyNames;

var en = new EgyptianNamesEngine();

// Generation & Transliteration
var names = en.Generate(count: 3, gender: "female");
Console.WriteLine(en.Translate("محمد أحمد علي")); // Mohamed Ahmed Ali

// 14D Features
Console.WriteLine(string.Join(", ", en.Dallaa("محمد", "tashkeel"))); // مِيدُو, حَمُّو, حَمُّودَة
Console.WriteLine(en.Tashkeel("محمد عبدالرحمن")); // مُحَمَّد عَبْدُ الرَّحْمَن
Console.WriteLine(string.Join(", ", en.Split("محمدأحمدعليحسن"))); // محمد, أحمد, علي, حسن
```

---

### 5. Dart / Flutter

```bash
flutter pub add egy_names:^0.3.5
```

```dart
import 'package:egy_names/egy_names.dart';

void main() {
  final en = EgyNames();
  
  // 14D Features & Pet Names
  print(en.dallaa('محمد', format: 'ipa')); // ['[ˈmiːdu]', '[ˈħæm.mu]', '[ħæmˈmuːdæ]']
  print(en.famousFigures('محمد', lang: 'ar'));
  print(en.ipaEg('محمد')); // '[moˈħamːæd]'

  // Splitting & Translation
  print(en.translate("محمد أحمد علي")); // Mohamed Ahmed Ali
  print(en.tashkeel("محمد عبدالرحمن")); // مُحَمَّد عَبْدُ الرَّحْمَن
  print(en.split("محمدأحمدعليحسن"));    // [محمد, أحمد, علي, حسن]
}
```

---

### 6. Java & Android (Kotlin / Scala)

**Maven (`pom.xml`):**
```xml
<dependency>
    <groupId>io.github.abdullahafifykhalil</groupId>
    <artifactId>egy-names</artifactId>
    <version>0.3.5</version>
</dependency>
```

**Gradle (`build.gradle` / `build.gradle.kts`):**
```groovy
implementation 'io.github.abdullahafifykhalil:egy-names:0.3.5'
```

```java
import com.afify.egynames.EgyptianNames;

public class Main {
    public static void main(String[] args) {
        EgyptianNames en = new EgyptianNames();
        System.out.println(en.dallaa("محمد", "tashkeel")); // [مِيدُو, حَمُّو, حَمُّودَة]
        System.out.println(en.famousFigures("محمد", "en"));
        System.out.println(en.translate("محمد أحمد علي")); // Mohamed Ahmed Ali
        System.out.println(en.tashkeel("محمد عبدالرحمن")); // مُحَمَّد عَبْدُ الرَّحْمَن
    }
}
```

---

### 7. Modern C++ (C++20 / C++17)

```cmake
include(FetchContent)
FetchContent_Declare(
    egy_names
    GIT_REPOSITORY https://github.com/AbdullahAfifyKhalil/egy-names.git
    GIT_TAG v0.3.5
    SOURCE_SUBDIR cpp/egy_names
)
FetchContent_MakeAvailable(egy_names)
target_link_libraries(your_target PRIVATE egy_names)
```

```cpp
#include <egy_names/egy_names.hpp>
#include <iostream>

int main() {
    egy_names::EgyptianNames en;
    std::cout << en.translate("محمد أحمد علي") << "\n"; // Mohamed Ahmed Ali
    std::cout << en.tashkeel("محمد عبدالرحمن") << "\n"; // مُحَمَّد عَبْدُ الرَّحْمَن
    auto dallaa = en.dallaa("محمد", "tashkeel");
    for (const auto& d : dallaa) std::cout << d << " ";
    std::cout << "\n";
    return 0;
}
```

---

## Hugging Face Datasets and Model

The underlying national datasets — and the fallback classifier trained on them — are open-source on Hugging Face.

### 1. Egyptian Names Dataset (44.6K Lexicon and 15.88M Corpus)
[https://huggingface.co/datasets/Abdullah-afify/egyptian-names](https://huggingface.co/datasets/Abdullah-afify/egyptian-names)
* **`final_canonical` (Default):** 44,626 unique master names with 100% Tashkeel, Arabic/English meanings, and 6-slot generational probabilities.
* **`phase0_raw`:** 1.54M raw full name strings.
* **`phase1_segmented`:** 1.0M segmented patronymic chains.
* **`phase3_corrections`:** 23,457 orthographic correction rules.

```python
from datasets import load_dataset

dataset = load_dataset("Abdullah-afify/egyptian-names")
print(dataset["train"][0])
```

### 2. Fallback classifier (names not in the book)
[https://huggingface.co/Abdullah-afify/egy-names-fallback-classifier](https://huggingface.co/Abdullah-afify/egy-names-fallback-classifier)

Trained on this dataset. Used only when `lookup` misses. Every prediction is labeled `inferred: true`. The model abstains (`unknown` / `neutral`) below calibrated precision thresholds instead of guessing. Wired into the Python SDK as `identify()` / `identify_all()`.

### 3. Egyptian High School Students Degrees Dataset (2017–2026)
[https://huggingface.co/datasets/Abdullah-afify/egyptian-high-school-students-grades](https://huggingface.co/datasets/Abdullah-afify/egyptian-high-school-students-grades)
* **3,790,225 Total Records** across 5 national examination cohorts (**2017**, **2023**, **2024**, **2025**, **2026**).

---

## Onomastic Architecture

### 1. Patronymic Lineage Decomposition
The position of a name within an Egyptian patronymic chain defines its legal and social role:

| Position | Formal Role | Arabic Designation | Generational Context |
| :--- | :--- | :--- | :--- |
| **Slot 1** | **Personal Given Name** | اسم الشخص الأول | Individual identity (Male or Female) |
| **Slot 2** | **Father's Name** | اسم الأب | Direct paternal lineage (Male only) |
| **Slot 3** | **Grandfather's Name** | اسم الجد | Paternal grandfather (Male only) |
| **Slot 4** | **Great-Grandfather** | اسم سلف العائلة | Ancestral patriarch (Male only) |
| **Slot 5** | **Family Surname / Clan**| اللقب والعائلة | Tribal, geographic toponym, or guild surname |

---

### 2. Concatenated Dynamic Programming Segmentation
When processing unspaced Arabic text (`محمدأحمدعليحسنالشناوي`), the library executes a shortest-path dynamic programming algorithm over Unicode codepoints:

$$\text{Cost}(i) = \min_{j < i} \Big( \text{Cost}(j) + \text{BaseCost} + \text{Bonus}(\text{Freq}_{j..i}) + \lambda \cdot \text{Length}_{j..i} \Big)$$

---

## About Afify

**[Afify](https://afify.co)** works in software, hardware, and media. One product. Many pieces. No center. Built to last. Unified, modular, decentralized, sustainable — or it does not ship.

Egy-Names is an Afify open-source project.

* **Egy-Names**: [**afify.co/egy-names**](https://afify.co/egy-names) — origin, process, insights, lab, examples, and demo
* **Website**: [**afify.co**](https://afify.co)
* **Instagram**: [**@afify.life**](https://www.instagram.com/afify.life/)
* **LinkedIn**: [**Abdullah Afify**](https://www.linkedin.com/in/abdullah-afify)
* **Medium**: [**The Secret Code of Egyptian Names**](https://medium.com/@abdullah.afify/the-secret-code-of-egyptian-names-how-we-engineered-a-14-dimensional-nlp-engine-5205db7f04f4) · [**@abdullah.afify**](https://medium.com/@abdullah.afify)
* **GitHub**: [**@AbdullahAfifyKhalil**](https://github.com/AbdullahAfifyKhalil)
* **Founder**: [**Abdullah Afify**](https://github.com/AbdullahAfifyKhalil)

---

## License and Citation

Distributed under the **MIT License**. See `LICENSE` for details.

```bibtex
@software{afify2026egynames,
  author       = {Abdullah Afify},
  title        = {egy-names: A Production-Grade Onomastic Intelligence and Linguistic Engine for Egyptian Names},
  year         = {2026},
  publisher    = {GitHub},
  version      = {0.3.5},
  url          = {https://github.com/AbdullahAfifyKhalil/egy-names}
}
```

---

<div align="center">
  <sub>Developed by <b><a href="https://github.com/AbdullahAfifyKhalil">Abdullah Afify</a></b> • An <b><a href="https://afify.co">Afify</a></b> open-source project • <b><a href="https://afify.co/egy-names">afify.co/egy-names</a></b></sub>
</div>
