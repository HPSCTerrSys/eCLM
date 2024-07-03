# North-Rhine Westphalia

This regional test case covers the state of North-Rhine Westphalia at a grid size of 300x300 grid cells. It runs in BGC mode (prognostic calculation of vegetation states at each time step for all 78 available plant functional types (PFTs) including crops). To set up eCLM and execute this test case, please follow the instructions below.

```{attention}
 The following only works for JSC users as the model inputs and forcing files are thus far not publicly available.
```

```{figure} ../images/nrw_boas.png
:height: 300px
:name: fig4

The DE-NRW domain extension and dominant land use type. Adapted from <a href="https://doi.org/10.5194/hess-27-3143-2023" target="_blank">Boas et al (2023)</a>.
```

## 1. Copy the namelist files
For JSC users, all required namelist and input files to run this case are in the shared directory `/p/scratch/cslts/shared_data/rlmod_eCLM`

```sh
cp /p/scratch/cslts/shared_data/rlmod_eCLM/example_cases/nrw_300x300  test_cases/
cd test_cases/nrw_300x300
```

## 2. Check case setup

Print out the namelist files and look at the customized configurations.

```sh
cat lnd_in
cat drv_in
```

## 3. Run the test case.

Customize the copied job script `run-eclm-job.sh` as desired. In this example, it is already customized to this test case, you should just adapt the SBATCH parameters `--account` to your compute project and `--partition` to your system. As the NRW case is a regional domain, the number of processors is increased to 128 compared to the single-column case (SBATCH parameter `--ntasks-per-node=128`). 

```sh
sbatch run-eclm-job.sh
```
To check the job status, run `sacct`.

The model run is successful if the history files (nrw_300x300.clm2.h0.*.nc) have been generated.