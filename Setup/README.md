
## https://huggingface.co/docs/transformers/installation

####################
# Install Anaconda #
####################
https://www.anaconda.com/download

## Create the environment

conda 

###############################################
# Python packages                             #
# conda list -e > requirements.txt            #
# conda config --append channels conda-forge  #
# conda install --yes --file requirements.txt #
###############################################

Note:
* That if you setup manually the sample code may have version related warnings/errors.
* It is recommended that you install package with *requirements.txt* file

# Setup Jupyter lab
conda install --yes jupyterlab jupyter

# Change this command for your platform (pytorch.org)
conda install --yes pytorch torchvision torchaudio cpuonly -c pytorch

# Install HuggingFace libraries
conda install --yes transformers huggingface_hub

# Misc
conda install --yes conda-forge::matplotlib

##########################################
# Setup Python 3.12  virtual environment #
##########################################

## Install Python 3.12

### Setup virtual environment
python -m venv dev

### Activate the virtual environment
* Open a terminal window

./dev/Scripts/activate

### Install Jupyter
In Anaconda open a terminal.

```
conda install jupyter
conda install jupyterlab
```

pip install -r ./Setup/requirements.txt


### VENV not activating
* Open a PowerShell
* Set-ExecutionPolicy Unrestricted -Force

### VENV verify the environment
pip -V

##################
# Conda commands #
##################
conda env export

conda create --name <en name> --file <env yaml>


###############
# Colab setup #
###############
!curl -H "Accept: application/vnd.github.VERSION.raw" https://raw.githubusercontent.com/acloudfan/gen-ai-app-dev/main/Setup/gcsetup.sh  > gcsetup.sh
!chmod u+x gcsetup.sh
!./gcsetup.sh

###########################
# Windows 10/11 WSL setup #
###########################

* MUST have the WSL2 version for Docker. 

Open Windows PowrShell
> wsl -l -v

To check version start wsl
$ uname -a

* Install Docker

https://docs.docker.com/desktop/wsl/



