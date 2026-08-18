#include <egy_names/egy_names.hpp>
#include <iostream>

int main() {
    egy_names::EgyNames en;

    std::cout << "============================================================" << std::endl;
    std::cout << " Egyptian Names (egy-names) - C++20 Showcase" << std::endl;
    std::cout << "============================================================" << std::endl;

    // 1. Generation
    std::cout << "\n1. Name Generation:" << std::endl;
    auto names = en.generate(3, 3, "male", "muslim");
    for (const auto& n : names) {
        std::cout << "   " << n.ar << "  (" << n.en << ")" << std::endl;
    }

    // 2. Translation
    std::cout << "\n2. Transliteration:" << std::endl;
    std::cout << "   'محمد أحمد علي' -> " << en.translate("محمد أحمد علي") << std::endl;

    // 3. Correction
    std::cout << "\n3. Correction:" << std::endl;
    std::cout << "   'احمد مصطفا عبد الرحيم' -> " << en.correct("احمد مصطفا عبد الرحيم") << std::endl;

    // 4. Tashkeel
    std::cout << "\n4. Tashkeel:" << std::endl;
    std::cout << "   'محمد عبدالرحمن' -> " << en.tashkeel("محمد عبدالرحمن") << std::endl;

    // 5. Splitting
    std::cout << "\n5. Splitting:" << std::endl;
    auto parts = en.split("محمدأحمدعليحسن");
    std::cout << "   'محمدأحمدعليحسن' -> ";
    for (const auto& p : parts) std::cout << "[" << p << "] ";
    std::cout << std::endl;

    return 0;
}
