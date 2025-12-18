# Installing eCLM from source

```{warning}
For advanced users.
```

## Requirements

* MPI compilers (e.g. OpenMPI)
* CMake
* LAPACK
* [netCDF C and Fortran libraries](https://downloads.unidata.ucar.edu/netcdf)
* [PnetCDF](https://github.com/Parallel-NetCDF/PnetCDF)

## Steps

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

## Reference build scripts

- [eCLM build on Ubuntu](https://github.com/HPSCTerrSys/eCLM/blob/4d567d2d68cac0fba977914b4a9c3ba199afd0ff/.github/workflows/CI.yml#L70-L121)
- [eCLM build on TSMP2](https://github.com/HPSCTerrSys/TSMP2/blob/master/cmake/BuildeCLM.cmake)
