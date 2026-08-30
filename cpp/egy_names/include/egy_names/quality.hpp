#pragma once

// Personal-name quality gate.
//
// The book keeps some surface tokens so split and compounds still resolve.
// Those tokens are not a person's name. Production APIs must not treat
// them as one. Mirrors python/src/egy_names/_quality.py.

#include "types.hpp"
#include "rules_config.hpp"
#include "lookup_indices.hpp"
#include <optional>
#include <sstream>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

namespace egy_names {

inline const std::unordered_set<std::string>& non_personal_ar_set(const std::string& data_path = "") {
    static std::unordered_set<std::string> cached;
    static bool loaded = false;
    if (!loaded) {
        cached = RulesConfig::non_personal_ar(data_path);
        loaded = true;
    }
    return cached;
}

// True if this lemma may stand as a person's name.
inline bool is_personal_entry(const NameEntry& entry, const std::string& data_path = "") {
    const auto& non_personal = non_personal_ar_set(data_path);
    return non_personal.find(entry.ar) == non_personal.end();
}

// True if a multi-word lemma's first half is not a real name.
//
// A well-formed two-word lemma is either a kunya ("أبو" + element) or a
// name plus a compound. What is left after spacing fixes are corrupted
// rows: truncated fragments, doubled-letter typos, three-name chains
// glued into two words. Their first half resolves to nothing, and they
// all sit at the corpus noise floor.
inline bool is_malformed_compound(const NameEntry& entry, const std::string& data_path = "") {
    std::string ar = entry.ar;
    size_t first = ar.find_first_not_of(" \t\n\r");
    size_t last = ar.find_last_not_of(" \t\n\r");
    ar = (first == std::string::npos) ? "" : ar.substr(first, last - first + 1);

    if (ar.find(' ') == std::string::npos) return false;
    if (entry.corpus_share > RulesConfig::low_confidence_share_epsilon(data_path)) return false;

    std::string first_word = ar.substr(0, ar.find(' '));

    const auto& exempt = RulesConfig::kunya_exempt_prefixes(data_path);
    for (const auto& p : exempt) {
        if (first_word == p) return false;
    }

    return !LookupIndices::lookup_ar(first_word, data_path).has_value();
}

// True if this lemma is likely a fabricated/unverified filler row.
//
// Zero real-world corpus share on its own just means "rare". But zero
// share combined with the catalog's own gloss admitting the name's
// meaning or origin is unclear is a strong signal the row was never
// attested, only guessed to fill out a role/pattern.
inline bool is_low_confidence_entry(const NameEntry& entry, const std::string& data_path = "") {
    if (is_malformed_compound(entry, data_path)) return true;
    if (entry.corpus_share > RulesConfig::low_confidence_share_epsilon(data_path)) return false;

    const std::string& meaning = entry.meaning_ar;
    for (const auto& marker : RulesConfig::uncertain_meaning_markers(data_path)) {
        if (!marker.empty() && meaning.find(marker) != std::string::npos) return true;
    }
    return false;
}

// True if generate may emit this lemma as one token.
inline bool is_generatable_entry(const NameEntry& entry, const std::string& data_path = "") {
    return is_personal_entry(entry, data_path)
        && !is_low_confidence_entry(entry, data_path)
        && entry.ar.find(' ') == std::string::npos;
}

// Family and tribal tokens are lineage, not the person.
inline bool is_lineage_role(const NameEntry& entry) {
    return entry.role == NameRole::FAMILY || entry.role == NameRole::TRIBAL;
}

// Split on whitespace, but merge an adjacent pair into one lemma when the
// book has it as a two-word compound (e.g. kunya "Abu X"). Greedy pairwise
// lookahead, mirroring _compound_tokens in the Python SDK.
inline std::vector<std::pair<std::string, std::optional<NameEntry>>> compound_tokens(
    const std::string& full_name, const std::string& data_path = "") {
    std::vector<std::pair<std::string, std::optional<NameEntry>>> out;

    std::vector<std::string> raw;
    {
        std::istringstream ss(full_name);
        std::string tok;
        while (ss >> tok) raw.push_back(tok);
    }

    size_t i = 0;
    size_t n = raw.size();
    while (i < n) {
        if (i + 1 < n) {
            std::string pair = raw[i] + " " + raw[i + 1];
            auto pair_entry = LookupIndices::lookup_ar(pair, data_path);
            if (!pair_entry.has_value()) {
                pair_entry = LookupIndices::lookup_ar(raw[i] + raw[i + 1], data_path);
            }
            if (pair_entry.has_value()) {
                out.emplace_back(pair, pair_entry);
                i += 2;
                continue;
            }
        }
        out.emplace_back(raw[i], LookupIndices::lookup(raw[i], data_path));
        i += 1;
    }
    return out;
}

}  // namespace egy_names
