# -*- coding: utf-8 -*-
"Script to process raster data"
#libs
import rasterio
import os
import re

#paths
baseDir = "E:\GIS-Datenbasis\Sentinel2_Schweden"
dataDir = os.path.join(baseDir, "S2A_MSIL2A_20230208T103211_N0509_R108_T34VCR_20230208T133552\S2A_MSIL2A_20230208T103211_N0509_R108_T34VCR_20230208T133552.SAFE\GRANULE\L2A_T34VCR_A039859_20230208T103205\IMG_DATA\R10m")
stackDir = os.path.join(baseDir, "rasterStack.tif")

#list data
dataList = os.listdir(dataDir)
#join path
dataList = [os.path.join(dataDir, i) for i in os.listdir(dataDir)]

#retrieve metadata from one of the raster files
with rasterio.open(os.path.join(dataDir, dataList[0])) as rasterMeta:
    meta = rasterMeta.meta

#update to 3 layers
meta.update(count = 3)

#creating a raster stack
with rasterio.open(stackDir, "w", **meta) as rasterStack:
    #iterate over bands using enumerate -> returns elements in the form of
    # (1,band1), (2,band2)... which allows retrieving the index number and the 
    # element itself for processing (see how "id" and "layer" is used)
    for id, layer in enumerate(dataList, start=0):
        print(id, layer)
        ##rgb bands of sentinel 10m resolution product are band 3 (red), 4 (green) and
        # 5 (blue), thus only the band 2 to 4 should be included
        if re.search(".*B0[2-4]_10m.jp2",os.listdir(dataDir)[id]):
            with rasterio.open(layer) as rasterLayer:
                rasterStack.write_band(id, rasterLayer.read(1))