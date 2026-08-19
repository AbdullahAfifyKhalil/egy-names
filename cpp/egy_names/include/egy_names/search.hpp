#pragma once

#include "types.hpp"
#include "lookup_indices.hpp"
#include <string>
#include <vector>
#include <algorithm>

namespace egy_names {

class SearchEngine {
public:
    static std::vector<NameInfo> search(
        std::optional<Gender> gender = std::nullopt,
        std::optional<Religion> religion = std::nullopt,
        std::optional<NameRole> role = std::nullopt,
        std::optional<FrequencyClass> frequency = std::nullopt,
        const std::string& starts_with = "",
        const std::string& ends_with = "",
        const std::string& contains = "",
        double min_corpus_share = 0.0,
        int max_results = 50,
        const std::string& sort_by = "corpus_share",
        const std::string& data_path = "")
    {
        LookupIndices::ensure_built(data_path);
        const auto& all_entries = LookupIndices::get_all(data_path);

        std::vector<NameEntry> matched;
        for (const auto& e : all_entries) {
            if (gender.has_value() && e.gender != *gender) continue;
            if (religion.has_value() && e.religion != *religion) continue;
            if (role.has_value() && e.role != *role) continue;
            if (frequency.has_value() && e.frequency != *frequency) continue;
            if (e.corpus_share < min_corpus_share) continue;

            if (!starts_with.empty()) {
                if (e.ar.rfind(starts_with, 0) != 0 && e.en.rfind(starts_with, 0) != 0) continue;
            }

            if (!ends_with.empty()) {
                bool ends_ar = e.ar.size() >= ends_with.size() && e.ar.compare(e.ar.size() - ends_with.size(), ends_with.size(), ends_with) == 0;
                bool ends_en = e.en.size() >= ends_with.size() && e.en.compare(e.en.size() - ends_with.size(), ends_with.size(), ends_with) == 0;
                if (!ends_ar && !ends_en) continue;
            }

            if (!contains.empty()) {
                if (e.ar.find(contains) == std::string::npos && e.en.find(contains) == std::string::npos) continue;
            }

            matched.push_back(e);
        }

        if (sort_by == "corpus_share") {
            std::sort(matched.begin(), matched.end(), [](const NameEntry& a, const NameEntry& b) {
                return a.corpus_share > b.corpus_share;
            });
        }

        if (max_results > 0 && matched.size() > static_cast<size_t>(max_results)) {
            matched.resize(max_results);
        }

        std::vector<NameInfo> results;
        results.reserve(matched.size());
        for (const auto& e : matched) {
            results.push_back(to_name_info(e));
        }

        return results;
    }
};

} // namespace egy_names
