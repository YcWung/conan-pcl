cmake_minimum_required(VERSION 2.8.11)
project(cmake_wrapper)

find_package(flann REQUIRED)
add_library(FLANN::FLANN ALIAS flann::flann)

if(MSVC)
    add_compile_options(/bigobj)
endif()

add_subdirectory(${PCL_SRC_DIR} ${CONAN_FOLDERS_SOURCE})
