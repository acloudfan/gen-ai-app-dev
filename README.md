# Generative AI application design & development
This repository is part of a *highly structured* course that is primarily geared towards teaching the fundamentals of generative AI to application developers. Course assumes that learner has no prior experience with machine learning. 

## Interested in more information?

Checkout the course intro video on YouTube:

https://www.youtube.com/watch?v=Tl9bxfR-2hk

Check out the online course guide:

https://genai.acloudfan.com/

Check out free preview lessons on UDEMY:

https://www.udemy.com/course/generative-ai-app-dev/?referralCode=C255776F230F790E3ED4

Check out free preview lessons on my portal:

https://courses.pragmaticpaths.com/p/generative-ai-application-design-and-devlopement




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