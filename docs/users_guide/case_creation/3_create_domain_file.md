# Create domain file

In this step you will create the domain file for your case using `gen_domain`. First, you need to navigate into the `gen_domain_files/src/` directory and compile it with the loaded modules ifort, imkl, netCDF and netCDF-Fortran.

```sh
cd ../gen_domain_files/src/

# Compile the script
ifort -o ../gen_domain gen_domain.F90 -mkl -lnetcdff -lnetcdf
```
```{attention}
If you get a message saying "ifort: command line remark #10412: option '-mkl' is deprecated and will be removed in a future release. Please use the replacement option '-qmkl'" or the compiling fails, replace `-mkl` with `-qmkl`.
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

However, `gen_domain` defaults the use of the variables `mask` and `frac` on these files to be for ocean models, i.e. 0 for land and 1 for ocean. So to use them you have to either manipulate the `domain.lnd.*.nc` file to have mask and frac set to 1 instead of 0 (WARNING: some netCDF script languages have `mask` as a reserved keyword e.g. NCO, use single quotation marks as workaround).
Or simply swap/rename the `domain.lnd.*.nc` and `domain.ocn.*.nc` file:

```sh
mv domain.lnd."your gridname"_"your gridname"."yymmdd".nc temp.nc
mv domain.ocn."your gridname"_"your gridname"."yymmdd".nc domain.lnd."your gridname"_"your gridname"."yymmdd".nc
mv temp.nc domain.ocn."your gridname"_"your gridname"."yymmdd".nc
```

**Congratulations!** You successfully created your domain files and can now move on to the final next step to create your surface data.
