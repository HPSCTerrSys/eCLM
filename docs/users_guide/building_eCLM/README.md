# Building eCLM

## Installation

This section shows you how to build eCLM.

### Minimum system requirements

* MPI 3.1
* netCDF-C 4.7.4
* netCDF-Fortran 4.5.2
* PnetCDF 1.12.1
* LAPACK
* CMake 3.16
* Supported compilers
  - GCC 9.3.0
  - Intel 19.1.2

### Building eCLM

1. Configure CMake build options.

```sh
# User-specific variables
BUILD_DIR="bld"
INSTALL_DIR="eclm"

# Run cmake
cmake -S src -B "$BUILD_DIR" \
      -DCMAKE_INSTALL_PREFIX="$INSTALL_DIR" \
      -DCMAKE_C_COMPILER=mpicc \
      -DCMAKE_Fortran_COMPILER=mpifort
```

Additionally, you may specify these optional build variables.

* `CMAKE_BUILD_TYPE=DEBUG|RELEASE`. Defaults to `RELEASE`.
* `CMAKE_PREFIX_PATH`. Semicolon-separated list of paths (i.e. *install prefixes*) where external libraries might be found. You may need to specify this if CMake cannot find some of the required libraries (e.g. NetCDF, PnetCDF, LAPACK).

2. Build and install eCLM.

```sh
cmake --build "$BUILD_DIR"
cmake --install "$BUILD_DIR"
```

### Install namelist generator Python package

The namelist generator scripts require Python 3.X.

```sh
# Upgrade to latest version of pip
python3 -m pip install --upgrade pip

# Install package
pip3 install --user ./namelist_generator
```
