#pragma once

#include "types.hpp"
#include "data_loader.hpp"
#include "lookup_indices.hpp"
#include "generator.hpp"
#include "translator.hpp"
#include "corrector.hpp"
#include "splitter.hpp"
#include "annotator.hpp"
#include "search.hpp"

#include <string>
#include <vector>
#include <optional>
#include <sstream>
#include <cmath>
#include <iomanip>

namespace egy_names {

class EgyptianNames {
private:
    std::string custom_data_path;
    int default_seed = -1;

    static bool is_compound_prefix(const std::string& prefix) {
        std::string p = LookupIndices::normalize_ar(prefix);
        return (p == "عبد" || p == "ابو" || p == "ابن" || p == "ام" ||
                p == "نور" || p == "سيف" || p == "شمس" || p == "منه" ||
                p == "فاطمه" || p == "علاء" || p == "بهاء" || p == "ضياء" ||
                p == "سراج" || p == "محيي" || p == "حسام" || p == "تقي");
    }

public:
    explicit EgyptianNames(int seed = -1, const std::string& data_path = "")
        : custom_data_path(data_path), default_seed(seed)
    {
        LookupIndices::ensure_built(custom_data_path);
    }

    std::vector<GeneratedName> generate(
        int count = 5,
        int length = 3,
        const std::string& gender = "",
        const std::string& religion = "",
        int seed = -1)
    {
        int s = (seed >= 0) ? seed : default_seed;
        return Generator::generate(count, length, gender, religion, s, custom_data_path);
    }

    std::string translate(const std::string& name) {
        return Translator::translate(name, custom_data_path);
    }

    std::string correct(const std::string& name) {
        return Corrector::correct(name, custom_data_path);
    }

    std::string tashkeel(const std::string& name, const std::string& dialect = "standard") {
        if (name.empty()) return name;

        std::stringstream ss(name);
        std::string tok;
        std::vector<std::string> raw_tokens;
        while (ss >> tok) {
            raw_tokens.push_back(tok);
        }

        bool is_eg = (dialect.find("eg") != std::string::npos || dialect.find("Eg") != std::string::npos);
        std::vector<std::string> result;
        for (size_t i = 0; i < raw_tokens.size(); ++i) {
            std::string current = raw_tokens[i];

            if (i + 1 < raw_tokens.size() && is_compound_prefix(current)) {
                std::string next = raw_tokens[i + 1];
                std::string compound = current + " " + next;
                std::string compound_no_space = current + next;

                auto compound_entry = LookupIndices::lookup_ar(compound, custom_data_path);
                if (!compound_entry.has_value()) {
                    compound_entry = LookupIndices::lookup_ar(compound_no_space, custom_data_path);
                }

                if (compound_entry.has_value()) {
                    std::string val = is_eg ? compound_entry->tashkeel_eg : compound_entry->tashkeel_standard;
                    if (!val.empty()) {
                        result.push_back(val);
                        i++;
                        continue;
                    }
                }
            }

            auto entry = LookupIndices::lookup_ar(current, custom_data_path);
            if (entry.has_value()) {
                std::string val = is_eg ? entry->tashkeel_eg : entry->tashkeel_standard;
                result.push_back(!val.empty() ? val : current);
            } else {
                result.push_back(current);
            }
        }

        std::string out;
        for (size_t i = 0; i < result.size(); ++i) {
            if (i > 0) out += " ";
            out += result[i];
        }
        return out;
    }

    std::string tashkeel_eg(const std::string& name) {
        return tashkeel(name, "egyptian");
    }

    std::string ipa(const std::string& name, const std::string& dialect = "standard") {
        if (name.empty()) return "";
        std::vector<std::string> tokens = (name.find(' ') != std::string::npos) ? split_words(name) : split(name);
        bool is_eg = (dialect.find("eg") != std::string::npos || dialect.find("Eg") != std::string::npos);
        std::vector<std::string> ipa_parts;

        for (const auto& tok : tokens) {
            auto entry = LookupIndices::lookup(tok, custom_data_path);
            if (entry.has_value()) {
                std::string ipa_val = is_eg ? entry->ipa_eg : entry->ipa_standard;
                if (!ipa_val.empty()) {
                    // strip delimiters
                    std::string clean_ipa;
                    for (char c : ipa_val) {
                        if (c != '/' && c != '[' && c != ']') clean_ipa += c;
                    }
                    ipa_parts.push_back(clean_ipa);
                } else {
                    ipa_parts.push_back(tok);
                }
            } else {
                ipa_parts.push_back(tok);
            }
        }

        std::string joined;
        for (size_t i = 0; i < ipa_parts.size(); ++i) {
            if (i > 0) joined += " ";
            joined += ipa_parts[i];
        }
        return is_eg ? ("[" + joined + "]") : ("/" + joined + "/");
    }

    std::string ipa_eg(const std::string& name) {
        return ipa(name, "egyptian");
    }

    std::vector<std::string> dallaa(const std::string& name, const std::string& format = "plain") {
        auto entry = LookupIndices::lookup(name, custom_data_path);
        if (!entry.has_value()) return {};
        std::string fmt = format;
        std::transform(fmt.begin(), fmt.end(), fmt.begin(), ::tolower);
        if (fmt == "tashkeel" || fmt == "tashkeel_eg" || fmt == "tk") {
            return !entry->dallaa_tashkeel.empty() ? entry->dallaa_tashkeel : entry->dallaa_ar;
        } else if (fmt == "en" || fmt == "english") {
            return entry->dallaa_en;
        } else if (fmt == "ipa" || fmt == "phonetic") {
            return entry->dallaa_ipa;
        }
        return entry->dallaa_ar;
    }

    std::vector<PetName> dallaa_info(const std::string& name) {
        auto entry = LookupIndices::lookup(name, custom_data_path);
        if (!entry.has_value() || entry->dallaa_ar.empty()) return {};
        std::vector<PetName> res;
        for (size_t i = 0; i < entry->dallaa_ar.size(); ++i) {
            std::string ar = entry->dallaa_ar[i];
            std::string tk = i < entry->dallaa_tashkeel.size() ? entry->dallaa_tashkeel[i] : ar;
            std::string en = i < entry->dallaa_en.size() ? entry->dallaa_en[i] : "";
            std::string ipa = i < entry->dallaa_ipa.size() ? entry->dallaa_ipa[i] : "";
            res.push_back({ar, tk, en, ipa});
        }
        return res;
    }

    std::vector<std::string> pet_names(const std::string& name, const std::string& format = "plain") {
        return dallaa(name, format);
    }

    std::optional<std::string> root(const std::string& name) {
        auto entry = LookupIndices::lookup(name, custom_data_path);
        if (entry.has_value() && entry->root != "N/A") return entry->root;
        return std::nullopt;
    }

    std::optional<std::string> origin(const std::string& name) {
        auto entry = LookupIndices::lookup(name, custom_data_path);
        if (entry.has_value()) return entry->origin_type;
        return std::nullopt;
    }

    std::vector<std::string> famous_figures(const std::string& name, const std::string& lang = "ar") {
        auto entry = LookupIndices::lookup(name, custom_data_path);
        if (!entry.has_value()) return {};
        std::string l = lang;
        std::transform(l.begin(), l.end(), l.begin(), ::tolower);
        if (l.rfind("en", 0) == 0) {
            return !entry->famous_figures_en.empty() ? entry->famous_figures_en : entry->famous_figures_ar;
        }
        return entry->famous_figures_ar;
    }

    std::optional<std::string> trend(const std::string& name) {
        auto entry = LookupIndices::lookup(name, custom_data_path);
        if (entry.has_value()) return entry->trend_category;
        return std::nullopt;
    }

    static std::vector<std::string> split_words(const std::string& s) {
        std::stringstream ss(s);
        std::string w;
        std::vector<std::string> res;
        while (ss >> w) res.push_back(w);
        return res;
    }

    std::vector<std::string> split(const std::string& fullName) {
        return Splitter::split(fullName, custom_data_path);
    }

    std::vector<NameInfo> annotate(const std::string& fullName) {
        return Annotator::annotate(fullName, custom_data_path);
    }

    std::optional<NameInfo> annotate_single(const std::string& name) {
        return Annotator::annotate_single(name, custom_data_path);
    }

    std::optional<std::pair<std::string, std::string>> meaning(const std::string& name) {
        auto entry = LookupIndices::lookup(name, custom_data_path);
        if (!entry.has_value()) return std::nullopt;
        if (entry->meaning_ar.empty() && entry->meaning_en.empty()) return std::nullopt;
        return std::make_pair(entry->meaning_ar, entry->meaning_en);
    }

    std::vector<NameInfo> families(
        int count = 50,
        std::optional<FrequencyClass> frequency = std::nullopt,
        std::optional<Religion> religion = std::nullopt,
        const std::string& starts_with = "")
    {
        return SearchEngine::search(
            std::nullopt, religion, NameRole::FAMILY, frequency,
            starts_with, "", "", 0.0, count, "corpus_share", custom_data_path);
    }

    std::vector<NameInfo> search(
        std::optional<Gender> gender = std::nullopt,
        std::optional<Religion> religion = std::nullopt,
        std::optional<NameRole> role = std::nullopt,
        std::optional<FrequencyClass> frequency = std::nullopt,
        const std::string& starts_with = "",
        const std::string& ends_with = "",
        const std::string& contains = "",
        double min_corpus_share = 0.0,
        int max_results = 50,
        const std::string& sort_by = "corpus_share")
    {
        return SearchEngine::search(
            gender, religion, role, frequency,
            starts_with, ends_with, contains, min_corpus_share, max_results, sort_by, custom_data_path);
    }

    GenderDetection detect_gender(const std::string& fullName) {
        auto parts = split(fullName);
        if (parts.empty()) return {"unknown", 0.0};

        auto first_entry = LookupIndices::lookup(parts[0], custom_data_path);
        if (!first_entry.has_value() || first_entry->gender == Gender::NEUTRAL) {
            return {"neutral", 0.5};
        }

        double confidence = (first_entry->gender == Gender::FEMALE) ? 0.95 : 0.90;
        return {gender_to_string(first_entry->gender), confidence};
    }

    ReligionDetection detect_religion(const std::string& fullName) {
        auto parts = split(fullName);
        if (parts.empty()) return {"unknown", 0.0};

        int c_count = 0, m_count = 0;
        for (const auto& p : parts) {
            auto entry = LookupIndices::lookup(p, custom_data_path);
            if (!entry.has_value()) continue;
            if (entry->religion == Religion::CHRISTIAN) c_count++;
            else if (entry->religion == Religion::MUSLIM) m_count++;
        }

        if (c_count > 0 && c_count >= m_count) {
            return {"christian", std::min(0.99, 0.60 + c_count * 0.20)};
        }
        if (m_count > 0) {
            return {"muslim", std::min(0.99, 0.60 + m_count * 0.15)};
        }
        return {"neutral", 0.5};
    }

    std::vector<ChainPart> analyze_chain(const std::string& fullName) {
        auto parts = split(fullName);
        std::vector<ChainPart> chain;
        int n = static_cast<int>(parts.size());

        for (int i = 0; i < n; ++i) {
            ChainPart cp;
            cp.name = parts[i];
            cp.slot = i + 1;

            if (i == 0) {
                cp.role = "person";
                cp.detail = "Given Name (اسم الشخص)";
            } else if (i == 1) {
                cp.role = "father";
                cp.detail = "Father's Name (اسم الأب)";
            } else if (i == 2) {
                cp.role = "grandfather";
                cp.detail = "Grandfather's Name (اسم الجد)";
            } else if (i == n - 1 && n >= 4) {
                cp.role = "family_name";
                cp.detail = "Family / Surname (اللقب / اسم العائلة)";
            } else {
                cp.role = "ancestor";
                cp.detail = "Ancestor Name (السلف)";
            }

            chain.push_back(cp);
        }
        return chain;
    }

    std::optional<RankInfo> rank(const std::string& name) {
        auto entry = LookupIndices::lookup(name, custom_data_path);
        if (!entry.has_value()) return std::nullopt;

        const auto& ranked = LookupIndices::get_ranked(custom_data_path);
        int pos = 1;
        for (const auto& r : ranked) {
            if (r.ar == entry->ar) break;
            pos++;
        }

        double percentile = 100.0 * (1.0 - static_cast<double>(pos) / ranked.size());
        RankInfo ri;
        ri.rank = pos;
        ri.percentile = percentile;
        std::stringstream ss;
        ss << std::fixed << std::setprecision(4) << entry->corpus_share << "%";
        ri.corpus_share = ss.str();
        ri.description = "Rank #" + std::to_string(pos) + " of " + std::to_string(ranked.size());
        return ri;
    }

    UniquenessScore uniqueness(const std::string& fullName) {
        auto parts = split(fullName);
        if (parts.empty()) return {0.0, "unknown", "Empty name"};

        double prod = 1.0;
        int found = 0;

        for (const auto& p : parts) {
            auto entry = LookupIndices::lookup(p, custom_data_path);
            if (entry.has_value() && entry->corpus_share > 0.0) {
                prod *= (entry->corpus_share / 100.0);
                found++;
            }
        }

        if (found == 0) return {0.5, "moderate", "Unranked name elements"};

        double score = 1.0 - std::min(1.0, prod * 10000.0);
        std::string label;
        if (score > 0.85) label = "rare";
        else if (score > 0.60) label = "distinctive";
        else if (score > 0.35) label = "moderate";
        else label = "common";

        return {score, label, "Estimated uniqueness score"};
    }

    bool is_valid(const std::string& name) {
        return LookupIndices::lookup(name, custom_data_path).has_value();
    }

    nlohmann::json stats() {
        LookupIndices::ensure_built(custom_data_path);
        const auto& all = LookupIndices::get_all(custom_data_path);
        int given = 0, family = 0, male = 0, female = 0;

        for (const auto& e : all) {
            if (e.role == NameRole::GIVEN) given++;
            else family++;
            if (e.gender == Gender::MALE) male++;
            else if (e.gender == Gender::FEMALE) female++;
        }

        nlohmann::json s;
        s["total_names"] = all.size();
        s["given_names"] = given;
        s["family_names"] = family;
        s["male_names"] = male;
        s["female_names"] = female;
        s["metadata"] = LookupIndices::get_metadata(custom_data_path);
        return s;
    }
};

using EgyNames = EgyptianNames;

} // namespace egy_names
