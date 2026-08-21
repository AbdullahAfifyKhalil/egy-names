from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout

class EgyNamesConan(ConanFile):
    name = "egy-names"
    version = "0.1.1"
    license = "MIT"
    author = "Abdullah Afify"
    url = "https://github.com/AbdullahAfifyKhalil/egy-names"
    description = "A production-grade Egyptian onomastic intelligence library for modern C++."
    topics = ("arabic", "nlp", "egypt", "names", "onomastics")
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        self.requires("zlib/[>=1.2.11]")
        self.requires("nlohmann_json/[>=3.11.0]")

    def layout(self):
        cmake_layout(self)

    def package(self):
        self.copy("*.hpp", dst="include", src="include")
        self.copy("*.json.gz", dst="data", src="data")

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
