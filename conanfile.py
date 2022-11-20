# -*- coding: utf-8 -*-

import os
from glob import glob

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools import files
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get, copy
from conan.tools.build import check_min_cppstd
from conan.tools.scm import Version
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout

required_conan_version = ">=1.53.0"

class LibPclConan(ConanFile):
    name = "pcl"
    version = "1.12.1"
    description = (
        "The Point Cloud Library is a standalone, large scale, open project for 2D/3D image and point cloud processing"
    )
    url = "https://github.com/PointCloudLibrary/pcl"
    homepage = "http://www.pointclouds.org/"
    license = "BSD-3-Clause"
    # generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        # Options for modules
        "module_2d": [True, False],
        "module_cuda": [True, False],
        "module_features": [True, False],
        "module_filters": [True, False],
        "module_geometry": [True, False],
        "module_gpu": [True, False],
        "module_io": [True, False],
        "module_kdtree": [True, False],
        "module_keypoints": [True, False],
        "module_ml": [True, False],
        "module_octree": [True, False],
        "module_outofcore": [True, False],
        "module_people": [True, False],
        "module_recognition": [True, False],
        "module_registration": [True, False],
        "module_sample_consensus": [True, False],
        "module_search": [True, False],
        "module_segmentation": [True, False],
        "module_simulation": [True, False],
        "module_stereo": [True, False],
        "module_surface": [True, False],
        "module_surface_on_nurbs": [True, False],
        "module_tracking": [True, False],
        "module_visualization": [True, False],
        # Options for dependencies
        "with_cuda": [True, False],
        "with_davidsdk": [True, False],
        "with_dssdk": [True, False],
        "with_ensenso": [True, False],
        "with_libpng": [True, False],
        "with_libusb": [True, False],
        "with_opengl": [True, False],
        "with_openni": [True, False],
        "with_openni2": [True, False],
        "with_pcap": [True, False],
        "with_qhull": [True, False],
        "with_qt": [True, False],
        "with_rssdk": [True, False],
        "with_rssdk2": [True, False],
        "with_vtk": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        # TODO: choose which modules are enabled by default
        "module_2d": True,
        "module_cuda": False,
        "module_features": True,
        "module_filters": True,
        "module_geometry": True,
        "module_gpu": False,
        "module_io": True,
        "module_kdtree": True,
        "module_keypoints": True,
        "module_ml": True,
        "module_octree": True,
        "module_outofcore": False,
        "module_people": False,
        "module_recognition": True,
        "module_registration": True,
        "module_sample_consensus": True,
        "module_search": True,
        "module_segmentation": True,
        "module_simulation": False,
        "module_stereo": True,
        "module_surface": True,
        "module_surface_on_nurbs": True,
        "module_tracking": True,
        "module_visualization": False,
        # TODO: choose which options are enabled by default
        "with_cuda": False,
        "with_davidsdk": False,
        "with_dssdk": False,
        "with_ensenso": False,
        "with_libpng": False,
        "with_libusb": False,  # android has to be false
        "with_opengl": False,  # android has to be false
        "with_openni": False,
        "with_openni2": False,
        "with_pcap": False,
        "with_qhull": False,
        "with_qt": False,
        "with_rssdk": False,
        "with_rssdk2": False,
        "with_vtk": False,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.with_cuda:
            raise ConanInvalidConfiguration("Option 'with_cuda' is not supported yet")
        if self.options.with_davidsdk:
            raise ConanInvalidConfiguration("Option 'with_davidsdk' is not supported yet")
        if self.options.with_dssdk:
            raise ConanInvalidConfiguration("Option 'with_dssdk' is not supported yet")
        if self.options.with_ensenso:
            raise ConanInvalidConfiguration("Option 'with_ensenso' is not supported yet")
        if self.options.with_openni:
            raise ConanInvalidConfiguration("Option 'with_openni' is not supported yet")
        if self.options.with_openni2:
            raise ConanInvalidConfiguration("Option 'with_openni2' is not supported yet")
        if self.options.with_pcap:
            raise ConanInvalidConfiguration("Option 'with_pcap' is not supported yet")
        if self.options.with_qhull:
            raise ConanInvalidConfiguration("Option 'with_qhull' is not supported yet")
        if self.options.with_qt:
            raise ConanInvalidConfiguration("Option 'with_qt' is not supported yet")
        if self.options.with_rssdk:
            raise ConanInvalidConfiguration("Option 'with_rssdk' is not supported yet")
        if self.options.with_rssdk2:
            raise ConanInvalidConfiguration("Option 'with_rssdk2' is not supported yet")
        if self.options.with_vtk:
            raise ConanInvalidConfiguration("Option 'with_vtk' is not supported yet")

        if self.options.module_outofcore:
            raise ConanInvalidConfiguration("Module 'outofcore' is not supported yet")
        if self.options.module_people:
            raise ConanInvalidConfiguration("Module 'people' is not supported yet")
        if self.options.module_simulation:
            raise ConanInvalidConfiguration("Module 'simulation' is not supported yet")
        if self.options.module_visualization:
            raise ConanInvalidConfiguration("Module 'visualization' is not supported yet")

    def requirements(self):
        # Mandatory requirements
        self.requires("boost/1.80.0")
        self.requires("eigen/3.4.0")
        self.requires("flann/1.9.2")

        # Optional requirements
        if self.options.with_libpng:
            self.requires("libpng/1.6.38")
        if self.options.with_libusb:
            self.requires("libusb/1.0.26")

        # Module-dependent requirements
        if self.options.module_simulation:
            self.requires("glew/2.2.0")

    def export_sources(self):
        copy(self, "CMakeLists.txt", src=self.recipe_folder, dst=self.export_sources_folder)
        export_conandata_patches(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version],
                  destination=self.source_folder, strip_root=True)

    def layout(self):
        cmake_layout(self, src_folder="src")
        print("build_type {}".format(self.settings.build_type))
        self.folders.build = os.path.join("build", str(self.settings.build_type))
        self.folders.generators = os.path.join(self.folders.build, "generators")
        self.cpp.source.includedirs = glob("*/include", root_dir=os.path.join(self.recipe_folder, self.folders.source))
        self.cpp.build.libdirs=[os.path.join(self.folders.source, "lib")]
        self.cpp.build.bindirs=[os.path.join(self.folders.source, "bin")]
        self.cpp.build.includedirs=[os.path.join(self.folders.source, "include")]
        libs = glob("*.lib", root_dir=os.path.join(self.recipe_folder, self.folders.build, self.folders.source, "lib"))
        libs = [os.path.splitext(n)[0] for n in libs]
        self.cpp.build.libs=libs

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["PCL_SRC_DIR"] = self.source_folder.replace("\\", "/")
        tc.variables["CONAN_FOLDERS_SOURCE"] = self.folders.source
        tc.variables["PCL_SHARED_LIBS"] = self.options.shared
        tc.variables["PCL_BUILD_WITH_BOOST_DYNAMIC_LINKING_WIN32"] = self.options["boost"].shared
        tc.variables["PCL_BUILD_WITH_FLANN_DYNAMIC_LINKING_WIN32"] = self.options["flann"].shared
        tc.variables["FLANN_USE_STATIC"] = "OFF" if self.options["flann"].shared else "ON"
        if self.options.with_qhull:
            tc.variables["PCL_BUILD_WITH_QHULL_DYNAMIC_LINKING_WIN32"] = self.options["qhull"].shared

        # Do not build extra tooling & options
        tc.variables["BUILD_all_in_one_installer"] = False
        tc.variables["BUILD_apps"] = False
        tc.variables["BUILD_examples"] = False
        tc.variables["BUILD_global_tests"] = False
        tc.variables["BUILD_tools"] = False
        tc.variables["WITH_DOCS"] = False

        # Build modules as needed
        tc.variables["BUILD_2d"] = self.options.module_2d
        tc.variables["BUILD_common"] = True  # Always build at least common
        tc.variables["BUILD_CUDA"] = self.options.module_cuda
        tc.variables["BUILD_features"] = self.options.module_features
        tc.variables["BUILD_filters"] = self.options.module_filters
        tc.variables["BUILD_geometry"] = self.options.module_geometry
        tc.variables["BUILD_GPU"] = self.options.module_gpu
        tc.variables["BUILD_io"] = self.options.module_io
        tc.variables["BUILD_kdtree"] = self.options.module_kdtree
        tc.variables["BUILD_keypoints"] = self.options.module_keypoints
        tc.variables["BUILD_ml"] = self.options.module_ml
        tc.variables["BUILD_octree"] = self.options.module_octree
        tc.variables["BUILD_outofcore"] = self.options.module_outofcore
        tc.variables["BUILD_people"] = self.options.module_people
        tc.variables["BUILD_recognition"] = self.options.module_recognition
        tc.variables["BUILD_registration"] = self.options.module_registration
        tc.variables["BUILD_sample_consensus"] = self.options.module_sample_consensus
        tc.variables["BUILD_search"] = self.options.module_search
        tc.variables["BUILD_segmentation"] = self.options.module_segmentation
        tc.variables["BUILD_simulation"] = self.options.module_simulation
        tc.variables["BUILD_stereo"] = self.options.module_stereo
        tc.variables["BUILD_surface"] = self.options.module_surface
        tc.variables["BUILD_surface_on_nurbs"] = self.options.module_surface_on_nurbs
        tc.variables["BUILD_tracking"] = self.options.module_tracking
        tc.variables["BUILD_visualization"] = self.options.module_visualization

        # Configure dependencies as needed
        tc.variables["WITH_CUDA"] = self.options.with_cuda
        tc.variables["WITH_DAVIDSDK"] = self.options.with_davidsdk
        tc.variables["WITH_DSSDK"] = self.options.with_dssdk
        tc.variables["WITH_ENSENSO"] = self.options.with_ensenso
        tc.variables["WITH_LIBUSB"] = self.options.with_libusb
        tc.variables["WITH_OPENGL"] = self.options.with_opengl
        tc.variables["WITH_OPENNI"] = self.options.with_openni
        tc.variables["WITH_OPENNI2"] = self.options.with_openni2
        tc.variables["WITH_PCAP"] = self.options.with_pcap
        tc.variables["WITH_PNG"] = self.options.with_libpng
        tc.variables["WITH_QHULL"] = self.options.with_qhull
        tc.variables["WITH_QT"] = self.options.with_qt
        tc.variables["WITH_RSSDK"] = self.options.with_rssdk
        tc.variables["WITH_RSSDK2"] = self.options.with_rssdk2
        tc.variables["WITH_VTK"] = self.options.with_vtk
        
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder = self.export_sources_folder)
        cmake.build()

    def package(self):
        copy(self, "LICENSE.txt", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "PCL"
        self.cpp_info.names["cmake_find_package_multi"] = "PCL"
        self.cpp_info.libs = files.collect_libs(self)

        if self.settings.os != "Android":
            version_short = ".".join(self.version.split(".")[:2])
            self.cpp_info.includedirs = ["include/pcl-{}".format(version_short)]
