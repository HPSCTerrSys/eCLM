# JSC

The following section will explain the necessary steps to download the model from the official repository and get eCLM to run on JSC machines (<a href="https://www.fz-juelich.de/en/ias/jsc/systems/supercomputers/juwels" target="_blank">Juwels</a> or <a href="https://www.fz-juelich.de/en/ias/jsc/systems/supercomputers/jureca" target="_blank">Jureca-DC</a>).


## Prerequisites for JSC users

Before building and running eCLM on JSC machines, the following prerequisites should be fulfilled:

* Create a JSC/JuDoor account
* Join a compute time project
* Login to JSC Gitlab account
* Logging in to JSC machines


### Create a JSC/JuDoor account

You need a JSC account to access the HPC system. For that, you first need a JuDoor account for which you can register <a href="https://judoor.fz-juelich.de/register" target="_blank">here</a>.

Enter your e-mail address and click on "Send confirmation mail".

Afterwards, you will receive an e-mail from dispatch@jsc.de with a personalized link. Click on the link and fill in the form with your data.

Submit the form.

With this, the creation of your JSC account is completed. Now, you can log in to your <a href="https://judoor.fz-juelich.de/login" target="_blank">JuDoor account</a> with your username and password:


### Join a compute time project

Log in to your JuDoor account. Join the compute time project you were assigned to. Under "Projects", choose "+ Join a project":

Enter the project id. You can also add some additional information. Then you can join the project.

The PI/PA will be automatically informed about your join request and can add you to the different systems available in the project. Once you are approved to join the project compute time, you should be able to see the project id under "Projects".


### Login to eCLM-JSC Gitlab account

If you are a user in IBG-3 and want to run eCLM on the JSC machines, you can log in to the <a href="https://icg4geo.icg.kfa-juelich.de/ModelSystems/clm/eCLM_scripts" target="_blank">eCLM-JSC</a> Gitlab repository with your JSC account. This is where we will download the model from in the next section "Setting up eCLM".


### Logging in to JSC machines

To log in to one of the JSC machines you need a JSC account and access to a compute time project (see above).

The final step is to create and upload an SSH key for your account and local machine.

JSC provides thorough instructions for <a href="https://apps.fz-juelich.de/jsc/hps/juwels/access.html#openssh-key-generation" target="_blank">Juwels</a> and <a href="https://apps.fz-juelich.de/jsc/hps/jureca/access.html#openssh-key-generation" target="_blank">Jureca</a> on how to generate and upload SSH keys.


### Additional information on JSC machines

For the full user documentation regarding the JSC systems check:

* <a href="https://apps.fz-juelich.de/jsc/hps/juwels/index.html" target="_blank">Juwels documentation</a>
* <a href="https://apps.fz-juelich.de/jsc/hps/jureca/index.html" target="_blank">Jureca documentation</a>

### Additional software for windows users

#### Xming

Xming allows Windows machines to display a graphical Linux program which is running on a remote Linux server. You can download Xming <a href="http://www.straightrunning.com/XmingNotes/" target="_blank">here</a>.

To enable Xming in the PuTTY configuration, navigate to "Connection > SSH > X11" (left side panel), and check the box  "Enable X11 forwarding". If you save this configuration to your session, you only need to do this once.

```{image} ../images/Putty_X11.png
:height: 400px 
```
<p>

If Xming is active, you will see its' symbol in your taskbar.

#### WinSCP

WinSCP allows transferring files from your local system (e.g., laptop) to the cluster or vice-versa. You can download it <a href="https://winscp.net/eng/download.php" target="_blank">here</a>.

When you open WinSCP you need to connect to a "New site". You will need to fill in the "Host name", "User name", and "Password". Jureca host name is `jureca.fz-juelich.de`. Juwels host name is `juwels.fz-juelich.de`.

When you press "Login", you will be prompted to type in your passphrase for the SSH key that you created previously.

```{image} ../images/winSCP.png
:height: 300px
``` 
<p>

After that, you will see two panels. To the left is your local system and to the right the JSC system. Simply drag a file or folder to transfer it from one system to the other.

## Setting up eCLM

Once you created a JSC account and have access to a compute time project, follow these steps which will guide you on how to download and build eCLM on a JSC system. This guide involves four major steps:

1. Prepare the environment
2. Download eCLM
3. Build eCLM
   - Loading dependencies
   - Configuring build settings
   - Building eCLM
4. Verifying that eCLM works

Begin by logging in to the JSC system on your local machine using the ssh key.
(Windows users: open a terminal with Putty)

For juwels for example do this:

```sh
ssh -X -i ~/.ssh/id_ed25519 user1@juwels.fz-juelich.de # replace user1 with your JuDoor username!
```

### Step 1: Prepare the environment

First, if not already done, you will create your own folders within the `project1` and `scratch` directories of your compute project on the supercomputer.

```sh
# Check your projects and select a compute project with a non-empty 'budget-accounts'. Use it to replace projectID below! 
jutil user projects -u $USER

# Activate your project
jutil env activate -p projectID

# Create folders
MYPROJECT="$PROJECT/$USER"
MYSCRATCH="$SCRATCH/$USER"
mkdir -p $MYPROJECT $MYSCRATCHK
```

### Step 2: Prepare the environment

Navigate to your `$MYPROJECT` directory and clone the <a href="https://github.com/HPSCTerrSys/eCLM" target="_blank">eCLM repository</a> from Github. Next you will navigate into the main model folder and set the `eCLM_ROOT` environment variable.

```sh
# Clone eCLM Github repository
cd $MYPROJECT
git clone https://github.com/HPSCTerrSys/eCLM.git

# Navigate into eCLM folder and export environment variable
cd eCLM
eCLM_ROOT=$(pwd)
```
### Step 3: Build eCLM

#### Loading dependencies

Next, you need to load the software libraries required by eCLM. This is important as eCLM would fail to build nor run without knowing the location of its dependencies on the supercomputer. As this step needs to be done each time you start a new session, it is convenient to create a shell script that automates this step. Run this command to create a shell script named `load-eclm-variables.sh` in your `$HOME` directory:

```sh
cat << EOF > $HOME/load-eclm-variables.sh
```

Then copy the following in the shell file:
```{attention}
Before you copy, replace 'projectID' with your compute project!
```

```sh
#!/usr/bin/env bash

# Activate compute project
jutil env activate -p projectID

# Set helper variables
MYPROJECT=${MYPROJECT}
MYSCRATCH=${MYSCRATCH}
eCLM_ROOT=${eCLM_ROOT}

# Load eCLM dependencies
module load Stages/2024
module load Intel
module load ParaStationMPI
module load netCDF
module load netCDF-Fortran
module load PnetCDF
module load imkl
module load Python
module load Perl
module load CMake

# Display environment variables
module li
echo MYPROJECT=${MYPROJECT}
echo MYSCRATCH=${MYSCRATCH}
echo eCLM_ROOT=${eCLM_ROOT}

# Navigate into eCLM model folder
cd $eCLM_ROOT
EOF
```

Now, source the environment file by running:

```sh
source $HOME/load-eclm-variables.sh
```

You should get an output similar to this one:

```{figure} ../images/load_env.png
:height: 400px
```
<p>

#### Configuring build settings

eCLM is built using the CMake build system. Initially, you need to pass some build settings to `cmake`, such as which C/Fortran compilers to be used and the location of the install folder. This is accomplished by running the following commands:

```sh
# Set variables
BUILD_DIR="${eCLM_ROOT}/build"
INSTALL_DIR="${eCLM_ROOT}/install"

# CMake configure step
cmake -S "${eCLM_ROOT}/src"                    \
      -B "${BUILD_DIR}"                        \
      -D CMAKE_INSTALL_PREFIX="${INSTALL_DIR}" \
      -D CMAKE_BUILD_TYPE="RELEASE"            \
      -D CMAKE_C_COMPILER=mpicc                \
      -D CMAKE_Fortran_COMPILER=mpifort
```

#### Building eCLM

Finally, you can build eCLM. The commands below should take approximately 15-20 minutes to finish.

```sh
cmake --build "${BUILD_DIR}" && cmake --install "${BUILD_DIR}"
```

### Step 4: Verify that eCLM works

You can check if eCLM has been properly installed. The following command will display a directory tree showing the eCLM executable `eclm.exe` and library files in the `lib` directory:

```sh
tree $eCLM_ROOT/install
```
You should get something similar to:

```{figure} ../images/eclm_build.png
:height: 300px
```
<p>

**Congratulations!** You have successfully built and installed eCLM.