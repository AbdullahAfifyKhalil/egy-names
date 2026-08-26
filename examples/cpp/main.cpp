#include <egy_names/egy_names.hpp>
#include <iostream>
#include <string>

static void print_list(const std::string& label, const std::vector<std::string>& items, std::size_t limit = 8) {
    std::cout << "   " << label;
    for (std::size_t i = 0; i < items.size() && i < limit; ++i) {
        if (i) std::cout << ", ";
        std::cout << items[i];
    }
    std::cout << std::endl;
}

int main() {
    egy_names::EgyNames en;

    std::cout << "============================================================" << std::endl;
    std::cout << " Egyptian Names (egy-names) v0.3.2 — C++20 Showcase" << std::endl;
    std::cout << "============================================================" << std::endl;

    std::cout << "\n1. Name Generation:" << std::endl;
    for (const auto& n : en.generate(3, 4, "female", "muslim")) {
        std::cout << "   " << n.ar << "  (" << n.en << ")" << std::endl;
    }

    std::cout << "\n2. Transliteration:" << std::endl;
    std::cout << "   'محمد أحمد علي الشناوي' -> " << en.translate("محمد أحمد علي الشناوي") << std::endl;

    std::cout << "\n3. Orthographic Correction:" << std::endl;
    std::cout << "   'احمد مصطفا عبد الرحيم' -> " << en.correct("احمد مصطفا عبد الرحيم") << std::endl;

    std::cout << "\n4. Dual Tashkeel & IPA:" << std::endl;
    std::cout << "   Standard: " << en.tashkeel("محمد عبدالرحمن") << std::endl;
    std::cout << "   Egyptian: " << en.tashkeel_eg("محمد عبدالرحمن") << std::endl;
    std::cout << "   IPA std:  " << en.ipa("جمال") << std::endl;
    std::cout << "   IPA eg:   " << en.ipa_eg("جمال") << std::endl;

    std::cout << "\n5. Splitting concatenated names:" << std::endl;
    std::cout << "   ";
    for (const auto& p : en.split("محمدأحمدعليحسنالشناوي")) {
        std::cout << "[" << p << "] ";
    }
    std::cout << std::endl;

    std::cout << "\n6. Pet names & famous figures:" << std::endl;
    print_list("dallaa: ", en.dallaa("محمد", "tashkeel"));
    print_list("figures: ", en.famous_figures("محمد", "en"), 2);

    std::cout << "\n7. 14D lookup:" << std::endl;
    auto root = en.root("محمد");
    auto origin = en.origin("محمد");
    auto trend = en.trend("محمد");
    std::cout << "   root=" << (root ? *root : "null")
              << " | origin=" << (origin ? *origin : "null")
              << " | trend=" << (trend ? *trend : "null") << std::endl;
    if (auto meaning = en.meaning("محمد")) {
        std::cout << "   meaning: " << meaning->second << std::endl;
    }

    std::cout << "\n8. Demographics:" << std::endl;
    auto gender = en.detect_gender("فاطمة الزهراء");
    auto religion = en.detect_religion("مينا جرجس بطرس");
    std::cout << "   " << gender.gender << " (" << gender.confidence << ")" << std::endl;
    std::cout << "   " << religion.religion << " (" << religion.confidence << ")" << std::endl;

    std::cout << "\n9. Chain analysis, rank, uniqueness:" << std::endl;
    for (const auto& p : en.analyze_chain("محمد أحمد علي الشناوي")) {
        std::cout << "   Slot " << p.slot << ": " << p.name << " — " << p.role << std::endl;
    }
    if (auto rank = en.rank("محمد")) {
        auto uniq = en.uniqueness("محمد أحمد علي الشناوي");
        std::cout << "   rank=#" << rank->rank << "  uniqueness=" << uniq.score
                  << " (" << uniq.label << ")" << std::endl;
    }

    return 0;
}
