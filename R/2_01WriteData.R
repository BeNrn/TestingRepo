#Purpose:    Write data.
#Created:    09.07.2019
#Author:     BeNrn
#--------------------------------------------------------------
file_base <- path.expand("<path_to_test_data>/Testdata")

require(stringr)
#erster Ordner (Bombuscaro, 1 bis 144 alle IDs vorhanden)
#ID[131:144]
#-------------------------------------------------------

# 1 create folder pathes for pasture

#create a list with the pathes to all the relevant files using the create_folder_path function
#also returns unique plot locations, IDs(species names for pasture) and acquisition dates
source("<path_to_this_file>/FUN_create_folder_path.R")
returnList <- create_folder_path(folderPath = paste0(file_base, "org/field_data/"),
                                 validFolderNames = c("pasture_spectra"),
                                 additionalFolder1level = "TOSORT")

dirList <- returnList[[1]]
ID <- returnList[[2]]
acquisitionDate <- returnList[[3]]
plotLocation <- returnList[[4]]
rm(returnList)
#-------------------------------------------------------

# 2 create .csv files for:
# - reflectance NIR
# - transmittance NIR
# - dark current reflectance NIR
# - dark current reference NIR
# - reflectance VIS
# - transmittance VIS
# - dark current reflectance VIS
# - dark current reference VIS
source("<path_to_this_file>/read_spectral_data.R")

identifierList <- c("refl_raw_NQ*", "transm_raw_NQ*", "refl_refdc_NQDarkCurrent*", "refl_refdc_NQReference*",
                    "refl_raw_HDX*", "transm_raw_HDX*", "refl_refdc_HDXDarkCurrent*", "refl_refdc_HDXReference*")

outputFolderList <- c("pasture_reflectance_NIR.csv", "pasture_transmittance_NIR.csv", "pasture_darkCurrent_NIR.csv", "pasture_darkCurrentRef_NIR.csv",
                      "pasture_reflectance_VIS.csv", "pasture_transmittance_VIS.csv","pasture_darkCurrent_VIS.csv","pasture_darkCurrentRef_VIS.csv")

for(i in 1:length(identifierList)){
  print(i)
  read_spectral_data(identifier = identifierList[i], dirList = dirList, ID = ID, acquisitionDate = acquisitionDate, 
                     plotLocation = plotLocation, outputFolder = paste0(file_base, "processed/", outputFolderList[i]))
  
}

#-------------------------------------------------------

# 3 create folder pathes for tree leaves 

#create a list with the pathes to all the relevant files using the create_folder_path function
#also returns unique plot locations, IDs(species names for pasture) and acquisition dates
source("<path_to_this_file>/create_folder_path.R")
returnList <- create_folder_path(folderPath = paste0(file_base, "org/field_data/"),
                                 validFolderNames = c("treeleaf_spectra"),
                                 additionalFolder1level = "TOSORT")

dirList <- returnList[[1]]
ID <- returnList[[2]]
acquisitionDate <- returnList[[3]]
plotLocation <- returnList[[4]]
rm(returnList)
#-------------------------------------------------------

# 4 create .csv files for:
# - reflectance NIR
# - transmittance NIR
# - dark current reflectance NIR
# - dark current reference NIR
# - reflectance VIS
# - transmittance VIS
# - dark current reflectance VIS
# - dark current reference VIS
source("<path_to_this_file>/read_spectral_data.R")

identifierList <- c("refl_raw_NQ*", "transm_raw_NQ*", "refl_refdc_NQDarkCurrent*", "refl_refdc_NQReference*",
                    "refl_raw_HDX*", "transm_raw_HDX*", "refl_refdc_HDXDarkCurrent*", "refl_refdc_HDXReference*")

outputFolderList <- c("treeLeaf_reflectance_NIR.csv", "treeLeaf_transmittance_NIR.csv", "treeLeaf_darkCurrent_NIR.csv", "treeLeaf_darkCurrentRef_NIR.csv",
                      "treeLeaf_reflectance_VIS.csv", "treeLeaf_transmittance_VIS.csv","treeLeaf_darkCurrent_VIS.csv","treeLeaf_darkCurrentRef_VIS.csv")

for(i in 6:length(identifierList)){
  print(i)
  read_spectral_data(identifier = identifierList[i], dirList = dirList, ID = ID, acquisitionDate = acquisitionDate, 
                     plotLocation = plotLocation, outputFolder = paste0(file_base, "processed/", outputFolderList[i]))
  
}
