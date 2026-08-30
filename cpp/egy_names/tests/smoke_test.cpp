#include "egy_names/egy_names.hpp"
#include <iostream>
#include <cassert>

int main() {
    std::cout << "Initializing C++ EgyNames library..." << std::endl;
    egy_names::EgyNames en(42);

    // 1. Data Stats
    auto stats = en.stats();
    std::cout << "1. Loaded names: " << stats["total_names"] << std::endl;
    assert(stats["total_names"].get<int>() > 30000);

    // 2. Name Generation
    std::cout << "\n2. Name Generation (3 names):" << std::endl;
    auto names = en.generate(3, 3, "male", "muslim");
    for (const auto& n : names) {
        std::cout << "   " << n.ar << "  --  " << n.en << std::endl;
        assert(!n.ar.empty());
        assert(!n.en.empty());
    }

    // 3. Translation
    std::cout << "\n3. Translation:" << std::endl;
    std::string translated = en.translate("محمد أحمد علي");
    std::cout << "   'محمد أحمد علي' -> " << translated << std::endl;
    assert(translated.find("Mohamed") != std::string::npos || translated.find("Muhammad") != std::string::npos);

    // 4. Correction
    std::cout << "\n4. Correction:" << std::endl;
    std::string corrected = en.correct("احمد مصطفا عبد الرحيم");
    std::cout << "   'احمد مصطفا عبد الرحيم' -> " << corrected << std::endl;
    assert(corrected.find("أحمد") != std::string::npos);
    assert(corrected.find("مصطفى") != std::string::npos);
    assert(corrected.find("عبدالرحيم") != std::string::npos);

    // 5. Tashkeel with compound support
    std::cout << "\n5. Tashkeel (with compound support):" << std::endl;
    std::string tashkeeled = en.tashkeel("محمد عبدالرحمن");
    std::cout << "   'محمد عبدالرحمن' -> " << tashkeeled << std::endl;
    assert(tashkeeled.find("مُحَمَّد") != std::string::npos);
    assert(tashkeeled.find("الرَّحْمَن") != std::string::npos);

    // 5b. 11D Features
    std::cout << "\n5b. 11D Features (Tashkeel Eg, IPA, Dallaa, Roots, Origins, Trends):" << std::endl;
    std::string tk_eg = en.tashkeel_eg("محمد");
    std::string ipa_std = en.ipa("جمال", "standard");
    std::string ipa_eg = en.ipa_eg("جمال");
    auto dallaa = en.dallaa("محمد");
    auto root = en.root("محمد");
    auto origin = en.origin("محمد");
    auto figures = en.famous_figures("محمد");
    auto trend = en.trend("محمد");

    std::cout << "   Tashkeel Eg: " << tk_eg << std::endl;
    std::cout << "   IPA Standard: " << ipa_std << " | IPA Eg: " << ipa_eg << std::endl;
    std::cout << "   Root: " << (root ? *root : "N/A") << " | Origin: " << (origin ? *origin : "N/A") << std::endl;
    assert(!tk_eg.empty());
    assert(ipa_std.front() == '/');
    assert(ipa_eg.front() == '[');
    assert(!dallaa.empty());
    assert(root.has_value() && *root == "ح-م-د");
    assert(origin.has_value() && *origin == "arabic_classical");
    assert(!figures.empty());
    assert(trend.has_value() && *trend == "classic_timeless");

    // 6. Splitting / DP Segmentation
    std::cout << "\n6. Splitting concatenated Arabic names:" << std::endl;
    auto parts = en.split("محمدأحمدعليحسنالشاذلي");
    std::cout << "   'محمدأحمدعليحسنالشاذلي' -> ";
    for (const auto& p : parts) std::cout << "[" << p << "] ";
    std::cout << std::endl;
    assert(parts.size() >= 3);

    // 7. Meaning & Annotation
    std::cout << "\n7. Meaning Annotation:" << std::endl;
    auto meaning = en.meaning("محمد");
    if (meaning) {
        std::cout << "   محمد: " << meaning->first << std::endl;
    }

    // 8. Gender & Religion Inferences
    std::cout << "\n8. Demographics Inferences:" << std::endl;
    auto g = en.detect_gender("مريم إبراهيم حسن");
    std::cout << "   مريم إبراهيم حسن -> gender: " << g.gender << " (conf: " << g.confidence << ")" << std::endl;
    assert(g.gender == "female");

    auto r = en.detect_religion("جورج بطرس سمير ميخائيل");
    std::cout << "   جورج بطرس سمير ميخائيل -> religion: " << r.religion << " (conf: " << r.confidence << ")" << std::endl;
    assert(r.religion == "christian");

    auto first = en.detect_gender("فاطمة محمد علي حسن");
    assert(first.gender == "female");
    assert(!en.is_valid("الله"));
    assert(en.translate("Mahmoud") == "محمود");

    // 9. Chain Analysis
    std::cout << "\n9. Patronymic Chain Analysis:" << std::endl;
    auto chain = en.analyze_chain("محمد أحمد علي حسن الشاذلي");
    for (const auto& cp : chain) {
        std::cout << "   Slot " << cp.slot << ": " << cp.name << " (" << cp.role << ")" << std::endl;
    }
    assert(chain.size() == 5);
    assert(chain[0].role == "person");
    assert(chain[4].role == "family_name");

    std::cout << "\n==========================================" << std::endl;
    std::cout << " All C++ Smoke Tests Passed Successfully!" << std::endl;
    std::cout << "==========================================" << std::endl;

    return 0;
}
