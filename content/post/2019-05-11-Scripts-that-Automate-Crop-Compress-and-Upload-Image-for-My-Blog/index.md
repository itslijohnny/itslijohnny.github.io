---
title: Automate Image Processing for My Blog
date: 2019-05-11 22:28:30
tags:
  - Python
  - Automation
  - API
  - Tinypng
  - SM.MS
  - Blog
  - Automator
categories:
  - Blog
  - Python
keywords: python,automation,api,tinypng,SM.MS,blog,automator
description: This is an introduction to my Python Script that automates image processing. 
image: 5cd7b069e734a.jpg

---

>:warning:The old cript is `DEPRECATED`. I switch to FastAPI, and updated the code [here](https://github.com/itslijohnny/blog-image-processing-automation). The old code is now in [v1.0 Branch](https://github.com/itslijohnny/blog-image-processing-automation/tree/V1.0).  

As you can see, my blog contains cover images. Every time I write an article I need to upload a cover image to the image server. However, the process is complicated and trivial. I need to crop the image to a certain proportion and resize and compress the image to reduce the loading time. Moreover, to put the photographer's name on the image, I need to use other software. Therefore, I create two python scripts to automate the process.
<!--more-->

> For more information and code script, please go to my [GitHub page](https://github.com/itslijohnny/blog-image-processing-automation/tree/V1.0).

These scripts are for automating the process of cropping, resizing, adding author's information, compressing, and uploading an image.



- The compressing service I use [tinypng](https://tinypng.com)
- The storage for image I user [sm.ms](https://sm.ms/)
- This script works **only** for the image download from [unsplash.com](https://unsplash.com/)

## Usage

To use correctly, you need to create an `api.txt` file that contains only the API key for  [tinypng](https://tinypng.com). To generate an API key, you can check [https://tinypng.com/developers](https://tinypng.com/developers).

`main.py` can be easily run in the terminal with the command:

```Bash
python main.py
```

Once it launched, you can drag and drop any image on it.

`automator.py` can be used in Mac's Automator. By building a server with Automator, I can right click on any image and run the script, or use a shortcut to run the script.

