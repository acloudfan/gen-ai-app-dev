# generative-ai-for-architects
This is a collection of code artifacts for learning generative AI


# FAQ:

1. Setup Jupyter Lab in Anaconda virtual environment

Note - if not installed the option for "Jupyter" will not be available in Anaconda

```
conda install jupyter
conda install jupyterlab
```

2. PlantUML preview not working on Windows/Visual Studio

* Install Java Runtime
* Install GraphViz https://plantuml.com/graphviz-dot

3. I am getting the following warning in Notebook?

```
TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html  from .autonotebook import tqdm as notebook_tqdm
```

pip install jupyter --upgrade

4. I am unable to delete files from hugging face cache?

It generally means that you have something using the cached object/file. 

* Close all finder windows
* Shutdown the Jupyter lab using

```
jupyter notebook list
```

# Change the port number using the command above

```
jupyter notebook stop  8888
```

# List packages in your conda environment
conda list -e > requirements.txt

# Jupyter lab checkpoint files
To disable the generation of the checkpoint file, set the following in the configuration file. This file is available under the .jupyter folder for the user.

c.FileContentsManager.checkpoints = false

If you don't find the file, use the following command to generate it.

jupyter lab --generate-config


#################
## Package List #
#################

# python-dotenv-1.0.1
pip install python-dotenv

# langchain-core=0.2.29=pypi_0
pip install langchain

# langchain_community-0.2.11
pip install langchain_community

# langchain_openai-0.1.20 
pip install langchain_openai

# anthropic-0.32.0
pip install langchain_anthropic

# google-generativeai-0.7.2
pip install langchain_google_genai==0.7.2

# 