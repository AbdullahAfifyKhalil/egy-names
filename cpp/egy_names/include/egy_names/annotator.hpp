#pragma once

#include "types.hpp"
#include "lookup_indices.hpp"
#include <string>
#include <vector>
#include <sstream>

namespace egy_names {

class Annotator {
public:
    static std::optional<NameInfo> annotate_single(const std::string& name, const std::string& data_path = "") {
        auto entry = LookupIndices::lookup(name, data_path);
        if (!entry.has_value()) return std::nullopt;
        return to_name_info(*entry);
    }

    static std::vector<NameInfo> annotate(const std::string& fullName, const std::string& data_path = "") {
        std::stringstream ss(fullName);
        std::string tok;
        std::vector<std::string> tokens;
        while (ss >> tok) {
            tokens.push_back(tok);
        }

        std::vector<NameInfo> results;
        for (const auto& t : tokens) {
            auto info = annotate_single(t, data_path);
            if (info.has_value()) {
                results.push_back(*info);
            }
        }
        return results;
    }
};

} // namespace egy_names
