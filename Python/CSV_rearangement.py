# -*- coding: utf-8 -*-
"""
Purpose:    Rearange a CSV file.
Created:    07.10.2023
Author:     BeNrn
"""

#libs
import pandas as pd

#path
baseDir = r"C:\path...."

#open list
data = pd.read_csv(baseDir + r"\fileName.csv",
                   sep = ";",
                   header = 0,
                   encoding = "latin",
                   decimal = ",",
                   thousands = ".",
                   dtype = {"Datum": "str"})

#remove unneccesary columns
data = data.drop(["col1", "col2"], axis = 1)

#rearange columns
columnNames = data.columns.tolist()
columnNames = [columnNames[1]] +  [columnNames[0]] + columnNames[2:]
data = data[columnNames]

#add new calculation column
data["col3"] = 0

#merge transfers in one column
for index, entry in data.iterrows():
    #subtract charges
    data.loc[index, "col3"] = data.loc[index, "col3"] - data.loc[index, "col4"]
    #add transfers
    data.loc[index, "col3"] = data.loc[index, "col3"] + data.loc[index, "col5"]
    
#remove original transfer columns
data = data.drop(["col4", "col5"], axis = 1)

#rearange once more
columnNames = data.columns.tolist()
columnNames = [columnNames[0]] +  [columnNames[2]] + [columnNames[1]]
data = data[columnNames]

data.to_csv(baseDir + "\Processed_CSV.csv",
            sep = ";",
            index = False,
            decimal = ",")
