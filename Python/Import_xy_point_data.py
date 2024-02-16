# -*- coding: utf-8 -*-
"""
Purpose:    Load xy point file, add a coordinate system and write them to shape 
            file format.
Created:    16.02.2024
Author:     BeNrn
"""

def xy2Shape(baseDir, xyFileName, xColumn, yColumn, idColumn, inputCRS, shapeName, decimalDelimiter = ",", outputCRS = 31287):
    """
    Load xy point file, add a coordinate system and write them to shape file format.

    Parameters
    ----------
    baseDir : string
        Path ot environment where the dxf file resides.
    xyFileName : string
        Name of the xy file in baseDir.
    xColumn : string
        Name of the column that holds the x coordinate.
    yColumn : string
        Name of the column that holds the y coordinate.
    idColumn : string
        Name of the column that holds the id column.
    inputCRS : integer
        EPSG-Code of the dxf file.
    shapeName : string
        Name of the output file without file ending.
    decimalDelimiter : string
        Delimiter that separates decimal position.
    outputCRS : integer, optional
        EPSG-Code of the final shape file. The default is Austria Lambert with 
        31287.

    Returns
    -------
    One point shape file in the output location.
    """
    #load libs
    import geopandas as gp
    import os
    
    #set paths
    baseDir = baseDir
    
    pointFile = gp.read_file(filename = os.path.join(baseDir, xyFileName), delimiter = decimalDelimiter)
    
    pointFile[xColumn] = pointFile[xColumn].astype(float)
    pointFile[yColumn] = pointFile[yColumn].astype(float)
    pointFile[idColumn] = pointFile[idColumn].astype(int)
    
    #calculate geometry column
    pointFile_xy = gp.points_from_xy(x = pointFile[xColumn], y = pointFile[yColumn], crs = inputCRS)
    
    #add together
    pointDF = gp.GeoDataFrame(pointFile, geometry = pointFile_xy)
    
    #return crs
    print(pointDF.crs)
    
    #pointDF.plot()
    
    #skip if no transformation is defined
    if outputCRS is not None:
        #to new crs
        pointDF = pointDF.to_crs(epsg = outputCRS)
        
    pointDF.to_file(filename = os.path.join(baseDir, "{}.shp".format(shapeName)))
        
# xy2Shape(baseDir = r"C:\pseudopath",
#          xyFileName = "pointFile.csv", 
#          xColumn = "LON", 
#          yColumn = "LAT", 
#          idColumn = "ID", 
#          inputCRS = 4326, 
#          shapeName = "output_shape", 
#          decimalDelimiter = ",", 
#          outputCRS = 31287)