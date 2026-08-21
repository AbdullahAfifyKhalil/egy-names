#pragma once

#include "types.hpp"
#include "lookup_indices.hpp"
#include <string>
#include <vector>
#include <sstream>

namespace egy_names {

class Translator {
private:
    static bool is_compound_prefix(const std::string& prefix) {
        std::string p = LookupIndices::normalize_ar(prefix);
        return (p == "عبد" || p == "ابو" || p == "ابن" || p == "ام" ||
                p == "نور" || p == "سيف" || p == "شمس" || p == "منه" ||
                p == "فاطمه" || p == "علاء" || p == "بهاء" || p == "ضياء" ||
                p == "سراج" || p == "محيي" || p == "حسام" || p == "تقي");
    }

public:
    static std::string translate(const std::string& fullName, const std::string& data_path = "") {
        if (fullName.empty()) return "";

        std::stringstream ss(fullName);
        std::string tok;
        std::vector<std::string> tokens;
        while (ss >> tok) {
            tokens.push_back(tok);
        }

        bool is_ar = LookupIndices::is_arabic(fullName);
        std::vector<std::string> result;

        for (size_t i = 0; i < tokens.size(); ++i) {
            std::string current = tokens[i];

            if (is_ar) {
                // Check compound if there is a next token
                if (i + 1 < tokens.size() && is_compound_prefix(current)) {
                    std::string next = tokens[i + 1];
                    std::string compound = current + " " + next;
                    std::string compound_no_space = current + next;

                    auto entry = LookupIndices::lookup_ar(compound, data_path);
                    if (!entry.has_value()) {
                        entry = LookupIndices::lookup_ar(compound_no_space, data_path);
                    }
                    if (entry.has_value() && !entry->en.empty()) {
                        result.push_back(entry->en);
                        i++;
                        continue;
                    }
                }

                auto entry = LookupIndices::lookup_ar(current, data_path);
                result.push_back(entry.has_value() && !entry->en.empty() ? entry->en : current);
            } else {
                auto entry = LookupIndices::lookup_en(current, data_path);
                result.push_back(entry.has_value() && !entry->ar.empty() ? entry->ar : current);
            }
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
