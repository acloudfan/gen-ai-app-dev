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



# Jupyter lab checkpoint files
To disable the generation of the checkpoint file, set the following in the configuration file. This file is available under the .jupyter folder for the user.

c.FileContentsManager.checkpoints = false

If you don't find the file, use the following command to generate it.

jupyter lab --generate-config