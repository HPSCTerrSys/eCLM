# Runnning example cases

Always load the eCLM environment before creating a case. This only needs to be done once per terminal session.

```sh
source eclm.loadmodules.env
```

## 1. Specify compute project

- For JSC systems (JURECA, JUWELS, JUSUF, etc.):

```sh
jutil env activate -p cslts     #replace 'cslts' with your compute project
```

- For non-JSC systems (Levante, etc.)
```sh
export BUDGET_ACCOUNTS=aa0049   #replace 'aa0049' with your compute project
```