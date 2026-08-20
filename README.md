<div align="center">

<img src="assets/banner.png" alt="Egyptian Names Banner" width="100%" style="border-radius: 12px; margin-bottom: 24px;" />

<img src="assets/logo.png" alt="Egyptian Names Logo" width="120" style="border-radius: 24px; box-shadow: 0 8px 30px rgba(0,0,0,0.3);" />

# Egyptian Names (`egy-names`)
### *A Production-Grade Onomastic Intelligence and Linguistic Engine for Egyptian Names*

[![PyPI Version](https://img.shields.io/badge/PyPI%20(Python)-v0.2.1-blue?logo=pypi)](https://pypi.org/project/egy-names/)
[![npm Version](https://img.shields.io/badge/npm%20(TS%2FJS)-v0.2.1-cb3837?logo=npm)](https://www.npmjs.com/package/egy-names)
[![NuGet Version](https://img.shields.io/badge/NuGet%20(.NET)-v0.2.1-004880?logo=nuget)](https://www.nuget.org/packages/egy-names/)
[![pub.dev Version](https://img.shields.io/badge/pub.dev%20(Dart)-v0.2.1-0175C2?logo=dart)](https://pub.dev/packages/egy_names)
[![Swift PM](https://img.shields.io/badge/Swift%20PM-v0.2.1-FA7343?logo=swift)](https://github.com/AbdullahAfifyKhalil/egy-names)
[![Maven Central](https://img.shields.io/badge/Maven%20Central-v0.2.1-orange?logo=apachemaven)](https://central.sonatype.com/artifact/io.github.abdullahafifykhalil/egy-names)
[![Hugging Face Names](https://img.shields.io/badge/Hugging%20Face-Names%20(13M%20Corpus)-yellow?logo=huggingface)](https://huggingface.co/datasets/Abdullah-afify/egyptian-names)
[![Hugging Face Degrees](https://img.shields.io/badge/Hugging%20Face-Student%20Degrees%20(3.79M)-blue?logo=huggingface)](https://huggingface.co/datasets/Abdullah-afify/egyptian-high-school-students-grades)
[![C++ Standard](https://img.shields.io/badge/C%2B%2B-20%20%2F%2017-00599C?logo=cplusplus)](https://github.com/AbdullahAfifyKhalil/egy-names)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Implemented with deterministic parity across 7 major programming languages:**
<br />
**Python** • **TypeScript / JavaScript** • **.NET / C#** • **Flutter / Dart** • **Swift** • **Java / Kotlin** • **C++**

[Features](#key-features) • [Overview](#overview) • [Installation & Usage](#installation--usage) • [Hugging Face Datasets](#hugging-face-datasets) • [Onomastic Architecture](#onomastic-architecture) • [About Afify Corporation](#about-afify-corporation) • [License](#license)

</div>

---

## Overview

Egyptian personal names follow an unbroken patronymic lineage system (*Personal + Father + Grandfather + Ancestor + Family/Tribe*) rather than the Western *Given + Surname* convention. This structure creates significant computational and linguistic challenges:

1. **Patronymic Lineage Ambiguity**: Determining the generational role of each name element in official and colloquial records.
2. **Compound Names**: Proper handling of prefixed and unspaced compound names (`عبدالرحمن` vs `عبد الرحمن`, `نور الدين`, `فاطمة الزهراء`).
3. **Orthographic Variations**: Resolving standard Arabic spelling variants (`مصطفى`/`مصطفا`, `إبراهيم`/`ابراهيم`, `أحمد`/`احمد`).
4. **Concatenated Names**: Segmenting unspaced text strings in legacy digital records (`محمدأحمدعليحسنالشاذلي`).

`egy-names` solves these problems deterministically without relying on language model inference, using an empirical statistical model extracted from over **13,000,000+ validated records**, **56,796 canonical names**, and **54,000+ orthographic correction rules**.

---

## Key Features

| Capability | Description | Example |
|---|---|---|
| **Patronymic Generation** | Slot-weighted sampling matching national demographic distributions | `حسام أحمد عبدالعليم` |
| **Concatenated Segmentation** | Dynamic programming shortest-path segmenter for unspaced text | `محمدأحمدعلي` $\to$ `[محمد, أحمد, علي]` |
| **Diacritization (Tashkeel)** | Full vowel mark restoration with compound awareness | `محمد عبدالرحمن` $\to$ `مُحَمَّد عَبْدُالرَّحْمَن` |
| **Orthographic Correction** | Rule-based correction and Alif/Alif Maqsura normalization | `احمد مصطفا` $\to$ `أحمد مصطفى` |
| **Transliteration** | Bidirectional Arabic $\leftrightarrow$ English with phonetic preservation | `محمد أحمد علي` $\leftrightarrow$ `Mohamed Ahmed Ali` |
| **Demographic Inference** | Empirical gender and religious cultural classification | `مريم` (Female 95%), `جورج` (Christian 99%) |
| **Lineage Decomposition** | Six-slot generational decomposition | Personal $\to$ Father $\to$ Grandfather $\to$ Family |
| **Etymology & Meanings** | Morphological root definitions and English translations | `محمد` $\to$ *The Praised One ( الجذر: ح م د )* |

---

## Hugging Face Datasets

The underlying national datasets are open-source and available on Hugging Face:

### 1. Egyptian Names & Onomastic Intelligence Dataset
👉 **[https://huggingface.co/datasets/Abdullah-afify/egyptian-names](https://huggingface.co/datasets/Abdullah-afify/egyptian-names)**
- **44,626 Canonical Names** with gender, religion, generational slot distribution weights, Tashkeel, root meanings, and transliterations.
- **15,875,535+ Raw Full Name Records** (`phase0_raw`) and **1,000,000 Segmented Chains** (`phase1_segmented`).
- **43,333 Unique Token Frequencies** and **23,457 Orthographic Correction Rules**.

#### 📊 Full Data vs. Single Names Breakdown

| Metric | Count | Description |
| :--- | :--- | :--- |
| **Total Raw Exam Records** | **~15,875,535** | Total individual student & citizen exam rows across 494 dataset files |
| **Total Full Name Occurrences** | **~15.88 Million** | Total full patronymic name chains (e.g., `"محمد أحمد علي حسن الشرقاوي"`) |
| **Unique Full Name Strings** | **1,545,970+** | Distinct full 3-to-5-part name combinations |
| **Total Single Name Occurrences** | **~63,500,000** | Total individual name occurrences across all slots (averaging 4 names per chain) |
| **Raw Distinct Single Tokens** | **43,333** | Distinct raw word tokens before typo cleaning |
| **Typo & Spelling Corrections** | **23,457** | Mappings for misspellings and unspaced compound names (`عبدالرحمن` $\to$ `عبد الرحمن`) |
| **Final Canonical Master Lexicon** | **44,626** | **The complete clean dictionary of unique Egyptian names** |

```python
from datasets import load_dataset

# Load default canonical dictionary (44.6K names)
names_dataset = load_dataset("Abdullah-afify/egyptian-names")

# Load raw full names
raw_names = load_dataset("Abdullah-afify/egyptian-names", "phase0_raw")
```


### 2. Egyptian High School Students Degrees Dataset (2017–2026)
👉 **[https://huggingface.co/datasets/Abdullah-afify/egyptian-high-school-students-grades](https://huggingface.co/datasets/Abdullah-afify/egyptian-high-school-students-grades)**
- **3,790,225 Total Student Records** across 5 national examination cohorts (**2017**, **2023**, **2024**, **2025**, and **2026**).
- Includes seating numbers, full student quad/quint names, total examination scores, and pass/fail statuses.

```python
# Load all 3.79M student records across 2017-2026
degrees_dataset = load_dataset("Abdullah-afify/egyptian-high-school-students-grades")

# Load a specific examination cohort (e.g. 2026 results)
cohort_2026 = load_dataset("Abdullah-afify/egyptian-high-school-students-grades", "year_2026")
```

---

## Installation & Usage

### Swift / iOS / macOS / visionOS
Add package via Xcode (`File > Add Package Dependencies...`) or in `Package.swift`:
```swift
dependencies: [
    .package(url: "https://github.com/AbdullahAfifyKhalil/egy-names.git", from: "0.2.1")
]
```
```swift
import EgyNames

let en = EgyptianNames()
print(en.translate("محمد أحمد علي"))  // Mohamed Ahmed Ali
print(en.correct("احمد مصطفا عبد الرحيم"))  // أحمد مصطفى عبدالرحيم
print(en.tashkeel("محمد عبدالرحمن"))  // مُحَمَّد عَبْدُالرَّحْمَن
print(en.split("محمدأحمدعليحسن"))  // ["محمد", "أحمد", "علي", "حسن"]
```

---

### Python (3.9+)
```bash
pip install egy-names==0.2.1
```
```python
from egy_names import EgyptianNames

en = EgyptianNames()
print(en.translate("محمد أحمد علي"))  # Mohamed Ahmed Ali
print(en.correct("احمد مصطفا عبد الرحيم"))  # أحمد مصطفى عبدالرحيم
print(en.tashkeel("محمد عبدالرحمن"))  # مُحَمَّد عَبْدُالرَّحْمَن
print(en.split("محمدأحمدعليحسن"))  # ['محمد', 'أحمد', 'علي', 'حسن']
```

---

### TypeScript / Node.js
```bash
npm install egy-names@0.2.1
```
```typescript
import { EgyptianNames } from 'egy-names';

const en = new EgyptianNames();
console.log(en.translate("محمد أحمد علي")); // Mohamed Ahmed Ali
console.log(en.correct("احمد مصطفا عبد الرحيم")); // أحمد مصطفى عبدالرحيم
console.log(en.tashkeel("محمد عبدالرحمن")); // مُحَمَّد عَبْدُالرَّحْمَن
console.log(en.split("محمدأحمدعليحسن")); // ['محمد', 'أحمد', 'علي', 'حسن']
```

---

### .NET / C#
```bash
dotnet add package egy-names --version 0.2.1
```
```csharp
using EgyNames;

var en = new EgyptianNames();
Console.WriteLine(en.Translate("محمد أحمد علي")); // Mohamed Ahmed Ali
Console.WriteLine(en.Correct("احمد مصطفا عبد الرحيم")); // أحمد مصطفى عبدالرحيم
Console.WriteLine(en.Tashkeel("محمد عبدالرحمن")); // مُحَمَّد عَبْدُالرَّحْمَن
Console.WriteLine(string.Join(", ", en.Split("محمدأحمدعليحسن"))); // محمد, أحمد, علي, حسن
```

---

### Dart / Flutter
```bash
flutter pub add egy_names:^0.2.1
```
```dart
import 'package:egy_names/egy_names.dart';

void main() {
  final en = EgyptianNames();
  print(en.translate("محمد أحمد علي")); // Mohamed Ahmed Ali
  print(en.correct("احمد مصطفا عبد الرحيم")); // أحمد مصطفى عبدالرحيم
  print(en.tashkeel("محمد عبدالرحمن")); // مُحَمَّد عَبْدُالرَّحْمَن
  print(en.split("محمدأحمدعليحسن")); // [محمد, أحمد, علي, حسن]
}
```

---

### Java / Kotlin
```xml
<dependency>
    <groupId>io.github.abdullahafifykhalil</groupId>
    <artifactId>egy-names</artifactId>
    <version>0.2.1</version>
</dependency>
```
```java
import com.afify.egynames.EgyptianNames;

EgyptianNames en = new EgyptianNames();
System.out.println(en.translate("محمد أحمد علي")); // Mohamed Ahmed Ali
System.out.println(en.correct("احمد مصطفا عبد الرحيم")); // أحمد مصطفى عبدالرحيم
System.out.println(en.tashkeel("محمد عبدالرحمن")); // مُحَمَّد عَبْدُالرَّحْمَن
```

---

### Modern C++ (C++20 / C++17)
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
    std::cout << en.correct("احمد مصطفا عبد الرحيم") << "\n"; // أحمد مصطفى عبدالرحيم
    std::cout << en.tashkeel("محمد عبدالرحمن") << "\n"; // مُحَمَّد عَبْدُالرَّحْمَن
}
```

---

## Onomastic Architecture

### 1. Patronymic Lineage Decomposition
The position of a name within an Egyptian patronymic chain defines its legal and social role:

```
[ محمد ]     [ أحمد ]      [ علي ]       [ حسن ]        [ الشاذلي ]
   │            │             │             │               │
Slot 1        Slot 2        Slot 3        Slot 4          Slot 5
Person        Father     Grandfather     Ancestor      Family/Tribe
(اسم الشخص)   (اسم الأب)   (اسم الجد)      (السلف)     (اللقب والعائلة)
```

`egy-names` models the empirical probability $P(\text{Name} \mid \text{Slot}_k)$ across all six positions.

### 2. Concatenated Dynamic Programming Segmentation
When processing unspaced Arabic text (`محمدأحمدعليحسنالشاذلي`), the library executes a shortest-path dynamic programming algorithm over Unicode codepoints:

$$\text{Cost}(i) = \min_{j < i} \Big( \text{Cost}(j) + \text{BaseCost} + \text{Bonus}(\text{Freq}_{j..i}) + \lambda \cdot \text{Length}_{j..i} \Big)$$

---

## About Afify Corporation

**[Afify Corporation](https://afify.co)** is a technology and media enterprise innovating across software, hardware systems, and digital media, leveraging advanced engineering and artificial intelligence.

- 🌐 **Website**: **[afify.co](https://afify.co)**
- 🐙 **GitHub**: **[github.com/AbdullahAfifyKhalil](https://github.com/AbdullahAfifyKhalil)**
- 👤 **Founder**: **[Abdullah Afify](https://github.com/AbdullahAfifyKhalil)**

---

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue on the [GitHub issues page](https://github.com/AbdullahAfifyKhalil/egy-names/issues).

---

## License

Distributed under the **MIT License**. See `LICENSE` for details.

---

<div align="center">
  <sub>Developed by <b><a href="https://github.com/AbdullahAfifyKhalil">Abdullah Afify</a></b> • Backed by <b><a href="https://afify.co">Afify Corporation (afify.co)</a></b></sub>
</div>
