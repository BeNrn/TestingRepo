# -*- coding: utf-8 -*-
"""
Purpose:    Script to process raster data.
Created:    26.02.2024
Author:     BeNrn
"""

#import libs
#------------
import rasterio
import os
import re
from rasterio.plot import show  
import matplotlib.pyplot as plt
import numpy as np
from rasterio.plot import show_hist
                
#Function to normalize the grid values
#--------------------------------------
def normalize(array, minGlobal, maxGlobal):
    """Normalizes numpy arrays into scale 0.0 - 1.0"""
    #array_min, array_max = array.min(), array.max()
    return ((array - minGlobal)/(maxGlobal - minGlobal))

#set paths
#---------
baseDir = "D:\GIS-Datenbasis\Europa\Sentinel2_Schweden"
dataDir = os.path.join(baseDir, "S2A_MSIL2A_20230208T103211_N0509_R108_T34VCR_20230208T133552.SAFE\GRANULE\L2A_T34VCR_A039859_20230208T103205\IMG_DATA\R10m")
stackDir = os.path.join(baseDir, "rasterStack.tif")

#collect data
#-------------
#list data
dataList = os.listdir(dataDir)
#join path
dataList = [os.path.join(dataDir, i) for i in os.listdir(dataDir)]

#process meta data
#-----------------
#retrieve metadata from one of the raster files
with rasterio.open(os.path.join(dataDir, dataList[0])) as rasterMeta:
    meta = rasterMeta.meta

#update to 3 layers
meta.update(count = 3)

#creating a raster stack
#------------------------
#set id of layers to 1 as expected by rasterio
i = 1
with rasterio.open(stackDir, "w", **meta) as rasterBand:
    #iterate over bands using enumerate -> returns elements in the form of
    # (1,band1), (2,band2)... which allows retrieving the index number and the 
    # element itself for processing (see how "id" and "layer" is used)
    for id, layer in enumerate(dataList, start=0):
        ##rgb bands of sentinel 10m resolution product are band 3 (red), 4 (green) and
        # 5 (blue), thus only the band 2 to 4 should be included
        if re.search(".*B0[2-4]_10m.jp2$",os.listdir(dataDir)[id]):
            print(id, i, layer)
            with rasterio.open(layer) as rasterLayer:
                rasterBand.write_band(i, rasterLayer.read(1))
            i+=1

#visualizations, normalizations, histograms
#-------------------------------------------
with rasterio.open(stackDir, "r") as rasterImage:
    #print(rasterImage.transform)
    #print(rasterImage.crs)
    
    #only using part of the raster for quicker processing
    band1 = rasterImage.read(1)[0:500, 0:500]
    band2 = rasterImage.read(2)[0:500, 0:500]
    band3 = rasterImage.read(3)[0:500, 0:500]
    
    minList = (band1.min(), band2.min(), band3.min())
    minGlobal = min(minList) 
    maxList = (band1.max(), band2.max(), band3.max())
    maxGlobal = max(maxList) 
    
    #normalization
    nb1 = normalize(array = band1, minGlobal = minGlobal, maxGlobal = maxGlobal)
    nb2 = normalize(array = band2, minGlobal = minGlobal, maxGlobal = maxGlobal)
    nb3 = normalize(array = band3, minGlobal = minGlobal, maxGlobal = maxGlobal)
    
    plt.imshow(np.dstack(tup = (nb1, nb2, nb3)))
    
    #https://github.com/OSGeo/gdal/issues/5736
    #show_hist(rasterImage, bins=50, lw=0.0, stacked=False, alpha=0.3,
    #      histtype='stepfilled', title="Histogram")
    
    #show one layer
    plt.imshow(rasterImage.read(2))
    show(rasterImage)

#histogram
plt.hist(band1.flatten(), bins = 50, fc=(1, 0, 0, 0.5)) #color and opacity (Red, Green, Blue, A = opacity)
plt.hist(band2.flatten(), bins = 50, fc=(0, 1, 0, 0.5))
plt.hist(band3.flatten(), bins = 50, fc=(0, 0, 1, 0.5))

#sources:
# normalization: https://python.plainenglish.io/how-to-normalize-a-raster-image-via-python-and-gdal-7238d0e2140f
# others:        https://earthpy.readthedocs.io/en/latest/gallery_vignettes/plot_rgb.html