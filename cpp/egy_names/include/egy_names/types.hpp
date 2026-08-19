#pragma once

#include <string>
#include <vector>
#include <memory>
#include <optional>
#include <unordered_map>

namespace egy_names {

enum class Gender {
    MALE,
    FEMALE,
    NEUTRAL
};

inline std::string gender_to_string(Gender g) {
    switch (g) {
        case Gender::MALE: return "male";
        case Gender::FEMALE: return "female";
        default: return "neutral";
    }
}

inline Gender string_to_gender(const std::string& s) {
    if (s == "m" || s == "male") return Gender::MALE;
    if (s == "f" || s == "female") return Gender::FEMALE;
    return Gender::NEUTRAL;
}

enum class Religion {
    MUSLIM,
    CHRISTIAN,
    NEUTRAL
};

inline std::string religion_to_string(Religion r) {
    switch (r) {
        case Religion::MUSLIM: return "muslim";
        case Religion::CHRISTIAN: return "christian";
        default: return "neutral";
    }
}

inline Religion string_to_religion(const std::string& s) {
    if (s == "m" || s == "muslim") return Religion::MUSLIM;
    if (s == "c" || s == "christian") return Religion::CHRISTIAN;
    return Religion::NEUTRAL;
}

enum class NameRole {
    GIVEN,
    FAMILY
};

inline std::string role_to_string(NameRole r) {
    return r == NameRole::GIVEN ? "given" : "family";
}

inline NameRole string_to_role(const std::string& s) {
    if (s == "f" || s == "family") return NameRole::FAMILY;
    return NameRole::GIVEN;
}

enum class FrequencyClass {
    COMMON,
    NORMAL,
    RARE
};

inline std::string freq_to_string(FrequencyClass f) {
    switch (f) {
        case FrequencyClass::COMMON: return "common";
        case FrequencyClass::NORMAL: return "normal";
        default: return "rare";
    }
}

inline FrequencyClass string_to_freq(const std::string& s) {
    if (s == "c" || s == "common") return FrequencyClass::COMMON;
    if (s == "n" || s == "normal") return FrequencyClass::NORMAL;
    return FrequencyClass::RARE;
}

struct NameEntry {
    std::string ar;
    std::string en;
    Gender gender = Gender::NEUTRAL;
    Religion religion = Religion::NEUTRAL;
    NameRole role = NameRole::GIVEN;
    std::vector<std::string> ar_variants;
    std::vector<std::string> en_variants;
    std::vector<double> slot_pcts;
    double corpus_share = 0.0;
    FrequencyClass frequency = FrequencyClass::NORMAL;
    std::string tashkeel;
    std::string meaning_ar;
    std::string meaning_en;
};

struct NameInfo {
    std::string ar;
    std::string en;
    std::string gender;
    std::string religion;
    std::string role;
    std::string frequency_class;
    double corpus_share = 0.0;
    std::string tashkeel;
    std::string meaning_ar;
    std::string meaning_en;
    std::vector<std::string> ar_variants;
    std::vector<std::string> en_variants;
    std::vector<double> slot_distribution;
};

struct GeneratedName {
    std::string ar;
    std::string en;
    std::vector<std::string> parts_ar;
    std::vector<std::string> parts_en;
};

struct ChainPart {
    std::string name;
    int slot = 0;
    std::string role;
    std::string detail;
};

struct GenderDetection {
    std::string gender;
    double confidence = 0.0;
};

struct ReligionDetection {
    std::string religion;
    double confidence = 0.0;
};

struct RankInfo {
    int rank = 0;
    double percentile = 0.0;
    std::string corpus_share;
    std::string description;
};

struct UniquenessScore {
    double score = 0.0;
    std::string label;
    std::string note;
};

inline NameInfo to_name_info(const NameEntry& e) {
    NameInfo info;
    info.ar = e.ar;
    info.en = e.en;
    info.gender = gender_to_string(e.gender);
    info.religion = religion_to_string(e.religion);
    info.role = role_to_string(e.role);
    info.frequency_class = freq_to_string(e.frequency);
    info.corpus_share = e.corpus_share;
    info.tashkeel = e.tashkeel;
    info.meaning_ar = e.meaning_ar;
    info.meaning_en = e.meaning_en;
    info.ar_variants = e.ar_variants;
    info.en_variants = e.en_variants;
    info.slot_distribution = e.slot_pcts;
    return info;
}

} // namespace egy_names
