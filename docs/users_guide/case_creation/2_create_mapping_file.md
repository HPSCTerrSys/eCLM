# Create mapping file

To start the mapping file creation go into the right directory:

```sh
cd mkmapdata
```

Before you run `runscript_mkmapdata.sh` you need to adapt some environment variables in lines 23-25 of the script. For this open the script (for example using vim text editor) and enter the name of your grid under `GRIDNAME` (same as what you used for the SCRIPgrid file). For `CDATE`, use the date that your SCRIPgrid file was created (per default the script uses the current date, if you created the SCRIPgrid file at some other point, you find the date of creation at the end of your SCRIPgrid file or in the file information). Lastly, provide the whole path and name of your SCRPgrid file under `GRIDFILE`. Save and close the script.

To create your mapping files, you need a set of rawdata. For now and until we have a common repository for this data, download them and adapt the path ("rawpath") in line 29 of the script to their new location. To download the data to the directory use:

```sh
wget --no-check-certificate -i clm_mappingfiles.txt
```

Now you can execute the script:

```sh
sbatch runscript_mkmapdata.sh
```

The output will be a `map_*.nc` file for each of the rawdata files.

Lastly, export the environment variable `MAPFILE` for later use:

```sh
export MAPFILE="path_to_your_mapfiles"/"name_of_one_of_your_map_files"
```