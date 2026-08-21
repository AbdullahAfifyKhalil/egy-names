#pragma once

#include "types.hpp"
#include <nlohmann/json.hpp>
#include <zlib.h>
#include <fstream>
#include <sstream>
#include <iostream>
#include <filesystem>
#include <mutex>

namespace egy_names {

struct DataBundle {
    std::vector<NameEntry> names;
    std::unordered_map<std::string, std::string> corrections;
    nlohmann::json metadata;
};

class DataLoader {
public:
    static std::string decompress_gzip(const std::string& gzip_path) {
        gzFile file = gzopen(gzip_path.c_str(), "rb");
        if (!file) {
            return "";
        }

        std::string decompressed;
        char buffer[65536];
        int bytes_read = 0;

        while ((bytes_read = gzread(file, buffer, sizeof(buffer))) > 0) {
            decompressed.append(buffer, bytes_read);
        }

        gzclose(file);
        return decompressed;
    }

    static std::string resolve_data_path(const std::string& custom_path = "") {
        if (!custom_path.empty() && std::filesystem::exists(custom_path)) {
            return custom_path;
        }

        std::vector<std::string> search_paths = {
            "data/names.json.gz",
            "../data/names.json.gz",
            "../../data/names.json.gz",
            "/Volumes/MAC/Development/Personal/Egyptian Names/library building/data/names.json.gz",
            "/Volumes/MAC/Development/Personal/Egyptian Names/library building/cpp/egy_names/data/names.json.gz"
        };

        for (const auto& p : search_paths) {
            if (std::filesystem::exists(p)) {
                return p;
            }
        }

        return "data/names.json.gz";
    }

    static DataBundle load_bundle(const std::string& custom_path = "") {
        static DataBundle cached_bundle;
        static bool is_cached = false;
        static std::mutex load_mutex;

        std::lock_guard<std::mutex> lock(load_mutex);
        if (is_cached && custom_path.empty()) {
            return cached_bundle;
        }

        std::string path = resolve_data_path(custom_path);
        std::string json_str = decompress_gzip(path);
        if (json_str.empty()) {
            std::cerr << "[egy_names] Warning: Could not load or decompress " << path << std::endl;
            return cached_bundle;
        }

        auto j = nlohmann::json::parse(json_str, nullptr, false);
        if (j.is_discarded()) {
            std::cerr << "[egy_names] Error: Invalid JSON in " << path << std::endl;
            return cached_bundle;
        }

        DataBundle bundle;
        if (j.contains("metadata")) {
            bundle.metadata = j["metadata"];
        }

        if (j.contains("names") && j["names"].is_array()) {
            for (const auto& item : j["names"]) {
                NameEntry e;
                e.ar = item.value("a", "");
                e.en = item.value("e", "");
                e.gender = string_to_gender(item.value("g", "n"));
                e.religion = string_to_religion(item.value("r", "n"));
                e.role = string_to_role(item.value("l", "g"));
                
                std::string av = item.value("av", "");
                if (!av.empty()) {
                    std::stringstream ss(av);
                    std::string segment;
                    while (std::getline(ss, segment, '|')) {
                        e.ar_variants.push_back(segment);
                    }
                } else {
                    e.ar_variants.push_back(e.ar);
                }

                std::string ev = item.value("ev", "");
                if (!ev.empty()) {
                    std::stringstream ss(ev);
                    std::string segment;
                    while (std::getline(ss, segment, '|')) {
                        e.en_variants.push_back(segment);
                    }
                } else {
                    e.en_variants.push_back(e.en);
                }

                if (item.contains("p") && item["p"].is_array()) {
                    for (const auto& p_val : item["p"]) {
                        e.slot_pcts.push_back(p_val.get<double>());
                    }
                }

                e.corpus_share = item.value("tp", 0.0);
                e.frequency = string_to_freq(item.value("fc", "n"));
                e.tashkeel = item.value("t", e.ar);
                e.tashkeel_standard = item.value("t", e.ar);
                e.tashkeel_eg = item.value("te", e.tashkeel_standard);
                e.ipa_standard = item.value("is", "");
                e.ipa_eg = item.value("ie", "");
                e.meaning_ar = item.value("ma", "");
                e.meaning_en = item.value("me", "");
                e.root = item.value("rt", "N/A");
                e.origin_type = item.value("ot", "arabic_classical");
                e.trend_category = item.value("tc", "classic_timeless");

                auto split_pipe = [](const std::string& str) -> std::vector<std::string> {
                    std::vector<std::string> res;
                    if (str.empty()) return res;
                    std::stringstream ss(str);
                    std::string segment;
                    while (std::getline(ss, segment, '|')) {
                        if (!segment.empty()) res.push_back(segment);
                    }
                    return res;
                };

                std::string dla = item.value("dla", item.value("dl", ""));
                e.dallaa_ar = split_pipe(dla);
                e.dallaa = e.dallaa_ar;
                e.dallaa_tashkeel = split_pipe(item.value("dlt", ""));
                e.dallaa_en = split_pipe(item.value("dle", ""));
                e.dallaa_ipa = split_pipe(item.value("dli", ""));

                std::string ffa = item.value("ffa", item.value("ff", ""));
                e.famous_figures_ar = split_pipe(ffa);
                e.famous_figures = e.famous_figures_ar;
                e.famous_figures_en = split_pipe(item.value("ffe", ""));

                bundle.names.push_back(e);
            }
        }

        if (j.contains("corrections") && j["corrections"].is_object()) {
            for (auto it = j["corrections"].begin(); it != j["corrections"].end(); ++it) {
                bundle.corrections[it.key()] = it.value().get<std::string>();
            }
        }

        if (custom_path.empty()) {
            cached_bundle = bundle;
            is_cached = true;
        }

        return bundle;
    }
};

} // namespace egy_names
