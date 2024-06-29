# Create surface file

In this step you will create the surface data file using the `mksurfdata.pl` script.
First, we will compile the script with `make` in the `mksurfdata/src` directory.


```sh
cd ../mksurfdata/src

# Compile the script
make
```

The script needs a few environment variables such as `GRIDNAME` (exported in the previous step), `CDATE` (date of creation of your SCRIP grid file as used in the mapping files creation) and `CSMDATA` (the path where the raw data of CLM is stored) before executing the script.

```sh
export CDATE=`date +%y%m%d`
export CSMDATA="full path to your mkmapdata/ directory"

# generate surfdata
./mksurfdata.pl -r usrspec -usr_gname $GRIDNAME -usr_gdate $CDATE -l $CSMDATA -allownofile -y 2000 -crop
```
The `-crop` option will create a surface file for BGC mode with all crops active. If you want to use SP mode, you should not use this option. 

```{tip} 
Use `./mksurfdata.pl -help` to display all options possible for this script. 
For example:
- hirespft - If you want to use the high-resolution pft dataset rather than the default lower resolution dataset (low resolution is at half-degree, high resolution at 3minute), hires is only available for present-day [2000]
```

The output will a netCDF file similar to `surfdata_"your grid name"_hist_78pfts_CMIP6_simyr2000_c"yymmdd".nc`.


**Congratulations!** You successfully created your surface data file! In the next step you will learn how to create your own atmospheric forcings.