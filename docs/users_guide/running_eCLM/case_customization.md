# Case customization

You can customize your case in various ways:

1. Customizing input data
2. Customizing case run 
3. Customizing case output

## 1. Customizing input data


## 2. Customizing case run


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
