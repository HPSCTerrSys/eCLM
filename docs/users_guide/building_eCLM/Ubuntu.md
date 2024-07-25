# Ubuntu

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
sudo apt install libblas-dev liblapack-dev
sudo apt install libxml2-utils pylint wget cmake netcdf-bin libnetcdf-dev libnetcdff-dev libpnetcdf-dev gfortran openmpi-bin libopenmpi-dev
```

Have a look in `.github/workflows/CI.yml` to find the Ubuntu packages
installed for CI-testing eCLM.
