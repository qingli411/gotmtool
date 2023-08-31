# gotmtool

Python tools to work with [GOTM](https://gotm.net).

----

# Quick Start

## Create the conda environment

```bash
$ conda env create -f environment.yml
```

This creates an environment from `environment.yml`. The name of the environment is "`gotm`", as can be seen by inspecting the `environment.yml` (this is also printed in the terminal after the environment is created / installed):

```yaml
name: gotm
channels:
  - conda-forge
dependencies:
  - python=3.9
  - gfortran=11
  - netcdf-fortran
  - cmake
  - xarray
  - scipy
  - ruamel.yaml
  - jupyter
  - notebook
  - matplotlib
  - pip
```

Creating the environment downloads and installs packages, and this takes some time.

## Activate the environment

```bash
$ conda activate gotm
```

## Run `gotm_env_init.py` to setup the directory structure and download gotm files (source code, input data, compiled build, executable)

```bash
python gotm_env_init.py
```

Running this script will initiate a series of prompts about yaml file names, directory names, and clone requests to github that must be answered to install and compile gotm.

Note: if you attempt to run `gotm_build.py` before `gotm_env_init.py`, you will receive an error

```
ERROR: GOTM environment file '.gotm_env.yaml' not found
  Please run gotm_env_init.py to set it up
```

## Run `gotm_build.py` to compile gotm

```bash
$ python gotm_build.py
```

You can also skip this step here and compile gotm when setting up the test case in Jupyter notebook. Please see the notebooks in `./examples` for a few examples.
