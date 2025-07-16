# Installing eCLM from source

```{warning}
For advanced users.
```

**Requirements**

* MPI compilers (e.g. OpenMPI)
* CMake
* LAPACK
* [netCDF C and Fortran libraries](https://downloads.unidata.ucar.edu/netcdf)
* [PnetCDF](https://github.com/Parallel-NetCDF/PnetCDF)


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

