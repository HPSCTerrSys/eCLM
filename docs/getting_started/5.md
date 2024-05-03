# North-Rhine Westphalia

**NOTE**: The following only works on JSC systems as the model inputs and forcing files are not publicly available.

```sh
# 1. Create case folder
nrw_case_dir=$SCRATCH/$USER/nrw_300x300_$SYSTEMNAME
mkdir $nrw_case_dir
cd $nrw_case_dir

# 2. Generate namelists
cp $ECLM_SCRIPTS_ROOT/sample_cases/nrw_300x300/* .
clm5nl-gen nrw_300x300.toml

# 3. Generate sbatch script
$ECLM_SCRIPTS_ROOT/job_scripts/gen_job_script

# Customize job script as desired. You may change the sbatch parameters
# (e.g. job account, number tasks/nodes), add post-processing steps, etc.
vim eclm.job.jurecadc    # replace 'eclm.job.jurecadc' with the generated log file 

# 4. Submit job to queue
sbatch eclm.job.jurecadc

# 5. Monitor job status (hit Ctrl+C to exit)
watch sacct
```