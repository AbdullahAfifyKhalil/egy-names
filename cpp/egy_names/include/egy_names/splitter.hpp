#pragma once

#include "types.hpp"
#include "lookup_indices.hpp"
#include <string>
#include <vector>
#include <cmath>
#include <algorithm>
#include <sstream>

namespace egy_names {

class Splitter {
public:
    static constexpr double BASE_SEGMENT_COST = 1.0;
    static constexpr double UNKNOWN_PENALTY = 8.0;
    static constexpr double LENGTH_BONUS_PER_CHAR = -0.05;

    static double get_freq_bonus(FrequencyClass fc) {
        switch (fc) {
            case FrequencyClass::COMMON: return -0.6;
            case FrequencyClass::NORMAL: return -0.2;
            default: return 0.0;
        }
    }

    static std::vector<std::string> dp_segment(const std::string& text, const std::string& data_path = "") {
        LookupIndices::ensure_built(data_path);
        const auto& ar_index = LookupIndices::get_ar_forms(data_path);
        const auto& ar_norm = LookupIndices::get_ar_norm_forms(data_path);

        // Convert UTF-8 to codepoints or byte-based substrings
        int n = static_cast<int>(text.length());
        std::vector<double> dp_cost(n + 1, std::numeric_limits<double>::infinity());
        std::vector<int> dp_prev(n + 1, -1);

        dp_cost[0] = 0.0;
        dp_prev[0] = 0;

        for (int i = 1; i <= n; ++i) {
            int start_j = (i > 45) ? (i - 45) : 0;
            for (int j = start_j; j < i; ++j) {
                if (dp_cost[j] == std::numeric_limits<double>::infinity()) continue;

                std::string substr = text.substr(j, i - j);
                if (substr.length() < 2 && j > 0) continue;

                auto it = ar_index.find(substr);
                if (it == ar_index.end()) {
                    it = ar_norm.find(LookupIndices::normalize_ar(substr));
                }

                if (it != ar_index.end() && it != ar_norm.end()) {
                    double cost = dp_cost[j] + BASE_SEGMENT_COST + get_freq_bonus(it->second.frequency) + LENGTH_BONUS_PER_CHAR * substr.length();
                    if (cost < dp_cost[i]) {
                        dp_cost[i] = cost;
                        dp_prev[i] = j;
                    }
                } else {
                    double cost = dp_cost[j] + UNKNOWN_PENALTY + substr.length();
                    if (cost < dp_cost[i]) {
                        dp_cost[i] = cost;
                        dp_prev[i] = j;
                    }
                }
            }
        }

        if (dp_cost[n] == std::numeric_limits<double>::infinity()) {
            return {text};
        }

        std::vector<std::string> segments;
        int pos = n;
        while (pos > 0) {
            int prev = dp_prev[pos];
            if (prev < 0) break;
            segments.push_back(text.substr(prev, pos - prev));
            pos = prev;
        }

        std::reverse(segments.begin(), segments.end());
        return segments;
    }

    static std::vector<std::string> split(const std::string& fullName, const std::string& data_path = "") {
        if (fullName.empty()) return {};

        std::stringstream ss(fullName);
        std::string tok;
        std::vector<std::string> tokens;
        while (ss >> tok) {
            tokens.push_back(tok);
        }

        if (tokens.size() > 1) {
            return tokens;
        }

        if (LookupIndices::is_arabic(fullName)) {
            auto entry = LookupIndices::lookup(fullName, data_path);
            if (entry.has_value()) {
                return {fullName};
            }
            return dp_segment(fullName, data_path);
        }

        return {fullName};
    }
};

} // namespace egy_names
