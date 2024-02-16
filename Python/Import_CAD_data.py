# -*- coding: utf-8 -*-
"""
Purpose:    Load DXF files, add a coordinate system and write them to shape 
            file format.
Created:    16.02.2024
Author:     BeNrn
"""

def dxf2Shape(baseDir, dxfFileName, inputCRS, shapeName, outputCRS = 31287):
    """
    Load DXF files, add a coordinate system and write them to shape file format.

    Parameters
    ----------
    baseDir : string
        Path ot environment where the dxf file resides.
    dxfFileName : string
        Name of the dxf file in baseDir.
    inputCRS : integer
        EPSG-Code of the dxf file.
    shapeName : string
        Name of the output file without file ending.
    outputCRS : integer, optional
        EPSG-Code of the final shape file. The default is Austria Lambert with 
        31287.

    Returns
    -------
    One shape file per geometry type in the output location.
    """
    #load libs
    import geopandas as gp
    import os
    
    #set paths
    baseDir = baseDir
    
    #DWG files must be converted to the open DXF file format first
    
    dxfFile = gp.read_file(filename = os.path.join(baseDir, dxfFileName))
    
    dxfFile = dxfFile.set_crs(epsg = inputCRS)
    
    #return crs
    print(dxfFile.crs)
    
    #dxfFile.plot()
    
    #skip if no transformation is defined
    if outputCRS is not None:
        #to new crs
        dxfFile = dxfFile.to_crs(epsg = outputCRS)
        
    #dxf file contians up to four different geometry types
    # to make them available as a shapefile all different geometry types must 
    # be exported separately
    #get all distinct geometry types
    geometrySet = set(dxfFile.geom_type)
    
    #iterate over geometry types and write to disk
    for geometryType in geometrySet:
        dxfFile[dxfFile.geom_type == geometryType].to_file(filename = os.path.join(baseDir, shapeName + "_" + geometryType + ".shp"))
        
# dxf2Shape(baseDir = r"C:\pseudopath",
#               dxfFile = "cad_file.dxf",
#               inputCRS = 4326,
#               outputCRS = 31287,
#               shapeName = "output_shape")