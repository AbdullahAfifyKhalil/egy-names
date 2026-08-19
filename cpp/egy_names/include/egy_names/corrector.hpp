#pragma once

#include "types.hpp"
#include "lookup_indices.hpp"
#include <string>
#include <vector>
#include <sstream>

namespace egy_names {

class Corrector {
private:
    static bool is_compound_prefix(const std::string& prefix) {
        std::string p = LookupIndices::normalize_ar(prefix);
        return (p == "عبد" || p == "ابو" || p == "ابن" || p == "ام" ||
                p == "نور" || p == "سيف" || p == "شمس" || p == "منه" ||
                p == "فاطمه" || p == "علاء" || p == "بهاء" || p == "ضياء" ||
                p == "سراج" || p == "محيي" || p == "حسام" || p == "تقي");
    }

public:
    static std::string correct_token(const std::string& token, const std::string& data_path = "") {
        if (token.empty()) return token;

        // 1. Direct surface correction
        auto canonical = LookupIndices::get_correction(token, data_path);
        if (canonical.has_value()) return *canonical;

        // 2. Exact match in index
        auto entry = LookupIndices::lookup_ar(token, data_path);
        if (entry.has_value()) return entry->ar;

        // 3. Normalized match
        std::string norm = LookupIndices::normalize_ar(token);
        const auto& ar_norm = LookupIndices::get_ar_norm_forms(data_path);
        auto it = ar_norm.find(norm);
        if (it != ar_norm.end()) return it->second.ar;

        // 4. Trailing Alif / Alif Maqsura check
        static const std::string alif_utf8 = "\u0627";
        static const std::string ya_utf8 = "\u064A";

        if (norm.size() >= alif_utf8.size() && norm.compare(norm.size() - alif_utf8.size(), alif_utf8.size(), alif_utf8) == 0) {
            std::string alt = norm.substr(0, norm.size() - alif_utf8.size()) + ya_utf8;
            auto it_alt = ar_norm.find(alt);
            if (it_alt != ar_norm.end()) return it_alt->second.ar;
        } else if (norm.size() >= ya_utf8.size() && norm.compare(norm.size() - ya_utf8.size(), ya_utf8.size(), ya_utf8) == 0) {
            std::string alt = norm.substr(0, norm.size() - ya_utf8.size()) + alif_utf8;
            auto it_alt = ar_norm.find(alt);
            if (it_alt != ar_norm.end()) return it_alt->second.ar;
        }

        return token;
    }

    static std::string correct(const std::string& name, const std::string& data_path = "") {
        if (name.empty()) return name;

        std::stringstream ss(name);
        std::string tok;
        std::vector<std::string> raw_tokens;
        while (ss >> tok) {
            raw_tokens.push_back(tok);
        }

        std::vector<std::string> result;
        for (size_t i = 0; i < raw_tokens.size(); ++i) {
            std::string current = raw_tokens[i];

            // Check compound pair (e.g. "عبد" + "الرحيم" -> "عبدالرحيم")
            if (i + 1 < raw_tokens.size() && is_compound_prefix(current)) {
                std::string next = raw_tokens[i + 1];
                std::string compound = current + " " + next;
                std::string compound_no_space = current + next;

                auto compound_entry = LookupIndices::lookup_ar(compound, data_path);
                if (!compound_entry.has_value()) {
                    compound_entry = LookupIndices::lookup_ar(compound_no_space, data_path);
                }

                if (compound_entry.has_value()) {
                    result.push_back(compound_entry->ar);
                    i++; // skip next
                    continue;
                }
            }

            result.push_back(correct_token(current, data_path));
        }

        std::string out;
        for (size_t i = 0; i < result.size(); ++i) {
            if (i > 0) out += " ";
            out += result[i];
        }
        return out;
    }
};

} // namespace egy_names
