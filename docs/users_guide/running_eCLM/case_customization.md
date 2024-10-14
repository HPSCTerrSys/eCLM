# Case customization

eCLM uses various namelist files that handle different settings and configurations for running a case. These namelists are similar to CLM5 (only the editing is different) so that you can refer to <a href="https://escomp.github.io/ctsm-docs/versions/release-clm5.0/html/users_guide/setting-up-and-running-a-case/customizing-the-clm-namelist.html#" target="_blank">Section 1.2.3 and 1.2.4 of the CLM5 User's Guide</a>  for more detailed information. 

The eCLM namelist files are:
- Land model namelist `lnd_in` (see <a href="https://docs.cesm.ucar.edu/models/cesm2/settings/2.1.0/clm5_0_nml.html" target="_blank">here</a> for definitions of namelist items)
- Data atmosphere namelist `datm_in` (see <a href="https://docs.cesm.ucar.edu/models/cesm2/settings/2.1.0/datm_nml.html" target="_blank">here</a> for definitions of namelist items)
- River runoff model namelist `mosart_in` (see <a href="https://docs.cesm.ucar.edu/models/cesm2/settings/2.1.0/mosart_nml.html" target="_blank">here</a> for definitions of namelist items)
- Driver namelist `drv_in` (see <a href="https://docs.cesm.ucar.edu/models/cesm2/settings/2.1.0/drv_nml.html" target="_blank">here</a> for definitions of namelist items)
- Driver fields namelist `drv_flds_in` (see <a href="https://docs.cesm.ucar.edu/models/cesm2/settings/2.1.0/drv_fields_nml.html" target="_blank">here</a> for definitions of namelist items)

Many of the namelist options are set by default and you do not need to change them, others you want to adapt when running your own case.

You can customize your case in various ways:

1. Customizing input data
2. Customizing case run 
3. Customizing case output

## 1. Customizing input data

The `lnd_in` file is the primary configuration file for the land model component in eCLM. It includes settings related to various processes and configurations specific to land surface modeling including which files are used as input data to the land and atmosphere.

Important namelist parameters to adjust for model input in `lnd_in` are:

- `fatmlndfrc`: Path to your domain file (holding grid information).
- `fsurdat`: Path to the surface data file (vegetation, soil types, etc.).
- `finidat`: Path to the initial conditions file (empty if doing a cold start).
- `datm_mode`: The mode for atmospheric forcing.
- `paramfile`: Path to your parameter file.
- `streams`: Paths to files containing atmospheric forcing data.

Also, make sure the paths pointing to the various common inputdata is still correct.

Additionally, the `datm_in` holds information on the atmospheric data used to force your simulation and should be adapted to your specific case.

Important namelist parameters in `datm_in` are:

- `domainfile`: Path to your domain file (holding grid information tht will serve as target grid for the atmospheric data)
- `mapalgo`: Sets the spatial interpolation method (usually the default is fine).
- `tintalgo`: Sets the time interpolation algorithm (usually the default is fine).

You should also adapt the stream files when using your own atmospheric forcings.

- `streams`: Data stream files for the different atmospheric input data

## 2. Customizing case run

Customizing your case run involves defining the period over which you want to run, the starting date etc.

Important namelist parameter in the `drv_in` are:

- `start_ymd`: The start date of the simulation in the format YYYYMMDD.
- `stop_n`: The number of time units (days, months, years) for the simulation.
- `stop_option`: The time unit for stop_n (e.g., 'nyears', 'nmonths', 'ndays').
- `stop_ymd`: The end date of the simulation.
- `restart_file`: The name of your restart file (file from which the simulation should start/continue when not doing a cold start)
- `restart_n`: The number of time units (days, months, years) for the restart file.
- `restart_option`: The time unit for restart_n (e.g., 'nyears', 'nmonths', 'ndays').
- `restart_ymd`: The date for writing a restart file.

## 3. Customizing case output

To customize your simulation output, you can specify the history field options in the namelist file `lnd_in`. By default, there is one stream of monthly data files. The field options to customize are:

- `hist_fincl1`: The list of history variables that you want to analyze
- `hist_mfilt`: The number of records within one output file. Default is 1.
- `hist_nhtfrq`: The frequency at which data is recorded and written to a file. Default: 0 – monthly output (monthly averages), positive values: number of model timesteps (half-hourly), negative values: absolute value in hours for output record
  
Here are two examples of a customized output:

**Ex. 1: Daily output with a year’s worth of daily records in a file**
```
hist_fincl1 = "TLAI","TSOI","TOTSOMC"
hist_mfilt = 365
hist_nhtfrq = -24
```
**Ex 2.: Monthly output with each month written to a separate file**
```
hist_fincl1 = "TLAI","GPP","TOTVEGC"
hist_mfilt = 1
hist_nhtfrq = 0
```

To add to the list of output variables, simply extend `hist_fincl1` with the desired history fields. A list of all available CLM5 history fields can be found <a href="https://escomp.github.io/ctsm-docs/versions/release-clm5.0/html/users_guide/setting-up-and-running-a-case/master_list_file.html" target="_blank">here</a>.

 ```{tip}
Additional streams can be added using `hist_fincl2` through `hist_fincl6`, each can have different output frequencies and averaging methods. By default, only the primary history files are active. The primary history files are monthly by default, and other streams are daily but you can adapt this. 
In addition, it can be useful to remove all (or the default) history fields. The option `hist_empty_htapes` allows you to turn off all default output. You can then still output your own reduced list of history fields using `hist_fincl1`.

The default averaging depends on the specific field but for most of the fields it is the average over the output interval. Other averaging can be specified in two ways.
-	By adding an averaging flag to the end of the field name after a colon (for example `TSOI:X`, would output the maximum of soil temperature)
-	Using the `hist_avgflag_pertape` argument

For more details on the usage see <a href="https://escomp.github.io/ctsm-docs/versions/release-clm5.0/html/users_guide/setting-up-and-running-a-case/customizing-the-clm-namelist.html#various-ways-to-change-history-output-averaging-flags" target="_blank">here</a>.
```

After having adjusted your namelist files you may also want to adjust the job script `run-eclm-job.sh` e.g. to change the job name or to allocate more computing resources when running a larger case.

You can then submit the job.

```sh
sbatch run-eclm-job.sh
```

You can monitor your job using `sacct` or `squeue -u $USER`.