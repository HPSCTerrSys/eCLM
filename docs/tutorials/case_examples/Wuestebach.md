# Single-Point Wuestebach

**NOTE**: For non-JSC systems, the Wuestebach input files must be downloaded first by running `./download_wtb_files`.

```sh
# 1. Create case folder
wtb_case_dir=test_cases/wtb_1x1_$SYSTEMNAME
mkdir -p $wtb_case_dir
cd $wtb_case_dir

# 2. Generate namelists
cp $ECLM_SCRIPTS_ROOT/sample_cases/wtb_1x1/* .
find . -type f -name 'user_datm.streams.txt*' | xargs sed -i "s#__ECLM_SHARED_DATA__#$ECLM_SHARED_DATA#g"
clm5nl-gen wtb_1x1.toml

# 3. Generate sbatch script
$ECLM_SCRIPTS_ROOT/job_scripts/gen_job_script

#  Customize job script as desired. You may change the sbatch parameters
#  (e.g. job account, number tasks/nodes), add post-processing steps, etc.
vim eclm.job.jurecadc    # replace 'eclm.job.jurecadc' with the generated log file

#  NOTE: As Wuestebach is a single-column case, the number of processors
#  should be set to 1. Modify the jobscript to reflect this, i.e. set
#  the SBATCH parameter --ntasks-per-node=1.

# 4. Submit job to queue
sbatch eclm.job.jurecadc

# 5. Monitor job status (hit Ctrl+C to exit)
watch sacct
```

The model run is successful if the history files (`wtb_1x1.clm2.h0.*.nc`) have been generated.