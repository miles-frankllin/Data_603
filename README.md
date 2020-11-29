# Contributers
- Miles Franklin
    - UMBC
    - Data Science 603 
    - Dr. Waleed Youssef
    - 11/28/2020

# Goal and Overview
The goal of this project is to develop a machine learning model to identify whether or not an individual is wearing a face mask. The data used in this model was scraped from [Shutter Stock Photos](https://www.shutterstock.com) and stored in a series of a MongoDB collections. Additionally, we were hoping to implement our model to perform predictions on a real time camera feed, although this has been left for a Future Direction.

# Motivation
This initial motivation of this project was to scrape Google Images for portraits by race, with the goal of creating a machine learning model that would be able to identify the race of an individual with a fair degree of accuracy. We quickly realized that there were several factors that we did not initially take into consideration, namely, the limited storage space provided from MongoDB, and the complexity of classifying images between a total of 6+ groups. Hence, we transitioned from a multi-classification problem to the binary classification presented here.

# Background
The United States is struggling to contain the spread of Covid-19 in large part to the debate over the need or efficacy of wearing masks. While that debate is not entertained in this project, we aimed to create a tool that could be useful in this divided environment. 

# Navigation
[Web Scraping File](https://github.com/miles-frankllin/Data_603/blob/main/main.py) -
[Web Scraping Site](https://www.shutterstock.com) <br>
[Mask Classification (Tree)]() <br>
[Mask Classification (CNN)](https://github.com/miles-frankllin/Data_603/blob/main/Mask_Classification_CNN.ipynb) - 
[Human Collaboration (CNN)](https://github.com/miles-frankllin/Data_603/blob/main/Human_Collaboration/Human_Collaboration.ipynb)


# Requirements
<pre>
Languages               : Python 3.8.3
Tools/IDE               : Anaconda
Libraries (UI)          : IPython
Libraries (Web Scraping): requests, bs4, time, urllib, simplejson
Libraries (Images)      : pickle, PIL, json, pymongo, skimage, bson,
                          os, shutil, errno, io
Libraries (ML and Other): pandas, matplotlib, numpy, scipy, sklearn,
                          random, sklearn, tensorflow, keras_preprocessing
</pre>



# Data Source: Base Site for Web Scraping
<pre>
URL            : https://www.shutterstock.com
Limitations    : With the techniques used, can only scrape 20 images per page,even though there are many more.
Concerns       : N/A
</pre>


# Future Directions
- Move Notebooks into Google Colab to make use of servers with available GPU’s
    - GPU’s are designed to process image data and can greatly improve runtime
- Import larger datasets to train on
    - 12,000 image dataset of faces with and without masks ([Kaggle](https://www.kaggle.com/ashishjangra27/face-mask-12k-images-dataset))
    - 5,00 image dataset of faces without masks ([Kaggle](https://www.kaggle.com/jeffheaton/glasses-or-no-glasses)) 
- Transfer Learning: Find a similar project to build on top of rather than building from scratch
- Learn to use real time camera feed for model deployment
- Improve upon web scraping techniques
    - Google Images
    - Webdrivers (Selenium)
- Need a better understanding of Neural Network layers, so that we can design a meaningful architecture of our own
