# Egyptian Names (`egy-names`) — C++20 / C++17 Library

A high-performance modern C++ library for Egyptian onomastic intelligence — generate, translate, annotate, split, correct, and analyze Egyptian names.

---

## Features

- 🏎️ **Ultra Fast**: Header-only modern C++20 design with zero heap allocations in inner loops.
- 📜 **33,000+ Validated Names**: Full national corpus statistics with demographic and religious indicators.
- 🔀 **Concatenated Name Segmentation**: Dynamic programming shortest-path segmenter for unspaced text.
- 🌍 **Bidirectional Transliteration**: Arabic $\leftrightarrow$ English with phonetic preservation.
- ✍️ **Smart Tashkeel & Correction**: Automatic diacritics and compound name normalization (`عبدالرحمن`).

---

## Installation & Quick Start

### CMake Integration

```cmake
include(FetchContent)
FetchContent_Declare(
    egy_names
    GIT_REPOSITORY https://github.com/AbdullahAfifyKhalil/egy-names.git
    GIT_TAG v0.1.1
)
FetchContent_MakeAvailable(egy_names)

target_link_libraries(your_app PRIVATE egy_names)
```

### Usage

```cpp
#include <egy_names/egy_names.hpp>
#include <iostream>

int main() {
    egy_names::EgyNames en;

    // 1. Generate realistic Egyptian names
    auto names = en.generate(3, 3, "male", "muslim");
    for (const auto& n : names) {
        std::cout << n.ar << " (" << n.en << ")\n";
    }

    // 2. Translate Arabic to English
    std::cout << en.translate("محمد أحمد علي") << "\n";
    // Output: Mohamed Ahmed Ali

    // 3. Orthographic Correction
    std::cout << en.correct("احمد مصطفا عبد الرحيم") << "\n";
    // Output: أحمد مصطفى عبدالرحيم

    // 4. Tashkeel (Diacritization)
    std::cout << en.tashkeel("محمد عبدالرحمن") << "\n";
    // Output: مُحَمَّد عَبْدُالرَّحْمَن

    // 5. Segment concatenated names
    auto parts = en.split("محمدأحمدعليحسنالشاذلي");
    // Output: ["محمد", "أحمد", "علي", "حسن", "الشاذلي"]

    return 0;
}
```

---

## License

MIT License © 2026 Abdullah Afify
