#script to extract information from little london map
# path: C:\Users\tamta\Documents\Freizeit\Minecraft\images\MC_Karte.tiff
# pixel size: 1268 x 924
# mc-block size: 634 x 462
# scale: 1:2

# rgb-value map

#import libs
#-----------
#basics
import geopandas as gpd
import os
import rasterio
import matplotlib.pyplot as plt
from rasterio.plot import show
import numpy as np

#supervised classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

#plotting
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches

#path
env = "C:/Users/tamta/Documents/KnowHow/Geoinformatik/Daten/Bildkarten"

#read map as RGB-raster
#----------------------
with rasterio.open(os.path.join(env, "Karte_20220415.tiff")) as baseMap: 
#baseMap = rasterio.open(os.path.join(env, "images/MC_Karte.tiff"))
    
    #map crs
    print(baseMap.crs)
    
    #map extent:
    rasterio.plot.plotting_extent(baseMap)
    
    #plot map
    #fig, ax = plt.subplots(figsize=(12,12))
    #show(mcMap, ax=ax)
    
    #plt.imshow(mcMap.read(1)) #red
    #plt.imshow(mcMap.read(2)) #green
    #plt.imshow(mcMap.read(3)) #blue
    
    #show(mcMap.read())
        
    #read landuse classification as points
    #-------------------------------------
    landUsePoints = gpd.read_file(os.path.join(env, "Karte/LandClassification.gpkg"))
    #crs
    print(landUsePoints.crs)
    # epsg:32632
    
    #plot
    #landUsePoints.plot()
    
    #plot map and points
    #--------------------
    fig, ax = plt.subplots(figsize=(12,12))
    show(baseMap, ax=ax)
    landUsePoints.plot(ax=ax, color='yellow')
    
    #add columns to points
    #--------------------
    landUsePoints["red"] = None
    landUsePoints["green"] = None
    landUsePoints["blue"] = None
    
    #extract rbg values for points
    #------------------------------
    for entry in landUsePoints.iterrows():
        #print(entry)
        #row       ... complete row with index
        #row[1]    ... values of the row
        #row[1][1] ... second value equals point geometry
        x = entry[1][1].xy[0][0]
        y = entry[1][1].xy[1][0]
        row, col = baseMap.index(x,y)
        landUsePoints["red"][landUsePoints.index == entry[0]] = baseMap.read(1)[row,col] #red
        landUsePoints["green"][landUsePoints.index == entry[0]] = baseMap.read(2)[row,col] #green
        landUsePoints["blue"][landUsePoints.index == entry[0]] = baseMap.read(3)[row,col] #blue
        #https://hatarilabs.com/ih-en/extract-point-value-from-a-raster-file-with-python-geopandas-and-rasterio-tutorial
    
    #supervised land use classification
    #----------------------------------
    #method: https://scikit-learn.org/stable/modules/cross_validation.html
    #example: #https://towardsdatascience.com/land-cover-classification-in-satellite-imagery-using-python-ae39dbf2929
    
    #extract ground truth (category = Y and pixel values = X)
    landUseArray_values = landUsePoints[["red", "green", "blue"]].to_numpy()
    landUseArray_categories = landUsePoints[["Category"]].to_numpy().ravel() #1d array expected for fitting
    
    #cross validation, hold out a part of the date to use for later performance testing (40%)
    X_train, X_test, y_train, y_test = train_test_split(landUseArray_values, landUseArray_categories, test_size=0.4, random_state=0)
    
    #k-nearest neighbor classifier
    knn = KNeighborsClassifier(n_neighbors=6)
    
    #fit to ground truth
    knn.fit(X_train, y_train)
    
    # Predict the labels of test data
    knn_pred = knn.predict(X_test)
    
    #accuracy
    print(classification_report(y_test, knn_pred))
    
    #extract map pixels for landuse estimation
    #------------------------------------------
    red_map = baseMap.read(1)
    green_map = baseMap.read(2)
    blue_map = baseMap.read(3)
    
    #flat_red_map = red_map.flatten()
    #flat_green_map = green_map.flatten()
    #flat_blue_map = blue_map.flatten()
    baseMap_array = np.array([red_map,green_map,blue_map])
    #mcMap_array_flat = np.array([flat_red_map,flat_green_map,flat_blue_map])
    
    #move axis (3 channels are now the last dimension)
    baseMap_MovedArray = np.moveaxis(baseMap_array, 0, -1)
    
    #changing the shape of the array to a long table with 3 columns
    #first argument defines the number of rows, second argument the number of
    # columns. -1 can be used to fill up the array depending on the data size (just
    # fill the array until it's full)
    # np.array([[1,2,3], [4,5,6]])
    # np.array([[1,2,3], [4,5,6]]).reshape(3,-1)
    #rows must be the values, cols must be the channels
    baseMap_FlatArray = baseMap_MovedArray.reshape(-1, 3)
    
    #prediction for total map
    karte_pred = knn.predict(baseMap_FlatArray)
    
    #reshape back to normal format is necessary
    karteMoved = karte_pred.reshape(924, -1)
    
    #replace class names  with numbers
    #classes were: 'crop', 'grass', 'house', 'path', 'rail', 'road', 'rock', 'sand', 'snow', 'tree', 'water'
    i = 1
    for element in np.unique(karteMoved):
        karteMoved[karteMoved == element] = i
        i+=1
    
    karteMoved = karteMoved.astype("float64")
    
    #plt.imshow(karteMoved)

classes = list(np.unique(karteMoved).astype('int'))
colorList = ["#d7e140", #crop
             "#1eab35", #grass
             "#d34a16", #house
             "#837671", #path
             "#000000", #rail
             "#d00000", #road
             "#4f4848", #rock
             "#c2d273", #sand
             "#ffffff", #snow
             "#07640c", #tree
             "#23158b"] #water
classNames = ['crop', 'grass', 'house', 'path', 'rail', 'road', 'rock', 'sand', 'snow', 'tree', 'water']

legendEntries = [mpatches.Patch(color=colorList[i], label="{}".format(classNames[i]) ) for i in range(len(colorList))]
# Plot newly classified and masked raster
cmap_20530 = ListedColormap(colorList)
fig = plt.figure(figsize=(9, 6))
ax = fig.add_subplot(111)
ax.margins(2)
im = ax.imshow(karteMoved, cmap = cmap_20530)
ax.set(title="Landcover classes")
ax.legend(handles = legendEntries, loc='center left', bbox_to_anchor=(1, 0.5))
ax.set_axis_off()
fig.savefig(os.path.join(env, "images/classified_map.png"), dpi = 300, bbox_inches = "tight")

#export as tiff
#---------------
#with rasterio.open(fp = os.path.join(env, "Karte_klassifiziert.tif"), 
#                   mode = "w",
#                   driver = "GTiff",
#                   height = karteMoved.shape[0],
#                   width =  karteMoved.shape[1],
#                   count = 1,
#                   dtype = np.dtype(np.float64)) as classifiedMap:
#
#    classifiedMap.write(karteMoved, 1)