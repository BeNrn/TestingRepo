#Purpose:    Filter double entries
#Created:    27.11.2020
#Author:     BeNrn
#--------------------------------------------------------------

#set working directory and load libs
workingDir <- path.expand("<path_to_testdata>/Testdata/")
#-------------------------------------------------------

#load deca
decagon <- read.csv(paste0(workingDir, "decagon_POSIXDate.csv"), stringsAsFactors = FALSE)
decagon$MeasurementTime1 <- as.POSIXct(decagon$MeasurementTime1)

#determine double entries
decagon$doubleEntry <- 0

#number of double entries (where data values are dublicates from coloum 1 to 14 )
nrow(decagon[which(duplicated(decagon[,1]) & duplicated(decagon[,2]) & duplicated(decagon[,3]) 
                   & duplicated(decagon[,4]) & duplicated(decagon[,5]) & duplicated(decagon[,6])
                   & duplicated(decagon[,7]) & duplicated(decagon[,8]) & duplicated(decagon[,9])
                   & duplicated(decagon[,10]) & duplicated(decagon[,11]) & duplicated(decagon[,12])
                   & duplicated(decagon[,13]) & duplicated(decagon[,14])),])


#index for double entries
#decagon$doubleEntry turns to 1 when the aforementioned contidion is fulfilled
decagon[which(duplicated(decagon[,1]) & duplicated(decagon[,2]) & duplicated(decagon[,3]) 
                   & duplicated(decagon[,4]) & duplicated(decagon[,5]) & duplicated(decagon[,6])
                   & duplicated(decagon[,7]) & duplicated(decagon[,8]) & duplicated(decagon[,9])
                   & duplicated(decagon[,10]) & duplicated(decagon[,11]) & duplicated(decagon[,12])
                   & duplicated(decagon[,13]) & duplicated(decagon[,14])),][,16] <- 1

nrow(decagon[which(decagon[,16] == 1),])

#clear double entries
decagon <- decagon[decagon[,16] == 0,]
decagon$doubleEntry <- NULL

#save the table / load the table for later use
# write.csv(decagon, paste0(workingDir, "decagon_noDouble.csv"), row.names = FALSE)
# decagon <- read.csv(paste0(workingDir, "decagon_noDouble.csv"), stringsAsFactors = FALSE)
# decagon$MeasurementTime1 <- as.POSIXct(decagon$MeasurementTime1)

#there are still 246 double entries for the date left
nrow(decagon[which(duplicated(decagon[,1])),])
decagon[which(decagon[,1] == "2015-11-16 10:25:00"),]
