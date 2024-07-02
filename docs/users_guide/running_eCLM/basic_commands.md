# Basic commands to run eCLM

Begin by logging in to the JSC (or another) system. Then, source the eCLM environment file.

```sh
source load-eclm-variables.sh
```

You can create a folder called `cases` or similar in your main eLCM directory in which you create a directory for your new case.

```sh
mkdir -p cases/"your case name"
```

For the moment, copy the namelists from one of the test cases to use as a starting point for your new case.

```sh
cd "your case name"
cp ../"testcase"/. .
```

In the next step, you will customize the namelist files to your new case.










