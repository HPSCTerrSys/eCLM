# Create surface file

In this step you will create the surface data file using the `mksurfdata.pl` script.
First, we will compile the script with `make` in the `mksurfdata/src` directory.


```sh
cd ../mksurfdata/src

# Compile the script
make
```

The script needs a few environment variables such as `GRIDNAME` (exported in the previous step), `CDATE` (date of creation of the mapping files which can be found at the end of each `map_*` file before the file extension) and `CSMDATA` (the path where the raw data for the surface file creation is stored) before executing the script.

```sh
export CDATE=`date +%y%m%d`
export CSMDATA="/p/scratch/cslts/shared_data/rlmod_eCLM/inputdata/" # this works for JSC users only, for non JSC users see below 

# generate surfdata
./mksurfdata.pl -r usrspec -usr_gname $GRIDNAME -usr_gdate $CDATE -l $CSMDATA -allownofile -y 2000 -crop
```

```{tip} 
The `-crop` option used in `./mksurfdata.pl` will create a surface file for BGC mode with all crops active. If you want to use SP mode, you should run without this option.

Use `./mksurfdata.pl -help` to display all options possible for this script. 
For example:
- `hirespft` - If you want to use the high-resolution pft dataset rather than the default lower resolution dataset (low resolution is at half-degree, high resolution at 3minute), hires is only available for present-day (2000)
```

**For non JSC users**:
Non JSC users can download the raw data from HSC datapub using this <a href="https://datapub.fz-juelich.de/slts/eclm/surfdata/rawdata/" target="_blank">link</a> or from the official <a href="https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/lnd/clm2/rawdata/" target="_blank">rawdata repository</a> using `wget` before submitting the script. 

```sh
wget "RAWDATA_LINK"/"NAME_OF_RAWDATA_FILE" --no-check-certificate # repeat this for every rawdata file
```

You will see a "Successfully created fsurdat files" message displayed at the end of the script if it ran through.

The output will be a netCDF file similar to `surfdata_"your grid name"_hist_78pfts_CMIP6_simyr2000_c"yymmdd".nc`.

**Congratulations!** You successfully created your surface data file! In the next step you will learn how to create your own atmospheric forcings.