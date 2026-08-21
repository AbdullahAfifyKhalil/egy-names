cmake_minimum_required(VERSION 3.15)
project(egy_names
    VERSION 0.3.1
    DESCRIPTION "A production-grade C++ library for Egyptian onomastic intelligence"
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(ZLIB REQUIRED)
find_package(nlohmann_json REQUIRED)

add_library(egy_names INTERFACE)
target_include_directories(egy_names INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

target_link_libraries(egy_names INTERFACE
    ZLIB::ZLIB
    nlohmann_json::nlohmann_json
)

# Smoke test executable
add_executable(smoke_test tests/smoke_test.cpp)
target_link_libraries(smoke_test PRIVATE egy_names)

# Copy data file to build directory
add_custom_command(TARGET smoke_test POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E make_directory $<TARGET_FILE_DIR:smoke_test>/data
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ${CMAKE_CURRENT_SOURCE_DIR}/data/names.json.gz
        $<TARGET_FILE_DIR:smoke_test>/data/names.json.gz
)
