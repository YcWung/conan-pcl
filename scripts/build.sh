#!/bin/bash

set -e

ROOT_DIR="$(cd $(dirname $0)/.. && pwd -P)"

mkdir -p "${ROOT_DIR}/build/Release"
pushd "${ROOT_DIR}/build/Release"
conan install ../..
conan build ../..
popd

mkdir -p "${ROOT_DIR}/build/Debug"
pushd "${ROOT_DIR}/build/Debug"
conan install ../.. -s build_type=Debug
conan build ../.. -s build_type=Debug
popd
