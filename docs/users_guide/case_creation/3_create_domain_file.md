# Create domain file

In this step you will create the domain file for your case using `gen_domain`. First, you need to navigate into the `gen_domain_files/src/` directory and compile it with the loaded modules ifort, imkl, netCDF and netCDF-Fortran.

```sh
cd ../gen_domain_files/src/

# Compile the script
ifort -o ../gen_domain gen_domain.F90 -mkl -lnetcdff -lnetcdf
```

Before running the script you need to export the environment variable `GRIDNAME` (same as what you used for the SCRIP grid file and in the `runscript_mkmapdata.sh` script).

```sh
export GRIDNAME="your gridname"
```
Then you can run the script:
```sh
cd ../
./gen_domain -m $MAPFILE -o $GRIDNAME -l $GRIDNAME
```

The output of this will be two netCDF files `domain.lnd.*.nc` and `domain.ocn.*.nc` that define the land and ocean mask respectively. The land mask will inform the atmosphere and land inputs of eCLM when running a case.

**Congratulations!** You successfully created your domain files and can now move on to the final next step to create your surface data.
