# -*- coding: utf-8 -*-
"""
Purpose:    Most used packages.
Created:    22.02.2024
Author:     BeNrn
"""
#import libs
import os

#set paths
basePath = r"C:\Users\tamta\Documents\KnowHow\Geoinformatik\Repositories"
#basePath = r"C:\Users\tamta\Documents\KnowHow\Geoinformatik\Repositories\KnowHowBase\R"

fileList = []

for root, dirs, files in os.walk(top = basePath, topdown = True):
    # print(root)
    # print(dirs)
    # print(files)
    for file in files:
        fileList = fileList + [os.path.join(root, file)]
    
scriptList = [i for i in fileList if i.split(".")[-1] in ("py", "ipynb")]

for script in scriptList:
    open()