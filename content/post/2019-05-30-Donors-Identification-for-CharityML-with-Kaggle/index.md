---
title: Donors Identification for CharityML
date: 2019-05-30 01:03:50
tags:
    - Machine Learning
    - SGDClassifier
    - AdaBoostClassifier
    - LogisticRegression
    - Python
    - Udacy
categories:
  - Data Analysis
  - Python
keywords: Machine Learning,SGD Classifier,AdaBoost,Logistic Regression,Python
description: A project of using Machine Leaning to identify potential donors.
image: 5cef9192b167778174.jpg
---
[![](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://lijohnny.com)  [![](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)  [![](https://img.shields.io/badge/Kaggle-Project-blue.svg)]() 

In this project, I built machine learning models that best identifies potential donors for CharityML(a fictitious charity organization) with data collected for the U.S. census. To find the best approach, I performed EDA, feature engineering, and building training and predicting pipeline to evaluate and optimize the performance between different machine learning models.

The modified census dataset consists of approximately 32,000 data points, with each datapoint having 13 features. This dataset is a modified version of the dataset published in the paper *"Scaling Up the Accuracy of Naive-Bayes Classifiers: a Decision-Tree Hybrid",* by Ron Kohavi. You may find this paper [online](https://www.aaai.org/Papers/KDD/1996/KDD96-033.pdf), with the original dataset hosted on [UCI](https://archive.ics.uci.edu/ml/datasets/Census+Income).

The model I have used:
- SGD Classifier
- AdaBoost
- Logistic Regression

<!--more-->

You can see the code(iPython notebook) [here](https://github.com/itslijohnny/udacity-data-scientist-nanodegree/blob/master/Supervised/Project-CharityML/finding_donors_done.ipynb).