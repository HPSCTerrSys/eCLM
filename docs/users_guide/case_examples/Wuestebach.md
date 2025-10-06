# Single-Point Wuestebach

```{warning} TODO
```

This test case at point scale covers the Wuestebach test site that is part of the TERENO network. Wuestebach is a forest site located in the Eifel region in Germany. To set up eCLM and run this test case, follow the instructions below.

```{figure} ../images/wtb_bogena.png
:height: 500px
:name: fig3

Location of the Wüstebach test site within the TERENO Rur/Lower Rhine Valley observatory. Adapted from <a href="http://dx.doi.org/10.2136/vzj2009.0173" target="_blank">Bogena et al (2010)</a>.
```

## 1. Download Wuestebach data files

```sh
git clone https://icg4geo.icg.kfa-juelich.de/ExternalReposPublic/tsmp2-static-files/extpar_eclm_wuestebach_sp.git
cd extpar_eclm_wuestebach_sp/static.resources
generate_wtb_namelists.sh 1x1_wuestebach
cd 1x1_wuestebach
```

## 2. Check the case setup
You can check out the important namelist files.

- The `lnd_in` file is the primary configuration file for the land model component in CLM. It includes settings related to various processes and configurations specific to land surface modeling. For a complete list of `lnd_in`-namelist options, see https://docs.cesm.ucar.edu/models/cesm2/settings/current/clm5_0_nml.html

- The `drv_in` file configures the coupler and driver settings that control how different components of the Earth system model interact. It manages the synchronization and communication between components such as the atmosphere, land, ocean, and sea ice models. For a complete list of `drv_in`-namelist options, see https://docs.cesm.ucar.edu/models/cesm2/settings/current/drv_nml.html


Print out the namelist files and look at the customized configurations.
```sh
cat lnd_in
cat drv_in
```

## 3. Run the test case

```bash
mpirun -np 1 eclm.exe
```

The model run is successful if the history files (`wtb_1x1.clm2.h0.*.nc`) have been generated.
