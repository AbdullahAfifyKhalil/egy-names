#pragma once

#include "types.hpp"
#include "lookup_indices.hpp"
#include <random>
#include <vector>
#include <algorithm>
#include <string>
#include <unordered_set>

namespace egy_names {

class Generator {
public:
    static std::vector<GeneratedName> generate(
        int count = 5,
        int length = 3,
        const std::string& gender = "",
        const std::string& religion = "",
        int seed = -1,
        const std::string& data_path = "")
    {
        LookupIndices::ensure_built(data_path);
        const auto& all_entries = LookupIndices::get_all(data_path);

        std::mt19937 rng;
        if (seed >= 0) {
            rng.seed(static_cast<unsigned int>(seed));
        } else {
            std::random_device rd;
            rng.seed(rd());
        }

        Gender target_gender = string_to_gender(gender);
        Religion target_religion = string_to_religion(religion);

        // Pre-filter slot candidates
        std::vector<std::vector<NameEntry>> slot_candidates(5);
        std::vector<std::vector<double>> slot_weights(5);

        for (int slot = 0; slot < 5; ++slot) {
            for (const auto& entry : all_entries) {
                if (slot == 0) {
                    if (!gender.empty() && entry.gender != target_gender && entry.gender != Gender::NEUTRAL) {
                        continue;
                    }
                } else {
                    // Subsequent slots in Egyptian culture are male patronymics or family names
                    if (entry.gender != Gender::MALE && entry.gender != Gender::NEUTRAL && entry.role != NameRole::FAMILY) {
                        continue;
                    }
                }

                if (!religion.empty() && entry.religion != target_religion && entry.religion != Religion::NEUTRAL) {
                    continue;
                }

                double weight = entry.corpus_share;
                if (slot < static_cast<int>(entry.slot_pcts.size())) {
                    weight *= (entry.slot_pcts[slot] / 100.0);
                }

                if (weight > 0.0) {
                    slot_candidates[slot].push_back(entry);
                    slot_weights[slot].push_back(weight);
                }
            }
        }

        // Fallback for empty slots
        for (int slot = 0; slot < 5; ++slot) {
            if (slot_candidates[slot].empty()) {
                for (const auto& entry : all_entries) {
                    if (slot == 0 && !gender.empty() && entry.gender != target_gender) continue;
                    slot_candidates[slot].push_back(entry);
                    slot_weights[slot].push_back(entry.corpus_share);
                }
            }
        }

        std::vector<GeneratedName> generated;
        for (int c = 0; c < count; ++c) {
            std::vector<std::string> parts_ar;
            std::vector<std::string> parts_en;
            std::unordered_set<std::string> seen_ar;

            for (int s = 0; s < length; ++s) {
                int slot_idx = std::min(s, 4);
                if (slot_candidates[slot_idx].empty()) continue;

                std::discrete_distribution<size_t> dist(slot_weights[slot_idx].begin(), slot_weights[slot_idx].end());
                
                NameEntry selected;
                int attempts = 0;
                do {
                    size_t idx = dist(rng);
                    selected = slot_candidates[slot_idx][idx];
                    attempts++;
                } while (seen_ar.count(selected.ar) > 0 && attempts < 10);

                seen_ar.insert(selected.ar);
                parts_ar.push_back(selected.ar);
                parts_en.push_back(selected.en);
            }

            GeneratedName gn;
            gn.parts_ar = parts_ar;
            gn.parts_en = parts_en;

            std::string full_ar, full_en;
            for (size_t i = 0; i < parts_ar.size(); ++i) {
                if (i > 0) { full_ar += " "; full_en += " "; }
                full_ar += parts_ar[i];
                full_en += parts_en[i];
            }
            gn.ar = full_ar;
            gn.en = full_en;

            generated.push_back(gn);
        }

        return generated;
    }
};

} // namespace egy_names
