# egy-names (C++)

Egyptian names engine for C++20. Same book as the other SDKs — 44,626 lemmas, offline.

A legal Egyptian name is a patronymic chain, not a first name and a last name. This package generates, translates, splits, and corrects those chains.

**[afify.co/egy-names](https://afify.co/egy-names)** — origin, process, insights, lab, examples, and demo.

**[The Secret Code of Egyptian Names](https://medium.com/@abdullah.afify/the-secret-code-of-egyptian-names-how-we-engineered-a-14-dimensional-nlp-engine-5205db7f04f4)** — how the engine was built.

## Accuracy

The book comes from real records. Some names will still come back wrong — a rare spelling, a name the catalog has never seen. If you find one, [open an issue](https://github.com/AbdullahAfifyKhalil/egy-names/issues).

## Install

```cmake
include(FetchContent)
FetchContent_Declare(egy_names
  GIT_REPOSITORY https://github.com/AbdullahAfifyKhalil/egy-names.git
  GIT_TAG v0.3.8)
FetchContent_MakeAvailable(egy_names)
target_link_libraries(your_target PRIVATE egy_names)
```

The book ships in the clone (`data/names.json.gz`). CMake records that path. You can also set `EGY_NAMES_DATA` to the file or its directory. `v0.3.6` only looked next to the working directory.

## Use

```cpp
#include <egy_names/egy_names.hpp>
#include <iostream>

int main() {
    egy_names::EgyNames e;

    for (const auto& p : e.split("محمدأحمدعليحسنالشناوي")) {
        std::cout << p << " ";
    }
    std::cout << "\n" << e.translate("محمد أحمد علي الشناوي") << "\n";
    std::cout << e.correct("احمد مصطفا عبد الرحيم") << "\n";

    auto name = e.generate(1, 4, "female", "muslim")[0];
    std::cout << name.ar << "  " << name.en << "\n";

    std::cout << e.is_valid("محمد") << "\n";  // true
    std::cout << e.is_valid("الله") << "\n";  // false — in the index, not a person's name

    auto g = e.detect_gender("فاطمة محمد علي");      // first personal token wins
    auto r = e.detect_religion("مينا جرجس بطرس");
    std::cout << g.gender << " " << r.religion << "\n";
}
```

Full API: [DOCUMENTATION.md](https://github.com/AbdullahAfifyKhalil/egy-names/blob/main/DOCUMENTATION.md). Runnable script: [`examples/cpp/`](https://github.com/AbdullahAfifyKhalil/egy-names/tree/main/examples/cpp).

## Other languages

Same book, other SDKs — no samples here. See the [repo](https://github.com/AbdullahAfifyKhalil/egy-names) and [afify.co/egy-names](https://afify.co/egy-names).

## License

MIT. Copyright (c) 2026 Afify by Abdullah Afify. An Afify open-source project.
