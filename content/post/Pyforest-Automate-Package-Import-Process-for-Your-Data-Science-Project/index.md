---
title: Pyforest - Automate Package Import Process for Your Data Science Project
description: A tool can speed up your data analysis
author: Johnny Li
date: 2021-03-19T19:56:44-07:00
tags:
    - Python
    - Data Analysis
    - Data Science
    - Jupyter
    - Jupyter Notebook
    - Jupyter Lab
    - import
    - Library
    - Package
    - Pyforest
    - Cookiecutter
    - Automation
    - Workflow
categories:
    - Blog
    - Python
    - Tutorial
keywords: python, data analysis, data science, jupyter, ipython, jupyter lab, jupyter notebook, import, library, package, pyforest, cookiecutter, automation, workflow
image: j4dzCfs1YINnUeP.jpg
math: false
license: 
hidden: false
mermaid: false
---

Usually, the first step we all do for any Python project is importing required packages. So, the beginning of the file usually looks like this: 

```python
import xxxx as xxx
from xxxx import xxxx
```

Importing packages is one of my least favorite parts when I'm working on a Data Scientist project. Packages like *pandas*, *numpy*, *lighteda*,  *matplotlib.pyplot*, and *seaborn* are commonly used for my projects. I need to repeat this step in every single Jupyter Notebook. Moreover, when the analysis/research dives deeper, and I need to import new packages in the middle, I have to go back to the beginning and import new packages (If you are using Jupyter Notebook, don't forget to press `Ctrl` + `Enter`).


![Import in the middle. ](https://i.loli.net/2021/03/20/mle46dnAb8zsr1K.gif)
{{<cap 
"Going back and forth to import packages is frustrating."
>}}


I can reduce some repetitive works by using template tools like cookiecutter.  

{{<github "itslijohnny/cookiecutter_data_analysis">}}


But, is there a way to automatically import related packages and add import statements for me, like this?
![](https://github.com/8080labs/pyforest/raw/master/examples/assets/pyforest_demo_in_jupyter_notebook.gif)
{{<cap 
"The packages are automatically imported in the first cell."
>}}

But how? **Pyforest** - a package can automatically import packages for you.
{{<github "8080labs/pyforest">}}

Pyforest can "lazy" import the packages and add the import statement to your Jupyter Notebook. It will not import packages you are not using. 

You can install it using pip:
```shell
pip install --upgrade pyforest
python -m pyforest install_extensions
```

The installation will add pyforest_autoimport.py to your Jupyter and IPython default startup settings. Therefore, you can start coding in Jupyter or Ipython and don't need to import pyforest.

![I didn't add the statement for import pandas as pd.](pyforestdemo.png)

Also, you can notice that I didn't type the full name of pandas library. Pyforest has already included all the common abbreviations.
![Pyforest includes many import statements.](sourcecode.png)

You can also edit  ~/.pyforest/user_imports.py to add your customized import statements.

![](user_imports.png)

Pyforest works better on Jupyter Notebook or IPython. If you want this feature to work in other editors, you can import Pyforest first. e.g.
```python
import pyforest
pyforest.active_imports()
```

This is my daily dose of Python tricks. I hope this post can help you. I strongly recommend you try [cookiecutter](https://github.com/itslijohnny/cookiecutter_data_analysis) and [Pyforest](https://github.com/8080labs/pyforest) to automate your Data Science/Analysis workflow.

------------------------
{{<fin "pyforest-automate-package-import-process-for-your-data-science-project" "Pyforest - Automate Package Import Process for Your Data Science Project">}}

------------------------