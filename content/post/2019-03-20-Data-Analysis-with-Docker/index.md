---
title: Data Analysis with Docker
date: 2019-03-20T02:02:28.828Z
tags: 
    - Docker
    - Tutorial
    - Jupyter Notebok
categories:
  - Data
  - Dev Env
image: 5cc38cc0066e1.jpg
description: Data Analysis is not all about reports or visualization. The correctness and reproducibility are also important for scientific research. A consistent environment is critical for reproducibility. There are several ways to achieve that. However, I find out using Docker at any time can repeat the experiment in the same environment. It is easy to scale up and scale horizontally. 
---

Data Analysis is not all about reports or visualization. The correctness and reproducibility are also important for scientific research. A consistent environment is critical for reproducibility. There are several ways to achieve that. However, I find out using [Docker]((https://www.docker.com/why-docker)) at any time can repeat the experiment in the same environment. It is easy to scale up and scale horizontally.

<!-- more -->

My docker image is based on Ubuntu. It includes common Data Science tools such as Jupyter Notebook wiht Python 3 and R kernel. With the help of R Magic,  I can run both Python and R in the same .ipynb file.  To learn more about R Magic, you can click [here](https://www.datacamp.com/community/blog/jupyter-notebook-r?utm_source=adwords_ppc&utm_campaignid=1565261270&utm_adgroupid=67750485268&utm_device=c&utm_keyword=&utm_matchtype=b&utm_network=g&utm_adpostion=1t1&utm_creative=295208661496&utm_targetid=dsa-473406574235&utm_loc_interest_ms=&utm_loc_physical_ms=9033309&gclid=EAIaIQobChMIt5Xy39jq4AIVbiCtBh3FdQ4IEAAYASAAEgLEZ_D_BwE).
I also installed Nbextensions for Jupyter Notebook.  For more information, you can click [here](https://github.com/ipython-contrib/jupyter_contrib_nbextensions)


> You can find my Dockerfile in my [GitHub Repository](https://github.com/itslijohnny/data-analyst-notebook-docker).

## HOW TO USE MY DOCKERFILE


### Install Docker
The Docker community have an explicit tutorial about how to install Docker. Please check [here](https://www.docker.com/community-edition#/download)


### Build

In the terminal, direct to the folder that contains the dockerfile and run the following command:
```sh
docker build -t data-analyst-notebook .
```
Don't forget the "." at the end. data-analyst-notebook is the name of the image. You can change to whatever you prefer.

### Start server
I use following code to start server:
```sh
docker run --rm -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes -v ~/:/home/jovyan/work data-analyst-notebook
```
There is more detailed instruction from [User Guide on ReadTheDocs](https://jupyter-docker-stacks.readthedocs.io/en/latest/)

If you feel like that the command is too long to run. You can add an alias to your .bashrc file like this:
```sh
alias dslab='docker run -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes -v ~/:/home/jovyan/work data-analyst-notebook'
```
Now you can use ```dslab``` in the terminal as a replacement for typing the long command.
