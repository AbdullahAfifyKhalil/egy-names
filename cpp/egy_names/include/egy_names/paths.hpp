#pragma once

#include <cstdlib>
#include <filesystem>
#include <string>
#include <vector>

namespace egy_names {

// Locate names.json.gz / logic_config.json from the cloned tree, an
// env override, or a CMake compile definition — not from cwd alone.
// A FetchContent consumer that runs from another directory still loads
// the book.

inline bool path_is_file(const std::filesystem::path& p) {
    std::error_code ec;
    return std::filesystem::is_regular_file(p, ec);
}

inline void add_file_candidate(std::vector<std::filesystem::path>& out, std::filesystem::path p) {
    if (!p.empty()) {
        out.push_back(std::move(p));
    }
}

inline void add_dir_file(std::vector<std::filesystem::path>& out, const std::filesystem::path& dir, const std::string& filename) {
    if (!dir.empty()) {
        out.push_back(dir / filename);
    }
}

inline std::vector<std::filesystem::path> data_file_candidates(const std::string& filename, const std::string& hint) {
    std::vector<std::filesystem::path> out;

    if (!hint.empty()) {
        std::filesystem::path h(hint);
        add_file_candidate(out, h);
        add_dir_file(out, h, filename);
        add_dir_file(out, h.parent_path(), filename);
    }

    if (const char* env = std::getenv("EGY_NAMES_DATA")) {
        std::filesystem::path e(env);
        add_file_candidate(out, e);
        add_dir_file(out, e, filename);
        add_dir_file(out, e.parent_path(), filename);
    }

#ifdef EGY_NAMES_DATA_DIR
    add_dir_file(out, std::filesystem::path(EGY_NAMES_DATA_DIR), filename);
#endif

    // This header lives at cpp/egy_names/include/egy_names/paths.hpp
    const std::filesystem::path hdr = std::filesystem::path(__FILE__).parent_path();
    add_dir_file(out, hdr / ".." / ".." / "data", filename);                 // cpp/egy_names/data
    add_dir_file(out, hdr / ".." / ".." / ".." / ".." / "data", filename);   // repo data/

    try {
        auto dir = std::filesystem::current_path();
        for (int i = 0; i < 8; ++i) {
            add_dir_file(out, dir / "data", filename);
            add_dir_file(out, dir / "cpp" / "egy_names" / "data", filename);
            auto parent = dir.parent_path();
            if (parent == dir) {
                break;
            }
            dir = parent;
        }
    } catch (...) {
    }

    return out;
}

inline std::string resolve_data_file(const std::string& filename, const std::string& hint = "") {
    for (const auto& p : data_file_candidates(filename, hint)) {
        if (path_is_file(p)) {
            std::error_code ec;
            auto abs = std::filesystem::absolute(p, ec);
            return ec ? p.lexically_normal().string() : abs.lexically_normal().string();
        }
    }
    return (std::filesystem::path("data") / filename).string();
}

} // namespace egy_names
