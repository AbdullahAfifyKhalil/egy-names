#pragma once

// Loader for the shared, cross-SDK rule config (data/logic_config.json).
//
// Mirrors python/src/egy_names/_rules_config.py: a single source of truth
// for thresholds and rule lists that used to be hardcoded per language.
// If the config file is missing or malformed, falls back to the values
// last known correct, so the library never hard-fails on a packaging
// mistake.

#include "paths.hpp"
#include <nlohmann/json.hpp>
#include <filesystem>
#include <fstream>
#include <mutex>
#include <sstream>
#include <string>
#include <unordered_set>
#include <vector>

namespace egy_names {

struct InferRule {
    nlohmann::json raw;
};

class RulesConfig {
private:
    static inline nlohmann::json _config;
    static inline bool _loaded = false;
    static inline std::mutex _mutex;

    static nlohmann::json fallback() {
        nlohmann::json j;
        j["quality"]["non_personal_ar"] = {
            "الله", "الرجل", "الرجال", "شربه", "لافندي", "لفندي", "ماء", "البيت"
        };
        j["quality"]["uncertain_meaning_markers"] = {
            "غير واضح", "لا يوجد معنى", "غير معروف",
            "قد يكون تحريف", "تحريفاً", "تحريفًا"
        };
        j["quality"]["low_confidence_share_epsilon"] = 0.0001;
        j["quality"]["kunya_exempt_prefixes"] = {"أبو", "ابو", "أم", "ام"};
        j["infer_thresholds"]["gender_min_p"] = 0.70;
        j["infer_thresholds"]["muslim_min_p"] = 0.85;
        j["infer_thresholds"]["christian_min_p"] = 0.90;
        j["infer_thresholds"]["role_min_p"] = 0.88;
        j["infer_rules"]["gender"] = nlohmann::json::array();
        j["infer_rules"]["religion"] = nlohmann::json::array();
        j["infer_rules"]["role"] = nlohmann::json::array();
        return j;
    }

    static std::string resolve_config_path(const std::string& data_dir_hint) {
        return resolve_data_file("logic_config.json", data_dir_hint);
    }

public:
    // data_path mirrors the names.json.gz custom_path so logic_config.json
    // is looked up in the same directory as the names bundle.
    static void ensure_loaded(const std::string& data_path = "") {
        if (_loaded) return;
        std::lock_guard<std::mutex> lock(_mutex);
        if (_loaded) return;

        std::string path = resolve_config_path(data_path);
        std::ifstream f(path);
        if (!f.is_open()) {
            _config = fallback();
            _loaded = true;
            return;
        }

        std::stringstream buf;
        buf << f.rdbuf();
        auto j = nlohmann::json::parse(buf.str(), nullptr, false);
        if (j.is_discarded()) {
            _config = fallback();
        } else {
            _config = j;
        }
        _loaded = true;
    }

    static std::unordered_set<std::string> non_personal_ar(const std::string& data_path = "") {
        ensure_loaded(data_path);
        std::unordered_set<std::string> out;
        auto arr = _config.value("quality", nlohmann::json::object()).value("non_personal_ar", nlohmann::json::array());
        for (const auto& v : arr) out.insert(v.get<std::string>());
        return out;
    }

    static std::vector<std::string> uncertain_meaning_markers(const std::string& data_path = "") {
        ensure_loaded(data_path);
        std::vector<std::string> out;
        auto arr = _config.value("quality", nlohmann::json::object()).value("uncertain_meaning_markers", nlohmann::json::array());
        for (const auto& v : arr) out.push_back(v.get<std::string>());
        return out;
    }

    static double low_confidence_share_epsilon(const std::string& data_path = "") {
        ensure_loaded(data_path);
        return _config.value("quality", nlohmann::json::object()).value("low_confidence_share_epsilon", 0.0001);
    }

    static std::vector<std::string> kunya_exempt_prefixes(const std::string& data_path = "") {
        ensure_loaded(data_path);
        std::vector<std::string> out;
        auto arr = _config.value("quality", nlohmann::json::object()).value("kunya_exempt_prefixes", nlohmann::json::array());
        for (const auto& v : arr) out.push_back(v.get<std::string>());
        return out;
    }

    static nlohmann::json infer_thresholds(const std::string& data_path = "") {
        ensure_loaded(data_path);
        return _config.value("infer_thresholds", fallback()["infer_thresholds"]);
    }

    // Rule table for 'gender' | 'religion' | 'role'. Not consumed by the
    // C++ SDK yet (ML fallback / inference is out of scope for this port);
    // loaded for forward compatibility.
    static nlohmann::json infer_rules(const std::string& kind, const std::string& data_path = "") {
        ensure_loaded(data_path);
        return _config.value("infer_rules", nlohmann::json::object()).value(kind, nlohmann::json::array());
    }
};

} // namespace egy_names
