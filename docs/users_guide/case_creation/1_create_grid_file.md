# Create SCRIP grid file

The first step in creating your input data is to define your model domain and the grid resolution you want to model in. There are several options to create the SCRIP grid file that holds this information:
1. Using the `mkscripgrid.py` script to create a regular latitude longitude grid.
2. Using the `produce_scrip_from_griddata.ncl` script to convert an existing netCDF file that holds the latidude and longitude centers of your grid in 2D (This allows you to create a curvilinear grid). 
3. Similar to the first option but using the `scrip_mesh.py` script to create the SCRIP grid file.

To start the SCRIP grid file creation navigate into the `mkmapgrids` directory where you will find the above mentioned scripts.

```sh
cd mkmapgrids
```

## 1. Create SCRIP grid file with `mkscripgrid.py`

To use `mkscripgrid.py`, first open the script (for example using vim text editor) and adapt the variables that describe your grid. These include your grid name, the four corner points of your model domain as well as the resolution (lines 42-50 of the script). Then you can execute the script:

```sh
python mkscripgrid.py
```

```{attention}
The `mkscripgrid.py` script requires numpy and netCDF4 python libraries to be installed (use pip install to do that if not already installed).
```

The output will be a SCRIP grid netCDF file containing the grid dimension and the center and corners for each grid point. It will have the format `SCRIPgrid_"Your grid name"_nomask_c"yymmdd".nc`

## 2. Create SCRIP grid file from griddata with `produce_scrip_from_griddata.ncl`

Unfortunately, NCL is not maintained anymore in the new software stages. Therefore, in order to use it you first need to load an older Stage and the required software modules:

```sh
module load Stages/2020
module load Intel/2020.2.254-GCC-9.3.0
module load ParaStationMPI/5.4.7-1
module load NCL
```

Next, adapt the input in `produce_scrip_from_griddata.ncl` to your gridfile.This includes choosing a name for your output file "OutFileName", adjusting the filename of your netcdf file in line 9 and the variable names for longitude/latitude in lines 10-11. Then execute:

```sh
ncl produce_scrip_from_griddata.ncl
```

## 3. Create SCRIP grid file from griddata using `scrip_mesh.py`

Alternatively to the first option, you can use the python script `scrip_mesh.py`. Like the ncl script it can create SCRIP files including the calculation of corners. It takes command line arguments like this:

```sh
python3 scrip_mesh.py --ifile NC_FILE.nc --ofile OUTPUT_SCRIP.nc --oformat SCRIP # replace NC_FILE.nc with your netcdf file and choose a name for your output SCRIP grid file for OUTPUT_SCRIP.nc
```

---

**Congratulations!** You successfully created your SCRIP grid file and can now move on to the next step.