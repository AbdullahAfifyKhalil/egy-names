#pragma once

#include "types.hpp"
#include "data_loader.hpp"
#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>
#include <mutex>
#include <cstdint>

namespace egy_names {

class LookupIndices {
private:
    static inline std::unordered_map<std::string, NameEntry> _ar_index;
    static inline std::unordered_map<std::string, NameEntry> _en_index;
    static inline std::unordered_map<std::string, NameEntry> _ar_norm_index;
    static inline std::unordered_map<std::string, std::string> _correction_index;
    static inline std::vector<NameEntry> _all_entries;
    static inline std::vector<NameEntry> _ranked_entries;
    static inline nlohmann::json _metadata;
    static inline bool _built = false;
    static inline std::mutex _index_mutex;

public:
    static std::string normalize_ar(const std::string& text) {
        if (text.empty()) return "";
        std::string result;
        result.reserve(text.size());

        size_t i = 0;
        while (i < text.size()) {
            unsigned char c1 = static_cast<unsigned char>(text[i]);

            // 1-byte ASCII
            if (c1 < 0x80) {
                result.push_back(c1);
                i++;
                continue;
            }

            // 2-byte UTF-8 sequence (Arabic is 0xD8..0xDB)
            if (c1 >= 0xD8 && c1 <= 0xDF && i + 1 < text.size()) {
                unsigned char c2 = static_cast<unsigned char>(text[i + 1]);
                uint32_t cp = ((c1 & 0x1F) << 6) | (c2 & 0x3F);

                // Strip Tashkeel & Diacritics
                if ((cp >= 0x064B && cp <= 0x065F) || cp == 0x0670 || (cp >= 0x0610 && cp <= 0x061A) || (cp >= 0x06D6 && cp <= 0x06ED)) {
                    i += 2;
                    continue;
                }

                // Strip Tatweel (0x0640)
                if (cp == 0x0640) {
                    i += 2;
                    continue;
                }

                // Normalize Alef variants (آ 0x0622, أ 0x0623, إ 0x0625, ٱ 0x0671 -> ا 0x0627)
                if (cp == 0x0622 || cp == 0x0623 || cp == 0x0625 || cp == 0x0671) {
                    result.push_back('\xD8');
                    result.push_back('\xA7'); // ا
                    i += 2;
                    continue;
                }

                // Alef Maqsura (ى 0x0649 -> ي 0x064A)
                if (cp == 0x0649) {
                    result.push_back('\xD9');
                    result.push_back('\x8A'); // ي
                    i += 2;
                    continue;
                }

                // Ta Marbuta (ة 0x0629 -> ه 0x0647)
                if (cp == 0x0629) {
                    result.push_back('\xD9');
                    result.push_back('\x87'); // ه
                    i += 2;
                    continue;
                }

                // Keep unchanged 2-byte char
                result.push_back(text[i]);
                result.push_back(text[i + 1]);
                i += 2;
                continue;
            }

            // 3-byte or 4-byte UTF-8
            if ((c1 & 0xF0) == 0xE0 && i + 2 < text.size()) {
                result.append(text.substr(i, 3));
                i += 3;
            } else if ((c1 & 0xF8) == 0xF0 && i + 3 < text.size()) {
                result.append(text.substr(i, 4));
                i += 4;
            } else {
                result.push_back(c1);
                i++;
            }
        }
        return result;
    }

    static std::string normalize_en(const std::string& text) {
        std::string s = text;
        std::transform(s.begin(), s.end(), s.begin(), [](unsigned char c) {
            return std::tolower(c);
        });
        // trim whitespace
        size_t first = s.find_first_not_of(" \t\n\r");
        if (first == std::string::npos) return "";
        size_t last = s.find_last_not_of(" \t\n\r");
        return s.substr(first, (last - first + 1));
    }

    static bool is_arabic(const std::string& text) {
        for (size_t i = 0; i < text.size(); ++i) {
            unsigned char c = static_cast<unsigned char>(text[i]);
            if (c >= 0xD8 && c <= 0xDB) return true; // UTF-8 prefix for Arabic block 0600-06FF
        }
        return false;
    }

    static void ensure_built(const std::string& custom_path = "") {
        if (_built) return;
        std::lock_guard<std::mutex> lock(_index_mutex);
        if (_built) return;

        DataBundle bundle = DataLoader::load_bundle(custom_path);
        _all_entries = bundle.names;
        _metadata = bundle.metadata;

        auto claim_en = [](const std::string& key, const NameEntry& e) {
            auto it = _en_index.find(key);
            if (it == _en_index.end() || e.corpus_share > it->second.corpus_share) {
                _en_index[key] = e;
            }
        };

        // A canonical key (some entry's own ar / normalized-ar) always wins
        // over any OTHER entry's variant claiming the same string — a rare
        // misspelling must never shadow a real lemma's own canonical
        // spelling. Among two variants with no canonical claim, the higher
        // corpus share wins, exactly like claim_en.
        std::unordered_set<std::string> canonical_ar_keys;
        std::unordered_set<std::string> canonical_ar_norm_keys;
        for (const auto& entry : _all_entries) {
            canonical_ar_keys.insert(entry.ar);
            canonical_ar_norm_keys.insert(normalize_ar(entry.ar));
        }

        auto claim_ar_variant = [](std::unordered_map<std::string, NameEntry>& index,
                                    const std::unordered_set<std::string>& canonical_keys,
                                    const std::string& key,
                                    const NameEntry& e) {
            if (canonical_keys.find(key) != canonical_keys.end()) {
                return;
            }
            auto it = index.find(key);
            if (it == index.end() || e.corpus_share > it->second.corpus_share) {
                index[key] = e;
            }
        };

        // Pass 1: canonical spellings are unconditional and take priority
        // over any other lemma's variant claiming the same string.
        for (const auto& entry : _all_entries) {
            _ar_index[entry.ar] = entry;
            _ar_norm_index[normalize_ar(entry.ar)] = entry;
        }

        // Pass 2: variants (AR + EN).
        for (const auto& entry : _all_entries) {
            for (const auto& v : entry.ar_variants) {
                std::string v_stripped = v;
                size_t first = v_stripped.find_first_not_of(" \t\n\r");
                if (first == std::string::npos) continue;
                size_t last = v_stripped.find_last_not_of(" \t\n\r");
                v_stripped = v_stripped.substr(first, last - first + 1);
                if (v_stripped.empty()) continue;
                claim_ar_variant(_ar_index, canonical_ar_keys, v_stripped, entry);
                claim_ar_variant(_ar_norm_index, canonical_ar_norm_keys, normalize_ar(v_stripped), entry);
            }

            // EN Index — keep the higher-share lemma on a colliding key
            claim_en(normalize_en(entry.en), entry);
            for (const auto& v : entry.en_variants) {
                if (!v.empty()) {
                    claim_en(normalize_en(v), entry);
                }
            }
        }

        _correction_index = bundle.corrections;

        _ranked_entries = _all_entries;
        std::sort(_ranked_entries.begin(), _ranked_entries.end(), [](const NameEntry& a, const NameEntry& b) {
            return a.corpus_share > b.corpus_share;
        });

        _built = true;
    }

    static std::optional<NameEntry> lookup_ar(const std::string& name, const std::string& data_path = "") {
        ensure_built(data_path);
        if (name.empty()) return std::nullopt;

        // Trim
        std::string trimmed = name;
        size_t first = trimmed.find_first_not_of(" \t\n\r");
        if (first == std::string::npos) return std::nullopt;
        size_t last = trimmed.find_last_not_of(" \t\n\r");
        trimmed = trimmed.substr(first, (last - first + 1));

        // 1. Direct match
        auto it = _ar_index.find(trimmed);
        if (it != _ar_index.end()) return it->second;

        // 2. Normalized match
        std::string norm = normalize_ar(trimmed);
        auto it_norm = _ar_norm_index.find(norm);
        if (it_norm != _ar_norm_index.end()) return it_norm->second;

        // 3. Alif / Alif Maqsura terminal phonetic equivalence
        static const std::string alif_utf8 = "\xD8\xA7"; // ا
        static const std::string ya_utf8 = "\xD9\x8A";   // ي

        if (norm.size() >= alif_utf8.size() && norm.compare(norm.size() - alif_utf8.size(), alif_utf8.size(), alif_utf8) == 0) {
            std::string alt = norm.substr(0, norm.size() - alif_utf8.size()) + ya_utf8;
            auto it_alt = _ar_norm_index.find(alt);
            if (it_alt != _ar_norm_index.end()) return it_alt->second;
        } else if (norm.size() >= ya_utf8.size() && norm.compare(norm.size() - ya_utf8.size(), ya_utf8.size(), ya_utf8) == 0) {
            std::string alt = norm.substr(0, norm.size() - ya_utf8.size()) + alif_utf8;
            auto it_alt = _ar_norm_index.find(alt);
            if (it_alt != _ar_norm_index.end()) return it_alt->second;
        }

        // 4. Space-less compound match
        std::string no_space = trimmed;
        no_space.erase(std::remove_if(no_space.begin(), no_space.end(), ::isspace), no_space.end());
        if (no_space != trimmed) {
            auto it_ns = _ar_index.find(no_space);
            if (it_ns != _ar_index.end()) return it_ns->second;
            auto it_ns_norm = _ar_norm_index.find(normalize_ar(no_space));
            if (it_ns_norm != _ar_norm_index.end()) return it_ns_norm->second;
        }

        return std::nullopt;
    }

    static std::optional<NameEntry> lookup_en(const std::string& name, const std::string& data_path = "") {
        ensure_built(data_path);
        auto it = _en_index.find(normalize_en(name));
        if (it != _en_index.end()) return it->second;
        return std::nullopt;
    }

    static std::optional<NameEntry> lookup(const std::string& name, const std::string& data_path = "") {
        ensure_built(data_path);
        if (is_arabic(name)) {
            return lookup_ar(name, data_path);
        }
        return lookup_en(name, data_path);
    }

    static std::optional<std::string> get_correction(const std::string& surface, const std::string& data_path = "") {
        ensure_built(data_path);
        auto it = _correction_index.find(surface);
        if (it != _correction_index.end()) return it->second;
        return std::nullopt;
    }

    static const std::vector<NameEntry>& get_all(const std::string& data_path = "") {
        ensure_built(data_path);
        return _all_entries;
    }

    static const std::vector<NameEntry>& get_ranked(const std::string& data_path = "") {
        ensure_built(data_path);
        return _ranked_entries;
    }

    static const std::unordered_map<std::string, NameEntry>& get_ar_forms(const std::string& data_path = "") {
        ensure_built(data_path);
        return _ar_index;
    }

    static const std::unordered_map<std::string, NameEntry>& get_ar_norm_forms(const std::string& data_path = "") {
        ensure_built(data_path);
        return _ar_norm_index;
    }

    static const nlohmann::json& get_metadata(const std::string& data_path = "") {
        ensure_built(data_path);
        return _metadata;
    }
};

} // namespace egy_names
