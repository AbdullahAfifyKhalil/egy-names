<div align="center">

<img src="assets/banner.png" alt="Egyptian Names Banner" width="100%" style="border-radius: 12px; margin-bottom: 20px;" />

<img src="assets/logo.png" alt="Egyptian Names Logo" width="140" style="border-radius: 50%; box-shadow: 0 8px 32px rgba(0,0,0,0.4);" />

# 🇪🇬 Egyptian Names (`egy-names`)
### *The Production-Grade Onomastic Intelligence & Linguistic Engine for Egyptian Names*

[![PyPI Version](https://img.shields.io/pypi/v/egy-names?color=blue&label=PyPI%20%28Python%29)](https://pypi.org/project/egy-names/)
[![npm Version](https://img.shields.io/npm/v/egy-names?color=cb3837&label=npm%20%28TS%2FJS%29)](https://www.npmjs.com/package/egy-names)
[![NuGet Version](https://img.shields.io/nuget/v/egy-names?color=004880&label=NuGet%20%28.NET%2FC%23%29)](https://www.nuget.org/packages/egy-names/)
[![pub.dev Version](https://img.shields.io/pub/v/egy_names?color=0175C2&label=pub.dev%20%28Dart%2FFlutter%29)](https://pub.dev/packages/egy_names)
[![Swift PM](https://img.shields.io/badge/Swift%20PM-iOS%20%7C%20macOS%20%7C%20visionOS-FA7343?logo=swift)](https://github.com/AbdullahAfifyKhalil/egy-names)
[![Maven Central](https://img.shields.io/badge/Maven%20Central-0.1.1-orange)](https://central.sonatype.com/)
[![C++ Standard](https://img.shields.io/badge/C%2B%2B-20%20%2F%2017-00599C?logo=cplusplus)](https://github.com/AbdullahAfifyKhalil/egy-names)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Available natively with 100% deterministic parity across 7 ecosystems:**
<br />
🐍 **Python** • 🟨 **TypeScript / Node.js** • 🔷 **.NET / C#** • 💙 **Flutter / Dart** • 🍎 **Swift / iOS** • ☕ **Java / Kotlin** • ⚡ **Modern C++**

[Features](#-key-features) • [The Story](#-the-story-why-egy-names) • [Installation](#-quick-start--installation) • [API & Examples](#-usage--api-examples) • [Dataset](#-data-pipeline--empirical-corpus) • [Architecture](#-onomastic-architecture)

</div>

---

## 📖 The Story: Why Egyptian Names?

Egyptian names present unique computational and onomastic challenges found in few other naming traditions:

1. **Patronymic Lineage Chains**: Unlike Western naming systems ($Given + Surname$), Egyptian naming forms an unbroken patronymic chain ($Personal + Father + Grandfather + Ancestor + Family/Tribe$), where each position conveys specific demographic and cultural meaning.
2. **Compound Name Ambiguity**: Names like `عبد الرحمن` (Abdel-Rahman), `نور الدين` (Nour El-Din), and `فاطمة الزهراء` (Fatima El-Zahraa) are frequently written concatenated (`عبدالرحمن`), unspaced, or split inconsistently across forms.
3. **Pervasive Orthographic Variations**: Civil registries and digital forms contain vast phonetic and orthographic variations (e.g. `مصطفى` vs `مصطفا`, `إبراهيم` vs `ابراهيم`, `أحمد` vs `احمد`).
4. **Unspaced Name Concatenation**: In legacy government records and scanned forms, entire full names appear glued together (`محمدأحمدعليحسنالشاذلي`).

`egy-names` solves these challenges **deterministically and without LLM hallucination**, backed by an empirical statistical frequency model extracted from over **33,000+ validated personal names** across millions of real records.

---

## ✨ Key Features

| Capability | Description | Example |
|---|---|---|
| 🎲 **Realistic Generation** | Patronymic Markov-chain generator with slot-specific frequencies | `حسام أحمد عبدالعليم` |
| 🔀 **DP Name Splitter** | Dynamic programming shortest-path segmenter for unspaced text | `محمدأحمدعلي` $\to$ `[محمد, أحمد, علي]` |
| ✍️ **Smart Tashkeel** | Full diacritization with compound name awareness | `محمد عبدالرحمن` $\to$ `مُحَمَّد عَبْدُالرَّحْمَن` |
| 🛠️ **Orthographic Corrector** | 54K+ rule dictionary + Alif/Alif Maqsura normalization | `احمد مصطفا` $\to$ `أحمد مصطفى` |
| 🌍 **Transliteration** | Bidirectional Arabic $\leftrightarrow$ English with phonetic preservation | `محمد أحمد علي` $\leftrightarrow$ `Mohamed Ahmed Ali` |
| 📊 **Demographic Inference** | Empirical gender & religious probability classification | `مريم` (Female 95%), `جورج` (Christian 99%) |
| 🌳 **Patronymic Decomposer** | Slot 1 to 6 genealogical lineage parser | Personal $\to$ Father $\to$ Grandfather $\to$ Family |
| 📖 **Etymology & Meanings** | Arabic root definitions and English translations | `محمد` $\to$ *The Praised One ( الجذر: ح م د )* |

---

## 🚀 Quick Start & Installation

### 🍎 Swift / iOS / macOS / visionOS (Swift Package Manager)
Add via Xcode: `File > Add Package Dependencies...` and enter:
```text
https://github.com/AbdullahAfifyKhalil/egy-names.git
```
Or in `Package.swift`:
```swift
dependencies: [
    .package(url: "https://github.com/AbdullahAfifyKhalil/egy-names.git", from: "0.1.1")
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

### 🐍 Python (3.9+)
```bash
pip install egy-names
```
```python
from egy_names import EgyptianNames, Gender, Religion

en = EgyptianNames()
print(en.translate("محمد أحمد علي"))  # Mohamed Ahmed Ali
print(en.correct("احمد مصطفا عبد الرحيم"))  # أحمد مصطفى عبدالرحيم
print(en.tashkeel("محمد عبدالرحمن"))  # مُحَمَّد عَبْدُالرَّحْمَن
print(en.split("محمدأحمدعليحسن"))  # ['محمد', 'أحمد', 'علي', 'حسن']
```

---

### 🟨 TypeScript / JavaScript (Node.js & Browser)
```bash
npm install egy-names
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

### 🔷 .NET / C# (.NET 8.0, 7.0, 6.0, Standard 2.0)
```bash
dotnet add package egy-names
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

### 💙 Flutter / Dart
```bash
flutter pub add egy_names
# or
dart pub add egy_names
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

### ☕ Java / Kotlin (Maven & Gradle)
```xml
<dependency>
    <groupId>io.github.abdullahafifykhalil</groupId>
    <artifactId>egy-names</artifactId>
    <version>0.1.1</version>
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

### ⚡ Modern C++ (C++20 / C++17)
```cmake
include(FetchContent)
FetchContent_Declare(
    egy_names
    GIT_REPOSITORY https://github.com/AbdullahAfifyKhalil/egy-names.git
    GIT_TAG v0.1.1
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

## 🧬 Onomastic Architecture

### 1. Patronymic Lineage Decomposition
In Egyptian culture, the position of a name inside the full sequence defines its legal and social role:

```
[ محمد ]     [ أحمد ]      [ علي ]       [ حسن ]        [ الشاذلي ]
   │            │             │             │               │
Slot 1        Slot 2        Slot 3        Slot 4          Slot 5
Person        Father     Grandfather     Ancestor      Family/Tribe
(اسم الشخص)   (اسم الأب)   (اسم الجد)      (السلف)     (اللقب والعائلة)
```

`egy-names` models the empirical probability $P(\text{Name} \mid \text{Slot}_k)$ across all positions.

### 2. Concatenated DP Name Segmentation
When processing unspaced Arabic text (`محمدأحمدعليحسنالشاذلي`), the library executes a shortest-path Dynamic Programming algorithm over character codepoints, evaluating:

$$\text{Cost}(i) = \min_{j < i} \Big( \text{Cost}(j) + \text{BaseCost} + \text{Bonus}(\text{Freq}_{j..i}) + \lambda \cdot \text{Length}_{j..i} \Big)$$

This segments concatenated names with over **99.2% accuracy** in less than 1 millisecond.

---

## 📊 Data Pipeline & Empirical Corpus

The engine is powered by an empirical national dataset processed in 5 rigorous phases:

- **33,117 Curated Canonical Names**
- **54,000+ Orthographic Correction Rules**
- **100% Zero-Dependency & Offline Execution** (Embedded 1.6 MB compressed bundle)

Detailed documentation and sample pipeline datasets are available in the [`data/`](data/) directory:
- [`data/pipeline/phase1_segmented_sample.csv`](data/pipeline/phase1_segmented_sample.csv): Token extraction from national records
- [`data/pipeline/phase2_slot_analysis_sample.csv`](data/pipeline/phase2_slot_analysis_sample.csv): Positional slot frequency tables
- [`data/pipeline/phase4_annotated_sample.csv`](data/pipeline/phase4_annotated_sample.csv): Full semantic and linguistic annotations

---

## 🌟 Interactive Examples & Benchmarks

Full runnable example suites for all languages are provided in [`examples/`](examples/):
- [Swift Examples](examples/swift/main.swift)
- [Python Examples](examples/python/demo.py)
- [TypeScript Examples](examples/typescript/demo.ts)
- [C# / .NET Examples](examples/csharp/Program.cs)
- [Flutter / Dart Examples](examples/dart/main.dart)
- [Java Examples](examples/java/Demo.java)
- [C++ Examples](examples/cpp/main.cpp)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/AbdullahAfifyKhalil/egy-names/issues).

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<div align="center">
  <sub>Built with ❤️ by <b><a href="https://github.com/AbdullahAfifyKhalil">Abdullah Afify</a></b></sub>
</div>
