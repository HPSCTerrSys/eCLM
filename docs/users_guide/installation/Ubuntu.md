# Installing eCLM on Ubuntu

```{warning}
Page under construction
```

## Minimum system requirements for Ubuntu

On Ubuntu the following command should load the necessary system
requirements

```sh
# Update `apt`
sudo apt update

# Install packages
# ----------------

# Utilities
sudo apt install libxml2-utils wget

# Python
sudo apt install python3 python3-pip pylint

# Compiler
sudo apt install gfortran openmpi-bin libopenmpi-dev cmake

# Linear algebra
sudo apt install libblas-dev liblapack-dev

# NetCDF
sudo apt install netcdf-bin libnetcdf-dev libnetcdff-dev libpnetcdf-dev
```

Have a look in `.github/workflows/CI.yml` to find the Ubuntu packages
installed for CI-testing eCLM.
