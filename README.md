# EmoSleep
Python scripts for the analysis of EmoSleep project's data

## Install python environment
In order to have a working environment to run this scripts, I advice to use
the resources in the 'env' path. Here an easy tutorial:

### Step 1 - download and install miniconda
Miniconda is the light version of anaconda and it doesn't require admin 
priviledges to be installed.
The aim of this toolbox is to easily manage python environments. 
It will automatically create a 'base' python environment (usually the latest 
version), then the user can create customized environments containing the 
disired python version and the needed libraries. 

You can find the latest version of miniconda <a href="https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links" target="_blank">here</a>.
Read the terms, accept all, keep the recommended position for the installation, and at last confirm the **automatic configuration**.
Once the installation is complete it would be better to restart the user session or to write in a new terminal (just for unix systems):

> source .bashrc

### Step 2 - create a new environment
We need to have an environment with a specific version of python in order to avoid compatibility issues. Thus, we will create a new environment using a .yml file that contains all the information needed to have a uniform set of variables. 

In this specific case we will use the **py310.yml** file contained in the env folder.

Open a new terminal and write:

> conda env create -f \<path to py310.yml>

Once it finishes without errors, close the terminal and re-open it.
Now you should be able to activate the new environment writing:

> source activate py310

or

> conda activate py310

In order to **come back to the base environment** you can type:
> conda deactivate

Other information about environment creation can be found [here](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#).

### Step 3 - install libraries
Now we need to install libraries, i.e. the toolboxes containing all the classes and functions used to perform a specific programming task (e.g. array managing is performed by the numpy library).

In order satisfy all the dependences (i.e. the needed library to execute the scripts) we are going to install a set of libraries using **pip** and the **pip_libs.txt** file contained in the env folder.

Open a new terminal and write:

> source activate py310 
> 
> pip install -r \<path to pip_libs.txt>

Once it finishes you would be able to use this set of libraries in your python environmen. You can check your environment libraries writing:

> pip freeze

### Step 4 - install this toolbox
In order to use scripts and functions of this toolbox, we need to add it to our libraries list. To do so open a terminal in the emosleep folder and type:

> source activate py310
>
> python setup.py develop

From now on you can import emosleep in your python scripts and use its functions.