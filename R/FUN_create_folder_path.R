#Purpose:    Function to create a folder path list.
#Created:    24.06.2019
#Author:     BeNrn
#--------------------------------------------------------------

create_folder_path <- function(folderPath, validFolderNames, additionalFolder1level){
#' Create a list object that contains the pathes to connect all the relevant files
#'  
#'  @description The function works through the different folder levels, creates a path and returns additional information 
#'  derived from the folder structure.
#'  @description The folder names in the first level distinguishes between plant species (tree and pasture). The names in 
#'  the second level contains information concerning the plot location. The third level names are chosen by the acquisition 
#'  date and the fouth level namse descripe the ID for the trees and the species name for the pasture.
#'  @description The files that are connected by the folderPath containing reflectance information.
#'  
#'  @param folderPath The path to the parent folder where all files are included.
#'  @param validFolderNames A character vector containing all relevant folders in the folderPath folder. Used to filter folders
#'  in folderPath that do not contain relevant information.
#'  @param additionalFolder1level One additional folder with unused information at the first level.
#'  
#'  @return A list of folderpathes that point at the individual .txt files
#'  @return A vector containing all occuring IDs, plot locations and acquisition dates
#'  


# create directory list
dirList <- dir(folderPath, recursive= F, full.names = T)

#filter the dirList by valid folder pathes that contains the data
new_dirList <- list()
for(i in 1:length(dirList)){
  if(any(str_detect(dirList[i], validFolderNames))){
    if(length(new_dirList) == 0){
      new_dirList <- dirList[i]
    }else{
      new_dirList <- append(new_dirList, dirList[i])
    }
  }
}

dirList <- new_dirList

#The three folder levels named after: 
dirList1level <- list() #the locations
dirList2level <- list() # the acquisition time
dirList3level <- list() # the ID/the species

#create dirList at the location folder level
#as folders are named after plot location, the names are stored in the plotLocation vector
plotLocation <- c()
for(i in 1:length(dirList)){
  ###for the plotLocation###
  temp <- list.files(dirList[i])
  temp <- temp[temp != additionalFolder1level] #filter additionalFolder1level
  plotLocation <- append(plotLocation, temp)
  ##########################
  files1level <- list.files(dirList[i], full.names = T)
  firstPosition <- str_length(additionalFolder1level)
  files1level<- files1level[str_sub(files1level, -firstPosition, -1) != additionalFolder1level] #filter additionalFolder1level
  dirList1level <- append(dirList1level, files1level)
}


#create dirList at the acquisition date folder level
#as folders are named after acquisition date, the names are stored in the acquisitionDate vector
acquisitionDate <- c()
for(i in 1:length(dirList1level)){
  ###for the plotLocation###
  temp <- list.files(dirList1level[[i]])
  acquisitionDate <- append(acquisitionDate, temp)
  ##########################
  files2level <- list.files(dirList1level[[i]], full.names = T)
  dirList2level <- append(dirList2level, files2level)
}

#create dirList at the ID folder level
#as folders are named after acquisition date, the names are stored in the acquisitionDate vector
ID <- c()
for(i in 1:length(dirList2level)){
  ###for the plotLocation###
  temp <- list.files(dirList2level[[i]])
  ID <- append(ID, temp)
  ##########################
  files3level <- list.files(dirList2level[[i]], full.names = T)
  dirList3level <- append(dirList3level, files3level)
}

#create the final folder connection to the .txt files itself
dirList <- lapply(dirList3level, function(x){
  dir(x, full.names = T)
})
#put all the needed output vectors in one list
#dirList...the list with the unique file pathes
#ID...a vector with unique IDs (for pasture it is the species name)
#acquisistionDate...the time of the data acquisition
#plotLocation...the location where the data is acuired
returnList <- list(dirList, ID, acquisitionDate, plotLocation)

return(returnList)

}