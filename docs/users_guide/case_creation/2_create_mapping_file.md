# Create mapping file

To start the mapping file creation navigate into the `mkmapdata` directory where you will find the script needed for this step.

```sh
cd ../mkmapdata
```

Before you run `runscript_mkmapdata.sh` you need to adapt some environment variables in lines 23-25 of the script. For this open the script (for example using vim text editor) and enter the name of your grid under `GRIDNAME` (same as what you used for the SCRIP grid file). For `CDATE`, use the date that your SCRIP grid file was created (per default the script uses the current date, if you created the SCRIPgrid file at some other point, you find the date of creation at the end of your SCRIPgrid file or in the file information). Lastly, provide the full path and name of your SCRIP grid file under `GRIDFILE`. Save and close the script.

To create your mapping files, you need a set of rawdata. For now and until we have a common repository for this data, download them and adapt the path ("rawpath") in line 29 of the script to their new location. To download the data to the directory use:

```sh
wget --no-check-certificate -i clm_mappingfiles.txt
```

Now you can execute the script:

```sh
sbatch runscript_mkmapdata.sh
```

The output will be a `map_*.nc` file for each of the rawdata files. These files are the input for the surface parameter creation weighted to your grid specifications.

To generate the domain file in the next step a mapfile is needed. This can be any of the generated `map_*.nc` files. So, set the environment variable `MAPFILE` for later use:

```sh
export MAPFILE="path to your mapfiles"/"name of one of your map files"
```

---

**Congratulations!** You successfully created your mapping files and can now move on to the next step.