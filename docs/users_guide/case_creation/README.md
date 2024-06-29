# Creating a custom case

This workflow will guide you through creating your own input datasets at a resolution of your choice for eCLM simulations.

Throughout this process, you will use a range of different scripts to create the necessary files.

```{figure} ../images/Build_custom_input.png
:height: 500px
:name: fig3

Overview of the work flow for the creation of custom surface datasets adapted from the <a href="https://escomp.github.io/ctsm-docs/versions/release-clm5.0/html/users_guide/using-clm-tools/creating-surface-datasets.html#" target="_blank">CLM5.0 User's Guide</a>.
```
<p>

This workflow is based on the following Github repository that contains all the necessary tools: https://github.com/HPSCTerrSys/eCLM_static_file_workflow. It follows the official CLM-workflow but makes a few adaptations. The basis is the clm5.0 release but there might be newer developments in the <a href="https://github.com/ESCOMP/CTSM.git" target="_blank">CTSM</a> and <a href="https://github.com/ESMCI/cime.git" target="_blank">CIME</a> Github repositories. 

To get started, log into the JSC system and clone the repository for instance into your folder in `project1` that you created during the build of eCLM.

```sh
cd /p/project1/projectID/user1 # replace projectID with your compute project and user1 with your username

git clone https://github.com/HPSCTerrSys/eCLM_static_file_workflow.git 
```

Sourcing the environment file that is contained in the repository will load all the required software modules.

```sh
cd eCLM_static_file_workflow/
source jsc.2023_Intel.sh
```
You are now ready to start with the workflow.

```{tableofcontents}
```