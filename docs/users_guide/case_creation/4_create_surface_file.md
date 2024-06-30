# Create surface file

In this step you will create the surface data file using the `mksurfdata.pl` script.
First, we will compile the script with `make` in the `mksurfdata/src` directory.


```sh
cd ../mksurfdata/src

# Compile the script
make
```

The script needs a few environment variables such as `GRIDNAME` (exported in the previous step), `CDATE` (date of creation of the mapping files which can be found at the end of each `map_*` file before the file extension) and `CSMDATA` (the path where the raw data of CLM is stored) before executing the script. For the rawdata the script expects a directory structure like `mkmapdata/lnd/clm2/rawdata` (you can do this by executing `mkdir -p lnd/clm2/rawdata` in your `mkmapdata` directory).

```sh
export CDATE=`date +%y%m%d`
export CSMDATA="full path to your mkmapdata/lnd/clm2/rawdata directory"

# generate surfdata
./mksurfdata.pl -r usrspec -usr_gname $GRIDNAME -usr_gdate $CDATE -l $CSMDATA -allownofile -y 2000 -crop
```


Running the script will give you an error because you have not downloaded the rawdata yet. The list of required rawdata can be in the `mksurfdata_map.namelist` file in the directory. Until we have a shared location for this data, download them from the official <a href="https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/lnd/clm2/rawdata/" target="_blank">rawdata repository</a> using `wget`.

```sh
wget https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/lnd/clm2/rawdata/"NAME_OF_RAWDATA" --no-check-certificate # repeat this for every rawdata file
```

Now resubmit the script and it should run successfully. If it did you will see a "Successfully created fsurdat files" message displayed at the end.

```{tip} 
The `-crop` option used in `./mksurfdata.pl` will create a surface file for BGC mode with all crops active. If you want to use SP mode, you should run without this option.

Use `./mksurfdata.pl -help` to display all options possible for this script. 
For example:
- hirespft - If you want to use the high-resolution pft dataset rather than the default lower resolution dataset (low resolution is at half-degree, high resolution at 3minute), hires is only available for present-day [2000]
```

The output will be a netCDF file similar to `surfdata_"your grid name"_hist_78pfts_CMIP6_simyr2000_c"yymmdd".nc`.


**Congratulations!** You successfully created your surface data file! In the next step you will learn how to create your own atmospheric forcings.