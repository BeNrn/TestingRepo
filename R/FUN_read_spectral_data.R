#Purpose:    Function to read files from a list and rearrange them as data frame.
#Created:    26.06.2019
#Author:     BeNrn
#--------------------------------------------------------------

read_spectral_data <- function(identifier, dirList, ID, acquisitionDate, plotLocation, outputFolder){
#' Collect files from the dirList named after the identifier, read them and arrange them in a dataframe
#' 
#' @description The function chose files from the data structure in dirList that match the name used in *identifier*.
#' @description All files are read and binded together in a dataframe.
#' 
#' @param identifier The name that all files are named after.
#' @param dirList The directory list that contains the pathes to all the files.
#' @param ID A character vector containing all unique IDs.
#' @param acquisitionDate A character vector containing all unique acquisition dates.
#' @param plotLocation A character vector containing all unique plot locations.
#' @param outputFolder The path where the output .csv dataframe should be saved. 
#' 
#' @return Write a dataframe containing the plotlocation, the acquisition date and the ID as well as the wavelength and the reflectance values to the output folder.
#' 
  
  
  #read data
  
  identifier = identifier
  reflData = data.frame(wavelength = NA, reflectance = NA, ID = NA, plotLocation = NA, acquisitionDate = NA)
  
  for(i in 1:length(dirList)){
    print(i)
    for(j in 1:length(dirList[[i]])){
      if(str_detect(dirList[[i]][j], identifier)){
        temp <- read.csv(dirList[[i]][j], sep = "\t", dec = ".", stringsAsFactors = F, header = F, skip = 1)
        #if the file contains a longer header the first value is text and the is.na is TRUE
        #in this case the file is rereaded and 14 lines are skipped
        if(is.na(as.numeric(temp$V1[1]))){
          temp <- read.csv(dirList[[i]][j], sep = "\t", dec = ".", stringsAsFactors = F, header = F, skip = 14)
        }
        names(temp)[1:2] <- c("wavelength", "reflectance")
        #------
        #assign ID, plot location and acquisition date
        temp$ID <- ID[str_detect(dirList[[i]][j], ID)][1]
        temp$plotLocation <- plotLocation[str_detect(dirList[[i]][j], plotLocation)]
        temp$acquisitionDate <- acquisitionDate[str_detect(dirList[[i]][j], acquisitionDate)]
        #bind all files together
        reflData <- rbind(reflData[1:5], temp)
        #------
      }
    }
  }
  
  #clear the NA row from the creation procedure and change the column position
  reflData <- reflData[2:nrow(reflData),]
  reflData <- cbind(reflData[,4:5], reflData[3], reflData[,1:2])
  write.csv(reflData, outputFolder, row.names = FALSE)
}

