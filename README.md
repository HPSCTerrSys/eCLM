# eCLM
[![status: alpha](https://img.shields.io/badge/status-alpha-yellow)](https://github.com/HPSCTerrSys/eCLM)

eCLM is based from [Community Land Model 5.0 (CLM5.0)]. It has the same modelling capabilities as CLM5 but with a more simplified infrastructure for build and namelist generation. The build system is handled entirely by CMake and namelists are generated through a small set of Python scripts. Only Fortran source codes necessary for a functional land model simulation were imported from CLM5. 

Unlike CLM5, there are no built-in batch scripts in eCLM. It is up to system maintainers or users to craft their own workflows by combining the basic tools in this repo plus the native tools in their respective platforms. If you are a user in [IBG-3], you may want to check out the [eCLM-JSC] repo.

## Installation

### Build requirements

* MPI
* netCDF-C
* netCDF-Fortran
* PnetCDF

### Building eCLM

1. Configure CMake build options.

```sh
# User-specific variables
BUILD_DIR="bld"
INSTALL_DIR="out"

# Run cmake
cmake -S src -B "$BUILD_DIR" \
      -DCMAKE_INSTALL_PREFIX="$INSTALL_DIR" \
      -DCMAKE_C_COMPILER=mpicc \
      -DCMAKE_Fortran_COMPILER=mpifort
```

Additionally, you may specify these optional build variables.

* `CMAKE_BUILD_TYPE=DEBUG|RELEASE`. Defaults to `RELEASE`.
* `BUILD_MCT=TRUE|FALSE`. Defaults to `TRUE`, meaning eCLM will build its internal MCT library. If set to `FALSE`, you must specify the path to external MCT library via `CMAKE_PREFIX_PATH`.

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

## Status

eCLM has only been lightly tested; so far it could run a single-point and a regional case in Germany. Still, more work has to be done to ensure the correctness of the build process and the generated namelists. A user-friendly and lightweight approach to model configuration also has to be developed. *eCLM is still in alpha version and would not be ready for production runs anytime soon*.

[Community Land Model 5.0 (CLM5.0)]: https://github.com/ESCOMP/CTSM/tree/release-clm5.0
[IBG-3]: https://www.fz-juelich.de/ibg/ibg-3/EN/Home/home_node.html
[eCLM-JSC]: https://icg4geo.icg.kfa-juelich.de/ModelSystems/clm/eclm-jsc