#Purpose:    Rest of leaves.
#Created:    17.06.2019
#Author:     BeNrn
#--------------------------------------------------------------
#create subordinate directories
for(i in 1: length(dirList)){
  if()
}


for(i in 1: length(dirList)){
  if(str_sub(dir(paste0(file_base, dirList[i])), 1, 4) == "2019"){
    if(length(validSubDirs == 1)){
      validSubDirs <- paste0(file_base, dirList[i], "/", dir(paste0(file_base, dirList[i])))
    }else{
      temp <- paste0(file_base, dirList[i], "/", dir(paste0(file_base, dirList[i])))
      validSubDirs <- append(validSubDirs, temp) 
    }
  }
}

## 
identifier <- 'refl_raw_HDX*' # prefix for HDX raw data of reflectance measurement
filelist <- vector(mode = "character")
for(i in 1:length(dirList)){
  x  <- dir(dirList)
  # save the date into character string + repeat by number of subdirectories
  # get tree numbers from directories
  temp_filelist <- list.files(dirList[i], pattern = identifier)
  for(j in 1:length(temp_filelist)){
    filelist[(i+j-1)] <- paste0(dirList[i], "/", temp_filelist[j]) # does not work because of r indexing
  }
}



read.SpecRawData <- function(filename, repetitions){
  
  rawCountData <- vector(mode = "list", length = 1)
  measurement <- 0
  
  for(i in 1:nrow(filename)){
    rc <- read.table(filename[i,], sep="\t", dec=",", stringsAsFactors = F, header = F, skip = 2)
    measurement <- measurement + 1
    rc$measurement <- as.integer(measurement)
    rc$leaf_no <- as.integer(measurement %/% repetitions)
    rawCountData <- rbind(rawCountData, rc)
  }
  names(rawCountData) <- c("wavelength", "counts", "measurement", "leaf_no")
  
  return(rawCountData)
}

create.SpecLib <- function(rawCountData){
  
  
}