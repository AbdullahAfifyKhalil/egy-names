<div align="center">

<img src="https://raw.githubusercontent.com/AbdullahAfifyKhalil/egy-names/main/assets/banner.png" alt="Egyptian Names Banner" width="100%" style="border-radius: 14px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);" />

<img src="https://raw.githubusercontent.com/AbdullahAfifyKhalil/egy-names/main/assets/logo.png" alt="Egyptian Names Logo" width="130" style="border-radius: 28px; box-shadow: 0 12px 36px rgba(0,0,0,0.25); margin-bottom: 12px;" />

# Egyptian Names (`egy-names`)
### *The Production-Grade Onomastic Intelligence and Computational Linguistic Engine for Egyptian Names*

[![PyPI Version](https://img.shields.io/badge/PyPI-v0.2.1-3776AB)](https://pypi.org/project/egy-names/)
[![npm Version](https://img.shields.io/badge/npm-v0.2.1-CB3837)](https://www.npmjs.com/package/egy-names)
[![NuGet Version](https://img.shields.io/badge/NuGet-v0.2.1-004880)](https://www.nuget.org/packages/egy-names/)
[![pub.dev Version](https://img.shields.io/badge/pub.dev-v0.2.1-0175C2)](https://pub.dev/packages/egy_names)
[![Swift PM](https://img.shields.io/badge/Swift_PM-v0.2.1-FA7343)](https://github.com/AbdullahAfifyKhalil/egy-names)
[![Maven Central](https://img.shields.io/badge/Maven_Central-v0.2.1-C71A36)](https://central.sonatype.com/artifact/io.github.abdullahafifykhalil/egy-names)
[![Hugging Face](https://img.shields.io/badge/Hugging_Face-44.6K_Lexicon-FFD21E)](https://huggingface.co/datasets/Abdullah-afify/egyptian-names)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Engineered with 100% Deterministic Parity across 7 Major Languages:**
<br />
**Python** | **TypeScript / JavaScript** | **.NET / C#** | **Flutter / Dart** | **Swift (iOS/macOS)** | **Java / Kotlin** | **C++ (C++20/17)**

[Why Egyptian Names?](#why-egyptian-names-are-unique-and-computationally-complex) | [Feature Deep Dive](#feature-engineering-deep-dive) | [Grounded Generation Engine](#the-mathematics-of-grounded-patronymic-generation) | [Corpus Scale](#national-corpus-genesis-and-empirical-grounding) | [Multi-Language Usage](#installation-and-multi-language-usage) | [Hugging Face Datasets](#hugging-face-datasets) | [Architecture](#onomastic-architecture) | [About Afify Corp](#about-afify-corporation) | [License](#license)

</div>

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
* **Compound Awareness**: Handles bound genitive constructs (`عبدالرحمن` $\to$ `عَبْدُ الرَّحْمَن`, `حسام الدين` $\to$ `حُسَامُ الدِّين`).

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
  * Missing/Extra letters (`ابراهم` $\to$ `إبراهيم`)
  * Compound fusion/spacing (`عبدالرحمن` $\to$ `عبد الرحمن`)
  * Alif Maqsura vs. Ya (`مصطفا` $\to$ `مصطفى`, `يحي` $\to$ `يحيى`)
  * Hamza normalization (`اسماعيل` $\to$ `إسماعيل`)
  * Ta Marbuta vs. Ha (`فاطمه` $\to$ `فاطمة`)

---

### 8. Bayesian Demographic and Religion Inference
* **How It Works**: Applies empirical frequency marginalization over patronymic chains.
* **Lineage Continuity**: Distinguishes between neutral names shared across denominations (`إبراهيم`, `يوسف`, `سمير`, `عادل`) and distinct markers (`ميخائيل`, `جرجس`, `شنودة` vs `محمد`, `أحمد`, `مصطفى`), calculating calibrated Bayesian confidence scores.

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

| Dimension | Standard Open-Source / LLMs | `egy-names` (v0.2.1) |
| :--- | :--- | :--- |
| **National Empirical Corpus** | Synthetic / web-scraped (<50K records) | **15.88M+ Verified Official Records** (30M+ total corpus) |
| **Master Lexicon Size** | 1,000–5,000 common names | **44,626 Unique Canonical Lemmas** (>99.9% population coverage) |
| **Spelling Typo Corrections** | Basic regex / none | **23,457 Deterministic Correction Rules** |
| **Execution Latency** | 500ms – 2,000ms (LLM API call) | **< 0.01 ms (Sub-microsecond In-Memory Hash Trie)** |
| **Dependencies and Privacy** | Cloud APIs / Internet required | **Zero Dependencies • 100% Offline and Deterministic** |
| **Arabic Diacritization (Tashkeel)**| Partial guessing | **100.0% Verified Arabic Tashkeel (44,626/44,626)** |
| **Morphological Etymology** | None | **100.0% Roots and Toponyms in Arabic and English** |
| **Age Intelligence Engine** | Non-existent | **Continuous Gaussian Generational Demographic Model** |
| **Cross-Language Parity** | Python-only | **7 Native SDKs** (Python, TS, Swift, C#, Dart, Java, C++) |

---

## National Corpus Genesis and Empirical Grounding

`egy-names` is extracted from **15,875,535 official examination records** spanning 5 nation-wide cohorts across all 27 Egyptian Governorates:

| Transformation Phase | Entity Count | Description |
| :--- | :--- | :--- |
| **Phase 0: Raw National Records** | **15,875,535 Records** | Official student and citizen examination rows across 494 national dataset files |
| **Phase 1: Patronymic Occurrences** | **~63,500,000 Tokens** | Individual name slot occurrences across all genealogical positions |
| **Phase 2: Raw Unique Word Tokens** | **43,333 Distinct Words** | Unique word forms before spelling normalization |
| **Phase 3: Typo and Orthography Rules** | **23,457 Rules** | Mappings for misspellings and unspaced compounds (`عبدالرحمن` $\to$ `عبد الرحمن`) |
| **Phase 4: Master Canonical Lexicon** | **44,626 Master Lemmas** | **The complete verified onomastic dictionary of Egypt** |

---

## Installation and Multi-Language Usage

### 1. Python (3.9+)

```bash
pip install --upgrade egy-names
```

```python
from egy_names import EgyNames

e = EgyNames()

# 1. Age Detection and Generation
print(e.names_for_age(24, gender="female", top=3))
# -> [NameInfo(ar='شهد', en='Shahd', ...), NameInfo(ar='يارا', en='Yara', ...)]

det = e.detect_age("كريم أشرف فاروق")
print(f"Age: ~{det.estimated_age} ({det.age_range[0]}–{det.age_range[1]} yrs) | Conf: {det.confidence} | {det.generation_label}")
# -> Age: ~25 (13–37 yrs) | Conf: 0.641 | youth generation

# 2. Concatenated DP Splitting
print(e.split("محمدأحمدعليحسنالشناوي"))
# -> ['محمد', 'أحمد', 'علي', 'حسن', 'الشناوي']

# 3. 100% Vocalization (Tashkeel) and Correction
print(e.tashkeel("محمد عبدالرحمن الشرقاوي"))
# -> "مُحَمَّد عَبْدُالرَّحْمَن الشَّرْقَاوِيّ"

print(e.correct("احمد مصطفا"))
# -> "أحمد مصطفى"

# 4. Complete Root Etymology
print(e.meaning("المنياوي"))
# -> {'ar': 'نسبة إلى مدينة المنيا في صعيد مصر...', 'en': 'Attributed to Minya in Upper Egypt...'}

# 5. Phonetic Egyptian Transliteration
print(e.translate("محمد عبد الحميد الشاذلي"))
# -> "Mohamed Abdelhamid Elshazly"
```

---

### 2. TypeScript / JavaScript (Node.js and Modern Browsers)

```bash
npm install egy-names@0.2.1
```

```typescript
import { EgyptianNames } from 'egy-names';

const en = new EgyptianNames();

// 1. Translation and Tashkeel
console.log(en.translate("محمد أحمد علي")); // Mohamed Ahmed Ali
console.log(en.tashkeel("محمد عبدالرحمن")); // مُحَمَّد عَبْدُالرَّحْمَن

// 2. Intelligent Dynamic Programming Splitting
console.log(en.split("محمدأحمدعليحسن")); // ["محمد", "أحمد", "علي", "حسن"]

// 3. Demographic Inferences
console.log(en.detectGender("فاطمة الزهراء")); // { gender: 'female', confidence: 0.95 }
console.log(en.detectReligion("مينا جرجس بطرس")); // { religion: 'christian', confidence: 0.98 }
```

---

### 3. Swift (iOS / macOS / watchOS / visionOS)

Add via Xcode (`File > Add Package Dependencies...`) or in `Package.swift`:
```swift
dependencies: [
    .package(url: "https://github.com/AbdullahAfifyKhalil/egy-names.git", from: "0.2.1")
]
```

```swift
import EgyNames

let en = EgyptianNames()

// Splitting unspaced legacy strings
let parts = en.split("محمدأحمدعليحسن")
print(parts) // ["محمد", "أحمد", "علي", "حسن"]

// Full Tashkeel restoration
print(en.tashkeel("محمد عبدالرحمن")) // مُحَمَّد عَبْدُالرَّحْمَن

// Egyptian passport transliteration
print(en.translate("محمد أحمد علي")) // Mohamed Ahmed Ali
```

---

### 4. .NET / C#

```bash
dotnet add package egy-names --version 0.2.1
```

```csharp
using EgyNames;

var en = new EgyptianNames();
Console.WriteLine(en.Translate("محمد أحمد علي")); // Mohamed Ahmed Ali
Console.WriteLine(en.Tashkeel("محمد عبدالرحمن")); // مُحَمَّد عَبْدُالرَّحْمَن
Console.WriteLine(string.Join(", ", en.Split("محمدأحمدعليحسن"))); // محمد, أحمد, علي, حسن
```

---

### 5. Dart / Flutter

```bash
flutter pub add egy_names:^0.2.1
```

```dart
import 'package:egy_names/egy_names.dart';

void main() {
  final en = EgyptianNames();
  print(en.translate("محمد أحمد علي")); // Mohamed Ahmed Ali
  print(en.tashkeel("محمد عبدالرحمن")); // مُحَمَّد عَبْدُالرَّحْمَن
  print(en.split("محمدأحمدعليحسن"));    // [محمد, أحمد, علي, حسن]
}
```

---

### 6. Java / Kotlin

```xml
<dependency>
    <groupId>io.github.abdullahafifykhalil</groupId>
    <artifactId>egy-names</artifactId>
    <version>0.2.1</version>
</dependency>
```

```java
import com.afify.egynames.EgyptianNames;

public class Main {
    public static void main(String[] args) {
        EgyptianNames en = new EgyptianNames();
        System.out.println(en.translate("محمد أحمد علي")); // Mohamed Ahmed Ali
        System.out.println(en.tashkeel("محمد عبدالرحمن")); // مُحَمَّد عَبْدُالرَّحْمَن
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
    GIT_TAG v0.2.1
)
FetchContent_MakeAvailable(egy_names)
target_link_libraries(your_target PRIVATE egy_names)
```

```cpp
#include <egy_names/egy_names.hpp>
#include <iostream>

int main() {
    egy_names::EgyNames en;
    std::cout << en.translate("محمد أحمد علي") << "\n"; // Mohamed Ahmed Ali
    std::cout << en.tashkeel("محمد عبدالرحمن") << "\n"; // مُحَمَّد عَبْدُالرَّحْمَن
    return 0;
}
```

---

## Hugging Face Datasets

The underlying national datasets are open-source and hosted on Hugging Face:

### 1. Egyptian Names Dataset (44.6K Lexicon and 15.88M Corpus)
👉 [**https://huggingface.co/datasets/Abdullah-afify/egyptian-names**](https://huggingface.co/datasets/Abdullah-afify/egyptian-names)
* **`final_canonical` (Default):** 44,626 unique master names with 100% Tashkeel, Arabic/English meanings, and 6-slot generational probabilities.
* **`phase0_raw`:** 1.54M raw full name strings.
* **`phase1_segmented`:** 1.0M segmented patronymic chains.
* **`phase3_corrections`:** 23,457 orthographic correction rules.

```python
from datasets import load_dataset

dataset = load_dataset("Abdullah-afify/egyptian-names")
print(dataset["train"][0])
```

### 2. Egyptian High School Students Degrees Dataset (2017–2026)
👉 [**https://huggingface.co/datasets/Abdullah-afify/egyptian-high-school-students-grades**](https://huggingface.co/datasets/Abdullah-afify/egyptian-high-school-students-grades)
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

## About Afify Corporation

**[Afify Corporation](https://afify.co)** is a technology and intelligence enterprise innovating across software architecture, language engineering, and high-performance machine systems.

* **Website**: [**afify.co**](https://afify.co)
* **GitHub**: [**@AbdullahAfifyKhalil**](https://github.com/AbdullahAfifyKhalil)
* **Founder and Lead Architect**: [**Abdullah Afify**](https://github.com/AbdullahAfifyKhalil)

---

## License and Citation

Distributed under the **MIT License**. See `LICENSE` for details.

```bibtex
@software{afify2026egynames,
  author       = {Abdullah Afify},
  title        = {egy-names: A Production-Grade Onomastic Intelligence and Linguistic Engine for Egyptian Names},
  year         = {2026},
  publisher    = {GitHub},
  version      = {0.2.1},
  url          = {https://github.com/AbdullahAfifyKhalil/egy-names}
}
```

---

<div align="center">
  <sub>Developed by <b><a href="https://github.com/AbdullahAfifyKhalil">Abdullah Afify</a></b> • Backed by <b><a href="https://afify.co">Afify Corporation (afify.co)</a></b></sub>
</div>
