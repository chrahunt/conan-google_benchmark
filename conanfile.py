#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil


class GoogleBenchmarkConan(ConanFile):
    name = "google_benchmark"
    version = "1.4.0"
    description = (
        "A library to support the benchmarking of functions, similar"
        " to unit-tests.")
    url = "https://github.com/chrahunt/conan-google_benchmark"
    homepage = "https://github.com/google/benchmark"

    # Indicates License type of the packaged library
    license = "Apache-2.0"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "lto": [True, False],
    }
    default_options = "shared=False", "fPIC=True", "lto=False"

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    requires = ()

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/google/benchmark"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = "benchmark-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['BENCHMARK_ENABLE_TESTING'] = False
        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.configure(
            build_folder=self.build_subfolder,
            source_folder=self.source_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        #self.copy(pattern="LICENSE", dst="license", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()
        self.copy(pattern="*", dst="include", src='include')
        self.copy(pattern="*", dst="lib", src='lib')

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os != 'Windows':
            self.cpp_info.cppflags = ["-pthread"]
