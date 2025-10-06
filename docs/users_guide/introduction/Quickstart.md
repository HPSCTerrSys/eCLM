# Installing eCLM

## Requirements

* MPI compilers (e.g. OpenMPI)
* CMake
* LAPACK
* [netCDF C and Fortran libraries](https://downloads.unidata.ucar.edu/netcdf)
* [PnetCDF](https://github.com/Parallel-NetCDF/PnetCDF)

## Method 1: Build eCLM through TSMP2 (recommended)

The easiest way to install eCLM is through [TSMP2 build system](https://github.com/HPSCTerrSys/TSMP2).

```sh
# Download TSMP2
git clone https://github.com/HPSCTerrSys/TSMP2.git
cd TSMP2

# Build and install eCLM
./build_tsmp2.sh --eCLM
```

## Method 2: Building from source (for advanced users)

```sh
# Download eCLM
git clone https://github.com/HPSCTerrSys/eCLM.git
cd eCLM

# Create eCLM install directory
mkdir install

# Set compilers
export CC=mpicc FC=mpifort

# Build and install eCLM
cmake -S src -B bld -DCMAKE_INSTALL_PREFIX=install
cmake --build bld --parallel
cmake --install bld
```

