# JSC

The following section will explain the necessary steps to download the model from the official repository and get eCLM to run on JSC machines ([Juwels](https://www.fz-juelich.de/en/ias/jsc/systems/supercomputers/juwels) or [Jureca-DC](https://www.fz-juelich.de/en/ias/jsc/systems/supercomputers/jureca)).


## Prerequisites for JSC users

Before building and running eCLM on JSC machines, the following prerequisites should be fulfilled:

* Create a JSC/JuDoor account
* Join a compute time project
* Login to JSC Gitlab account
* Logging in to JSC machines


### Create a JSC/JuDoor account

You need a JSC account to access the HPC system. For that, you first need a JuDoor account for which you can register [here](https://judoor.fz-juelich.de/register).

Enter your e-mail address and click on "Send confirmation mail".

Afterwards, you will receive an e-mail from dispatch@jsc.de with a personalized link. Click on the link and fill in the form with your data.

Submit the form.

With this, the creation of your JSC account is completed. Now, you can log in to your [JuDoor account](https://judoor.fz-juelich.de/login) with your username and password:


### Join a compute time project

Log in to your JuDoor account. Join the compute time project you were assigned to. Under "Projects", choose "+ Join a project":

Enter the project id. You can also add some additional information. Then you can join the project.

The PI/PA will be automatically informed about your join request and can add you to the different systems available in the project. Once you are approved to join the project compute time, you should be able to see the project id under "Projects".


### Login to eCLM-JSC Gitlab account

If you are a user in IBG-3 and want to run eCLM on the JSC machines, you can log in to the [eCLM-JSC](https://icg4geo.icg.kfa-juelich.de/ModelSystems/clm/eCLM_scripts) Gitlab repository with your JSC account. This is where we will download the model from in the next section "Setting up eCLM".


### Logging in to JSC machines

To log in to one of the JSC machines you need a JSC account and access to a compute time project (see above).

The final step is to create and upload an SSH key for your account and local machine.

JSC provides thorough instructions for [Juwels](https://apps.fz-juelich.de/jsc/hps/juwels/access.html#openssh-key-generation) and [Jureca](https://apps.fz-juelich.de/jsc/hps/jureca/access.html#openssh-key-generation) on how to generate and upload SSH keys.


### Additional information on JSC machines

For the full user documentation regarding the JSC systems check:

* [Juwels documentation](https://apps.fz-juelich.de/jsc/hps/juwels/index.html)
* [Jureca documentation](https://apps.fz-juelich.de/jsc/hps/jureca/index.html)

### Additional software for windows users

#### Xming

Xming allows Windows machines to display a graphical Linux program which is running on a remote Linux server. You can download Xming [here](http://www.straightrunning.com/XmingNotes/).

To enable Xming in the PuTTY configuration, navigate to "Connection > SSH > X11" (left side panel), and check the box  "Enable X11 forwarding". If you save this configuration to your session, you only need to do this once.

```{image} ../images/Putty_X11.png
:height: 400px
:name: fig1
```
<p>

If Xming is active, you will see its' symbol in your taskbar.

#### WinSCP

WinSCP allows transferring files from your local system (e.g., laptop) to the cluster or vice-versa. You can download it [here](https://winscp.net/eng/download.php).

When you open WinSCP you need to connect to a "New site". You will need to fill in the "Host name", "User name", and "Password". Jureca host name is `jureca.fz-juelich.de`. Juwels host name is `juwels.fz-juelich.de`.

When you press "Login", you will be prompted to type in your passphrase for the SSH key that you created previously.

```{image} ../images/winSCP.png
:height: 300px
:name: fig2
``` 
<p>

After that, you will see two panels. To the left is your local system and to the right the JSC system. Simply drag a file or folder to transfer it from one system to the other.

## Setting up eCLM

Once you created a JSC account and have access to a compute time project, follow these steps which will guide you on how to download, build, and install eCLM on a JSC system. This guide involves four major steps:

1. Download eCLM
2. Prepare the environment
3. Build eCLM
4. Verify that eCLM works correctly

Begin by logging in to the JSC system on your local machine using the ssh key.
(Windows users: open a terminal with Putty)

For jureca for example do this:

```sh
ssh -X -i ~/.ssh/id_ed25519 user1@jureca.fz-juelich.de # replace user1 with your JUDOOR username!
```


### Step 1: Download eCLM

Navigate to your compute project under `/p/project1/"your_project_name"` and create a directory with your name. Then clone the eCLM repository from https://icg4geo.icg.kfa-juelich.de/ModelSystems/clm/eCLM_scripts. Navigate into the main model folder and set the `eCLM_ROOT` environment variable.

```sh
git clone --recurse-submodules https://icg4geo.icg.kfa-juelich.de/ModelSystems/clm/eCLM_scripts.git

cd eCLM_scripts
eCLM_ROOT=$(pwd)
```
### Step 2: Prepare the environment

In order to run eCLM you need to load the right software libraries required by the model. You can do this by sourcing the environment file that is located in the main model folder.

```sh
source eclm.loadmodules.env
```

### Step 3: Build eCLM

Now you can build eCLM. The command below should take approximately 15-20 minutes to finish.

```sh
./eclm.build
```
 
### Step 4: Verify that eCLM works correctly

In order to check if eCLM has been properly installed, run the following command to see if the eCLM executable and library files are present:

```sh
tree $eCLM_ROOT/install
```

You should get something similar to:

```sh
/p/project/"your_project_name"/"your_username"/eCLM/install
├── bin
│   └── eclm.exe
└── lib
    ├── libclm.a
    ├── libcsm_share.a
    ├── libdatm.a
    ├── libesp.a
    ├── libglc.a
    ├── libgptl.a
    ├── libice.a
    ├── libmct.a
    ├── libmosart.a
    ├── libmpeu.a
    ├── libocn.a
    ├── libpio.a
    └── libwav.a
```