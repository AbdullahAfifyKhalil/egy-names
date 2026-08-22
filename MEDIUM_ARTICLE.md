# Solving the Arabic Name Problem in Modern NLP: Why Western Assumptions Fail and How We Built egy-names Across 7 Languages

### *From Pharaonic substrates and patronymic Markov chains to 14-dimensional linguistic intelligence, sub-millisecond transliteration, and 100% deterministic parity in Python, TypeScript, C#, Swift, Java, Dart, and C++.*

---

![Egyptian Names Banner](https://raw.githubusercontent.com/AbdullahAfifyKhalil/egy-names/main/assets/banner.png)

---

## 1. The Broken Paradigm: Why Western Name Schemas Fail

For decades, modern software architecture, relational database schemas, and Natural Language Processing (NLP) pipelines have operated on a Western-centric assumption:

$$\text{Person} = \text{First Name} + \text{Middle Initial (Optional)} + \text{Last Name (Family Surname)}$$

In systems deployed across Egypt and the broader Arab world, this fundamental assumption collapses immediately.

In Egypt—the most populous nation in the Arab world with over 115 million citizens—personal naming does not follow the nuclear family surname convention. Instead, it is governed by an **unbroken patronymic genealogical chain**:

$$\text{Full Legal Name} = \text{Personal Name} \to \text{Father} \to \text{Grandfather} \to \text{Great-Grandfather} \to \dots \to \text{Family / Clan Toponym}$$

When an enterprise database or machine learning pipeline attempts to parse an Egyptian customer name like:

$$\text{Ahmed Mohamed Hassan Ali El-Shenawy}$$

assigning `Ahmed` as the "First Name" and `El-Shenawy` as the "Last Name" discards the critical generational structure that dictates legal identity, KYC verification, credit scoring, demographic calibration, and conversational NLP.

### The Computational Challenges of Egyptian Onomastics

1. **Patronymic Slot Specialization**: Certain names appear almost exclusively as personal first names (e.g., *Fatma*, *Aya*, *Menna*), others strictly as deep ancestral patronymics, and others as geographic or guild-based clan surnames (e.g., *El-Miniawy*, *El-Gowharji*).
2. **Compound Name Fusion**: Names such as *Abdelrahman*, *Nour Eldin*, *Fatma Elzahraa*, and *Abou Bakr* are frequently written with spaces, without spaces, or with hyphens, confusing naive whitespace splitters.
3. **Spelling Permutations in Latin Script**: Because Arabic is written without mandatory short vowels, a single Arabic lemma like **محمد** can be legitimately transliterated in over 20 ways (*Mohamed, Mohammad, Muhammad, Muhammed, Mohamad, etc.*).
4. **Dialectal Phonetic Shifts**: Egyptian Arabic features a distinct phonological system, notably the glottal and velar transformations where the classical Arabic consonant **ج** (/d͡ʒ/) shifts to voiced velar plosive **[ɡ]**, and **ق** (/q/) shifts to glottal stop **[ʔ]**.
5. **Orthographic Noise**: Common typing variations between Alif Maqsura (**ى**) and Ya (**ي**), or ambiguous Hamza placement (**أ / إ / ا**), create massive data fragmentation across government and commercial registries.

To resolve these challenges once and for all, we designed and built **`egy-names`**: an open-source, production-grade onomastic intelligence and computational linguistic engine grounded in a verified corpus of **44,626 canonical Egyptian names** and **3.79 million demographic records**.

---

## 2. The Multi-Layered Heritage of Egyptian Names

Egyptian onomastics represents a continuous, four-millennium synthesis of four cultural layers:

| Cultural Substrate | Example Lemmas (Arabic) | Latin Transliteration | Historical and Etymological Significance |
| :--- | :--- | :--- | :--- |
| **Ancient Egyptian & Coptic** | مهرائيل , سوريال , بهنس , مينا | *Mehraeil, Soryal, Bahnas, Mina* | Pharaonic theophoric names and Christian heritage rooted in the Coptic language. |
| **Classical Arabic / Islamic** | محمد , عبد الرحمن , فاطمة , نور الدين | *Mohamed, Abdelrahman, Fatma, Nour Eldin* | Triliteral Semitic root morphology and Islamic theophoric attributes (*Abdel-*). |
| **Ottoman & Guild Surnames** | الجوهرجي , بوادقجي , خاقان , شلتوت | *Gowharji, Bawadqji, Khaqan, Shaltout* | Professional guild designations, military titles, and aristocratic family surnames. |
| **Nile Geographic Toponyms** | المنياوي , الطهطاوي , الشناوي , الدمياطي | *Elminyawy, Tahtawy, Elshenawy, Domyaty* | Toponymic surnames derived from the 27 governorates of Upper and Lower Egypt. |

---

## 3. Core Architecture & Feature Intelligence

The `egy-names` engine is built as an immutable, zero-dependency, compiled computational library delivering 14 distinct dimensions of onomastic intelligence per lemma:

![Egyptian Names Architecture](https://raw.githubusercontent.com/AbdullahAfifyKhalil/egy-names/main/assets/logo.png)

### 1. Grounded Patronymic Generation Engine
Rather than selecting names randomly from a flat dictionary, `egy-names` models patronymic succession using position-dependent probability vectors derived from millions of real-world cohorts:

$$P(\text{Token}_i = w \mid \text{Slot} = i, \text{Gender} = g, \text{Religion} = r)$$

- **Slot 1 (Personal Name)**: Reflects contemporary generational naming distributions, calibrated to male, female, or neutral genders.
- **Slot 2–4 (Father, Grandfather, Great-Grandfather)**: Restrained strictly to attested male patronymics according to historical frequency vectors.
- **Slot 5 (Clan / Family Surname)**: Biased toward true toponymic, occupational, and lineage surnames.

### 2. Dynamic Programming Concatenated Name Splitter
In unstructured text and legacy databases, spaces between compound tokens and consecutive names are frequently dropped (e.g., `محمدأحمدعليحسنمحمودالشناوي`).

`egy-names` solves this via a Dynamic Programming Viterbi lattice that evaluates all candidate token boundary segmentations and selects the maximum likelihood path:

$$\hat{S} = \arg\max_{S = (t_1, \dots, t_k)} \sum_{j=1}^{k} \log P(t_j \mid \text{Slot}_j) - \lambda \cdot \text{CompoundPenalty}$$

It atomically preserves compound names like *Abdelrahman* (**عبدالرحمن**), *Nour Eldin* (**نورالدين**), and *Fatma Elzahraa* (**فاطمة الزهراء**) without destructive fragmentation.

### 3. 14-Dimensional Deep Linguistic Intelligence
Each lemma in the lexicon is enriched with:
- **Dual Vocalized Tashkeel**: Standard Modern Standard Arabic (MSA) alongside authentic Egyptian Colloquial vocalization (e.g., Standard: `مُحَمَّد`, Egyptian: `مُحَمَّدْ`).
- **Dual IPA Phonetics**: International Phonetic Alphabet transcriptions capturing Egyptian dialectal realizations (e.g., `جمال` $\to$ Standard: `/d͡ʒamaːl/`, Egyptian: `[ɡæˈmæːl]`).
- **Bilingual Diminutives / Pet Names (أسماء الدلع)**: Attested Egyptian nicknames in Arabic, vocalized Tashkeel, English transliteration, and IPA (e.g., `محمد` $\to$ *Mido* `مِيدُو` `[ˈmiːdu]`, *Hamou* `حَمُّو` `[ˈħæm.mu]`, *Hamouda* `حَمُّودَة` `[ħæmˈmuːdæ]`).
- **Historical & Cultural Figures (الأسماء المشهورة)**: Curated notable figures in Arabic and English (e.g., `محمد صلاح`, *Mohamed Ali Pasha*, *Naguib Mahfouz*).
- **Semitic Morphological Roots**: Extraction of triliteral and quadriliteral roots (e.g., `ح-م-د`, `ع-ب-د`, `س-ل-م`).
- **Generational Age Intelligence**: Gaussian distribution modeling estimating chronological age brackets based on multi-token patronymic combinations.
- **Calibrated Bayesian Demographics**: Robust statistical gender and religious denomination classification.

---

## 4. 100% Deterministic Cross-Language Parity

A core engineering requirement of `egy-names` was **absolute deterministic parity**: a test case executed in Python must produce the exact same phonetic transcription, token segmentation, and patronymic generation sequence when executed in TypeScript, C#, Swift, Java, Dart, or C++.

### Python
```bash
pip install egy-names
```
```python
from egy_names import EgyptianNames

en = EgyptianNames()

# 1. Grounded Patronymic Generation
names = en.generate(count=3, gender="female", religion="muslim", length=4)
for n in names:
    print(f"Arabic:  {n.ar}")
    print(f"English: {n.en}")

# 2. Dynamic Programming Token Segmentation
tokens = en.split("محمدأحمدعليحسنمحمودالشناوي")
print("Split tokens:", tokens)

# 3. Dual Tashkeel & Egyptian IPA
print("Standard Tashkeel:", en.tashkeel_standard("محمد"))  # مُحَمَّد
print("Egyptian Tashkeel:", en.tashkeel_eg("محمد"))        # مُحَمَّدْ
print("Egyptian IPA:", en.ipa_eg("جمال"))                  # [ɡæˈmæːl]

# 4. Multi-Format Diminutives (Pet Names / Dalaa)
pet_names = en.dallaa("محمد", format="plain")
print("Pet Names:", pet_names)  # ['ميدو', 'حمو', 'حمودة']

# 5. Generational Age Estimation
age_info = en.detect_age("كريم أشرف فاروق")
print(f"Estimated Age: {age_info.mean_age} (Confidence: {age_info.confidence})")
```

---

### TypeScript / JavaScript (Node & Browser)
```bash
npm install egy-names
```
```typescript
import { EgyptianNames } from "egy-names";

const en = new EgyptianNames();

// Patronymic Generation
const names = en.generate({ count: 2, gender: "male", religion: "muslim", length: 4 });
console.log(names[0].ar, "->", names[0].en);

// Unspaced Segmentation
const split = en.split("عبدالرحمنمحمدالشناوي");
console.log(split); // ["عبدالرحمن", "محمد", "الشناوي"]

// Egyptian IPA
console.log(en.ipaEg("جمال")); // [ɡæˈmæːl]
```

---

### C# / .NET
```bash
dotnet add package egy-names
```
```csharp
using EgyNames;

var en = new EgyptianNames();

// 1. Generation
var names = en.Generate(new GenerationOptions { Count = 3, Gender = "male", Length = 4 });
foreach (var name in names) {
    Console.WriteLine($"{name.Ar} | {name.En}");
}

// 2. High-Performance Splitting
var tokens = en.Split("فاطمةالزهراءأحمدعلي");
```

---

### Swift (iOS, macOS, watchOS, Server Swift)
```swift
// In Package.swift dependencies:
.package(url: "https://github.com/AbdullahAfifyKhalil/egy-names.git", from: "0.3.2")
```
```swift
import EgyNames

let en = EgyptianNames()

// Native Swift Onomastic Intelligence
let generated = en.generate(count: 3, gender: "female", length: 4)
for name in generated {
    print("\(name.ar) -> \(name.en)")
}

let tokens = en.split("محمدعليالسيد")
let ipa = en.ipaEg("جمال") // [ɡæˈmæːl]
```

---

### Flutter & Dart
```bash
dart pub add egy_names
```
```dart
import 'package:egy_names/egy_names.dart';

void main() {
  final en = EgyptianNames();
  
  final names = en.generate(count: 3, gender: 'female', length: 4);
  for (final n in names) {
    print('${n.ar} (${n.en})');
  }
}
```

---

### Java & Android
```xml
<!-- In Maven pom.xml -->
<dependency>
    <groupId>io.github.abdullahafifykhalil</groupId>
    <artifactId>egy-names</artifactId>
    <version>0.3.2</version>
</dependency>
```
```java
import com.afify.egynames.EgyptianNames;
import com.afify.egynames.GeneratedName;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        EgyptianNames en = new EgyptianNames();
        List<GeneratedName> names = en.generate(3, "male", "muslim", 4);
        names.forEach(n -> System.out.println(n.getAr() + " -> " + n.getEn()));
    }
}
```

---

### Modern C++ (C++17 / C++20)
```cmake
# In CMakeLists.txt via FetchContent:
include(FetchContent)
FetchContent_Declare(
    egy_names
    GIT_REPOSITORY https://github.com/AbdullahAfifyKhalil/egy-names.git
    GIT_TAG v0.3.2
    SOURCE_SUBDIR cpp/egy_names
)
FetchContent_MakeAvailable(egy_names)
```
```cpp
#include "egy_names.hpp"
#include <iostream>

int main() {
    egy_names::EgyptianNames en;
    auto names = en.generate(3, "male", "muslim", 4);
    for (const auto& n : names) {
        std::cout << n.ar << " | " << n.en << "\n";
    }
    return 0;
}
```

---

## 5. Performance Benchmarks

Engineered for high-throughput data processing and low-latency production APIs, `egy-names` is profiled against aggressive stress tests:

| Metric / Operation | Python Performance | TypeScript / Node Performance | Hardware / Environment |
| :--- | :--- | :--- | :--- |
| **Token Lookup & Transliteration** | **1,536,517 lookups / sec** | **7,453,925 lookups / sec** | Apple Silicon (M-Series) |
| **Dynamic Programming Segmentation** | **8,542 full chains / sec** | **22,800 full chains / sec** | Multi-token Concatenated Lattice |
| **Grounded Patronymic Generation** | **173 complete 4-slot chains / sec** | **2,165 complete 4-slot chains / sec** | Markov Patronymic Probability Model |
| **Binary Memory Footprint** | **$< 35\text{ MB}$ RSS** | **$< 28\text{ MB}$ RSS** | Zero External C Extensions |
| **Adversarial Safety Pass Rate** | **100% (25 / 25 Suites Passed)** | **100% (13 / 13 Suites Passed)** | SQL Injection, Unicode Noise, Null Bounds |

---

## 6. Official Registries & Ecosystem Links

Every SDK is published to its official native package manager:

- **Python (PyPI)**: [https://pypi.org/project/egy-names/](https://pypi.org/project/egy-names/)
- **TypeScript / JavaScript (npm)**: [https://www.npmjs.com/package/egy-names](https://www.npmjs.com/package/egy-names)
- **Dart / Flutter (pub.dev)**: [https://pub.dev/packages/egy_names](https://pub.dev/packages/egy_names)
- **Java / Android (Maven Central)**: [https://central.sonatype.com/artifact/io.github.abdullahafifykhalil/egy-names](https://central.sonatype.com/artifact/io.github.abdullahafifykhalil/egy-names)
- **Java / Android (JitPack)**: [https://jitpack.io/#AbdullahAfifyKhalil/egy-names/v0.3.2](https://jitpack.io/#AbdullahAfifyKhalil/egy-names/v0.3.2)
- **C# / .NET (NuGet)**: [https://www.nuget.org/packages/egy-names/](https://www.nuget.org/packages/egy-names/)
- **Swift (Apple SPM)**: [https://github.com/AbdullahAfifyKhalil/egy-names](https://github.com/AbdullahAfifyKhalil/egy-names)
- **Modern C++ (CMake)**: [https://github.com/AbdullahAfifyKhalil/egy-names/tree/main/cpp/egy_names](https://github.com/AbdullahAfifyKhalil/egy-names/tree/main/cpp/egy_names)
- **Hugging Face (14D Lexicon Dataset)**: [https://huggingface.co/datasets/Abdullah-afify/egyptian-names](https://huggingface.co/datasets/Abdullah-afify/egyptian-names)
- **Hugging Face (3.79M Student Degrees Dataset)**: [https://huggingface.co/datasets/Abdullah-afify/egyptian-high-school-students-grades](https://huggingface.co/datasets/Abdullah-afify/egyptian-high-school-students-grades)
- **GitHub Master Repository**: [https://github.com/AbdullahAfifyKhalil/egy-names](https://github.com/AbdullahAfifyKhalil/egy-names)
- **Complete Technical API Reference**: [https://github.com/AbdullahAfifyKhalil/egy-names/blob/main/DOCUMENTATION.md](https://github.com/AbdullahAfifyKhalil/egy-names/blob/main/DOCUMENTATION.md)

---

## 7. Conclusion

Names are not arbitrary strings; they are structured cultural, historical, and demographic artifacts. In Arabic NLP and computational onomastics, treating names with mathematical rigor and phonetic accuracy transforms KYC verification, identity resolution, conversational AI, and demographic analysis.

`egy-names` is open-source under the MIT License and ready for production deployment across any stack.

If you find this project valuable for your research, enterprise infrastructure, or applications, consider starring the repository on GitHub and joining our open-source contributor community.
