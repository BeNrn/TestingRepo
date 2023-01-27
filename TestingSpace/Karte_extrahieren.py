#script to extract information from little london map
# path: C:\Users\tamta\Documents\Freizeit\Minecraft\images\MC_Karte.tiff
# pixel size: 1268 x 924
# mc-block size: 634 x 462
# scale: 1:2

# rgb-value map

#import libs
import geopandas as gpd
import os
import rasterio
import matplotlib.pyplot as plt
from rasterio.plot import show
import pandas as pd
import numpy as np

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

#path
env = "C:/Users/tamta/Documents/Freizeit/Minecraft"

#read map as RGB-raster
#----------------------
#with rasterio.open(os.path.join(env, "images/MC_Karte.tiff")) as mcMap: 
mcMap = rasterio.open(os.path.join(env, "images/MC_Karte.tiff"))

#map crs
print(mcMap.crs)

#map extent:
rasterio.plot.plotting_extent(mcMap)

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
show(mcMap, ax=ax)
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
    row, col = mcMap.index(x,y)
    landUsePoints["red"][landUsePoints.index == entry[0]] = mcMap.read(1)[row,col] #red
    landUsePoints["green"][landUsePoints.index == entry[0]] = mcMap.read(2)[row,col] #green
    landUsePoints["blue"][landUsePoints.index == entry[0]] = mcMap.read(3)[row,col] #blue
    #https://hatarilabs.com/ih-en/extract-point-value-from-a-raster-file-with-python-geopandas-and-rasterio-tutorial

#extract ground truth (category and pixel values)
landUseArray_values = landUsePoints[["red", "green", "blue"]].to_numpy()
landUseArray_categories = landUsePoints[["Category"]].to_numpy().ravel() #1d array expected for fitting

#cross validation, hold out a part of the date to use for later performance testing (40%)
X_train1, X_test1, y_train1, y_test1 = train_test_split(landUseArray_values, landUseArray_categories, test_size=0.4, random_state=0)

#k-nearest neighbor classifier
knn = KNeighborsClassifier(n_neighbors=6)

knn.fit(X_train1, y_train1)

# Predict the labels of test data
knn_pred = knn.predict(X_test1)

print(classification_report(y_test1, knn_pred))

#extract map pixels for landuse estimation
#------------------------------------------
red_map = mcMap.read(1)
green_map = mcMap.read(2)
blue_map = mcMap.read(3)

#flat_red_map = red_map.flatten()
#flat_green_map = green_map.flatten()
#flat_blue_map = blue_map.flatten()
mcMap_array = np.array([red_map,green_map,blue_map])
#mcMap_array_flat = np.array([flat_red_map,flat_green_map,flat_blue_map])

#move axis (3 channels are now the last dimension)
x_values = np.moveaxis(mcMap_array, 0, -1)

#changing the shape of the array to a long table with 3 columns
#first argument defines the number of rows, second argument the number of
# columns. -1 can be used to fill up the array depending on the data size (just
# fill the array until it's full)
# np.array([[1,2,3], [4,5,6]])
# np.array([[1,2,3], [4,5,6]]).reshape(3,-1)
#rows must be the values, cols must be the channels
X_data = x_values.reshape(-1, 3)


#prediction for total map
karte_pred = knn.predict(X_data)

#reshape back to normal format is necessary




#####
#nächste Aufgabe: Karte in korrekter Struktur ausgeben, sodass prediction funktioniert
# Vermutlich Struktur wie X notwendig

mcMap_array_flat.transpose(1)

shp = mcMap_array_flat.shape
out = x.transpose(1,0,2,3).reshape(shp[1],-1,shp[-1])
#####

mcMap_array_forPrediction = mcMap_array_flat.reshape(1171632,3)

np.array([flat_red_map, flat_red_map]).shape
np.array(np.arange(0, 3, 1), np.arange(0, len(flat_red_map), 1))

mcMap.close()

#visible atmospheric resistant index
#g-r/(g+r-bl)

landUsePoints["red"].plot()
plt.scatter(landUsePoints["green"], landUsePoints["blue"])

#classes
categories = ["tree", "road", "water", "grass", "sand", "path", "house", "rock", "snow", "crop", "rail"]

#plt.plot(landUsePoints["red"][landUsePoints["Category"] == "path"], landUsePoints["green"][landUsePoints["Category"] == "path"], "ro")

#supervised land use classification
#----------------------------------
#method: https://scikit-learn.org/stable/modules/cross_validation.html
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import svm

#########################################TEST CASE#############################
from sklearn import datasets
#150 measurements of 4 properties (x) on 3 different species (y)
X, y = datasets.load_iris(return_X_y=True)

X.shape
y.shape

#split into training and test data (40% of all samples are used as test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)

X_train.shape, y_train.shape

X_test.shape, y_test.shape

#https://towardsdatascience.com/land-cover-classification-in-satellite-imagery-using-python-ae39dbf2929
from sklearn.neighbors import KNeighborsClassifier

# K-NNC
knn = KNeighborsClassifier(n_neighbors=6)

knn.fit(X_train, y_train)

# Predict the labels of test data

knn_pred = knn.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, knn_pred)*100}")

print(classification_report(y_test, knn_pred))

#########################################TEST CASE END ########################

#in scikit-learn a random split into training and test sets can be quickly 
# computed with the train_test_split helper function
X = np.array(landUsePoints.loc[:,"red":]) #the spectral data
y = np.array(landUsePoints["Category"]) #the belonging categories

#split the dataset into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)

#Accuracy test, based on a classification model (Support vector machines (SVMs))
classifier = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
#mean accuracy based on the "raw" data
classifier.score(X_test, y_test) #0.745

#a third set can be defined, the validation set. It would be used to correct the
# fitted training set. But that would decreate the training set considerably.
#A solution is, to use the cross validation method (split the training data 
# into k samples and, at the end, compare those between each other to improve
# the model).

#cross validation 

#https://geohackweek.github.io/machine-learning/03-landclass/

classifier.fit(X_train, y_train)
y_t = classifier.predict()
predicted=y_t.reshape(rows, cols,3)

fig=plt.figure(figsize=(18, 16))
plt.imshow(palette[predicted][:,:,0])