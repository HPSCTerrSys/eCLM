Installation
============

.. code:: bash

    cd /path/to/eCLM/namelist_generator
    pip install --user .

Usage
=====

.. code:: bash

    $ clm5nl-gen -h
    clm5nl-gen - CLM5 namelist generator

    Generates CLM5 namelists from  model parameters file and saves
    the outputs to a specified directory. If no directory is
    specified, the namelists are saved to the current directory.

    Usage: 
    clm5nl-gen [--out DIR] PARAMFILE
    clm5nl-gen (-h | --help)
    clm5nl-gen (-v | --version)

    Arguments:
    PARAMFILE           model parameters file (.toml)

    Options:
    -o DIR --out DIR    Save generated namelists to this directory.
    -h --help           Show this screen.
    -v --version        Show version.