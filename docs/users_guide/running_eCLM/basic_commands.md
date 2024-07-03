# Basic commands to run eCLM

Begin by logging in to the JSC (or another) system. Then, source the eCLM environment file.

```sh
source load-eclm-variables.sh
```

You can create a folder called `cases` or similar in your main eCLM directory in which you create a new directory for every new case.

```sh
mkdir -p cases/"your case name"
```

For the moment, copy the namelists from one of the test cases to use as a starting point for your new case.

```sh
cd cases/"your case name" # replace with your case name
cp ../../test_cases/"test case"/. . # replace with the name of the test case
```

In the next step, you will customize the namelist files to your new case.










