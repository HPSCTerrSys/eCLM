# Analyzing model output

As a reminder, the model output can be found in your case directory. All eCLM output files are in netCDF format (.nc). If you are running for different time sampling frequencies (set in the `lnd_in` namelist), there will be separate files created for each frequency, e.g. `my_case.h0.1993-01.nc` and `my_case.h1.1993-01.nc`.

NetCDF is supported by many languages including Python, Matlab, R, NCL, IDL; tool suites of file operators (NCO, CDO) and viewing tools like ncview or ncdump. ncdump helps you to get an overview of the file structure and ncview is a graphical interface that allows to interactively visualize a selected variable across a selected range (time, spatial).

## Using Ncview

To use ncview you first have to load the ncview module. You also need <a href="http://www.straightrunning.com/XmingNotes/" target="_blank">Xming</a> to be active to display the ncview window. Then you can open ncview and look at your file. Afterward, you can simply close the ncview interface to get back to your terminal

```sh
module load ncview
ncview FILENAME.nc # replace FILENAME with your output history file
```

```{figure} images/ncview.png
:height: 400px
:name: fig4

Example of ncview interface.
```

## Using ncdump

The utility ncdump can be used to show the contents of netCDF files.

```sh
# Output a summary of your file (dimensions, variables, global attributes)
ncdump -h FILENAME.nc # replace FILENAME with your output history file

# Show the data for a specific variable
ncdump -v VAR1 FILENAME.nc # replace VAR1 with the variable of interest and FILENAME with your output history file
```

See `ncdump --help` for more options.

## Using Python

For scientific output analysis and visualizations, programming languages like Python are recommended. 

You can use Jupyter Notebooks on JSC machines to directly access the model input and output data (<a href="https://jupyter.jsc.fz-juelich.de/hub/login?next=%2Fhub%2Fhome" target="_blank">login to Jupyter-JSC</a>).
If you have access to <a href="https://gitlab.jsc.fz-juelich.de/" target="_blank">Gitlab</a>, you can check the tutorial for Jupyter Notebooks on JSC machines through the following link: <a href="https://gitlab.jsc.fz-juelich.de/sdlts/FallSchool_HPSC_TerrSys/ictp-workshop-tutorials/-/wikis/Jupyter-JSC" target="_blank">JupyterLab on JSC</a>.

An exemplary notebook for eCLM output analysis and an annual output file covering the period from 2017-01-01 to 2017-12-31 for the NRW domain are available in the shared data directory `/p/scratch/cslts/shared_data/rlmod_eCLM/`. Copy the Jupyter Notebook to your directory before modifying it.

```sh
cp /p/scratch/cslts/shared_data/rlmod_eCLM/Analyse_ECLM_Input_Output.ipynb $MYPROJECT
```

```{important}
Remember to stop the JupyterLab after usage! See point 3 in <a href="https://gitlab.jsc.fz-juelich.de/sdlts/FallSchool_HPSC_TerrSys/ictp-workshop-tutorials/-/wikis/Jupyter-JSC" target="_blank">JupyterLab on JSC</a>
```