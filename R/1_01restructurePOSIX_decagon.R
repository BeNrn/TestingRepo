#Purpose:    Restructure data.
#Created:    27.11.2020
#Author:     BeNrn
#--------------------------------------------------------------

#set working directory and load libs
workingDir <- path.expand("<path_to_test_data>/Testdata") #files starting with EM
#workingDir <- path.expand("<path_to_test_data>")

require(stringr)
require(gdata)
#-------------------------------------------------------

#read file list
l <- list.files(workingDir, full.names = TRUE)
l <- l[which(stringr::str_extract(l, "filelist") == "filelist")]
filelist <- read.csv(l, header = F , stringsAsFactors = F)

#read excel sheets
decagon <- vector(mode = "list", length = 14)

#if loop to filter empty files
for(i in 1:nrow(filelist)){
  if(nrow(read.xls(paste0(workingDir, "/", filelist[i,]), header = FALSE, stringsAsFactors = F)) != 3 & ncol(read.xls(paste0(workingDir, "/", filelist[i,])) == 14)){
  df <- read.xls(paste0(workingDir, "/", filelist[i,]), header = FALSE, stringsAsFactors = F, skip = 3)
  decagon <- rbind(decagon, df)
  }
}

#test unique dates
unique(stringr::str_sub(decagon$V1, 1, 10))

#rename header
names(decagon) <- c("MeasurementTime", "P1", "P2_SRS-Pi_532nm", "P2_SRS-Pi_570nm", "P2_SRS-Pi_alphaPRI",
                    "P3_SRS-Pr_532nm", "P3_SRS-Pr_570nm", "P3_SRS-Pr_PRI", 
                    "P4_SRS-Ni_630nm", "P4_SRS-Ni_800nm", "P4_SRS-Ni_alphaNDV",
                    "P5_SRS-Nr_630nm", "P5_SRS-Nr_800nm", "P5_SRS-Nr_NDVI")
#where:
#   p1...port with number
#   SRS...spectral reflectance sensor
#   Pi...PRI measurement i=hemispherical (up looking)
#   Nr...NDVI measurement, r=field stop (down looking)
#   alpha...630/800 for NDVI; 571/532 for PRI

#remove data from 1999 and 2011 as they are caused by incorrect allocation 
decagon[stringr::str_sub(decagon$MeasurementTime, 7, 10) == 1999,]
decagon[stringr::str_sub(decagon$MeasurementTime, 7, 10) == 2011,]
decagon <- rbind(decagon[1:44835,], decagon[44840:nrow(decagon),])

#save the table / load the table for later use
# write.csv(decagon, "decagon_wide.csv", row.names = FALSE)
# decagon <- read.csv("decagon_wide.csv", stringsAsFactors = FALSE)

#all collected data from the sensors is numerical data
#assign the numerical class to all non-numerical columns 
decagon[,9] <- as.numeric(decagon[,9])
decagon[,10] <- as.numeric(decagon[,10])
decagon[,11] <- as.numeric(decagon[,11])
decagon[,5] <- as.numeric(decagon[,5])

#############################################
#convert date into posix format
#1.create POSIX format in a new column
#2.rearrange data frame
decagon$MeasurementTime1 <- as.POSIXct(NA)

for(i in 1:nrow(decagon)){
  decagon[i,15] <- as.POSIXct(decagon[i,1], format = "%d.%m.%Y %H:%M")
  print(i)
}

#some entries are printed in another date format
head(decagon[which(is.na(decagon[,15])),])

#-----------------------------------------------
#1.identify PM time
#2.create an index in an additional column
decagon$PM <- 0

for(k in 1:nrow(decagon)){
  if(is.na(decagon[k,15])){
    if(str_sub(decagon[k,1], 18,19) == "PM"){
      decagon[k,16] <- 1
    }
  }
}

#create an ID
decagon$ID <- 1:nrow(decagon)

#test if all NA-rows are clustered 
head(decagon[which(is.na(decagon[,15])),])
tail(decagon[which(is.na(decagon[,15])),])

testDeca <- decagon[7181:7773,]
unique(testDeca$MeasurementTime1)
rm(testDeca)
#-----------------------------------------------
#transform to POSIX
#add 12 hours to PM time
for(i in 7181:7773){
  decagon[i,15] <- as.POSIXct(decagon[i,1], format = "%m/%d/%Y %H:%M")
  if(decagon[i,16] == 1){
    decagon[i,15] <- decagon[i,15]+60*60*12
  }
}

decagon <- cbind(decagon[15], decagon[2:14], decagon[17])
#############################################
#save the table / load the table for later use
# write.csv(decagon, "decagon_POSIXDate.csv", row.names = FALSE)
decagon <- read.csv("<path_to_test_data>/testdata/decagon_POSIXDate.csv", stringsAsFactors = FALSE)
decagon$MeasurementTime1 <- as.POSIXct(decagon$MeasurementTime1)