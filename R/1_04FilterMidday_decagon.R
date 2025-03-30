#Purpose:    Filter midday values.
#Created:    27.11.2020
#Author:     BeNrn
#--------------------------------------------------------------

#set working directory and load libs
workingDir <- path.expand("<path_to_test_data>/Testdata")

require(ggplot2)
#-------------------------------------------------------
#2 Stunden vor Beginn der Mittagszeit bis zum Ende der Mittagszeit oder bis zum Regenereignis als regenfreie Zeit mit einbeziehen

#load deca
decagon <- read.csv(paste0(workingDir,"decagon_noDouble.csv"), stringsAsFactors = FALSE)
decagon$MeasurementTime1 <- as.POSIXct(decagon$MeasurementTime1)

#double entry of date values
nrow(decagon[which(duplicated(decagon[,1])),])

#filter midday values by indexing
decagon$midday <- NA 
for(j in 1:nrow(decagon)){
  #print(j)
  if(stringr::str_sub(decagon[j,1], 12, 13) == "10"){
    decagon[j,16] <- 1
  }else if(stringr::str_sub(decagon[j,1], 12, 13) == "11"){
    decagon[j,16] <- 1
  }else if(stringr::str_sub(decagon[j,1], 12, 13) == "12"){
    decagon[j,16] <- 1
  }else if(stringr::str_sub(decagon[j,1], 12, 13) == "13"){
    decagon[j,16] <- 1
  }else{
    decagon[j,16] <- 0
  }
}

#all entries are allocated with one value 
unique(decagon$midday)

nrow(decagon[decagon$midday == 1,])

#create a new df
middayDeca <- decagon[decagon$midday == 1,]  
middayDeca$midday <- NULL

#save the table / load the table for later use
# write.csv(middayDeca, paste0(workingDir, "decagon_midday.csv"), row.names = FALSE)
# middayDeca <- read.csv(paste0(workingDir, "decagon_midday.csv"), stringsAsFactors = FALSE)
# middayDeca$MeasurementTime1 <- as.POSIXct(middayDeca$MeasurementTime1)
##################################################################
#not yet reviewed

#determine albedo
middayDeca$albedo <- middayDeca$P2_SRS.Pi_532nm/middayDeca$P3_SRS.Pr_532nm

#plot
ggplot(data = middayDeca)+
  geom_point(mapping = aes(x = middayDeca$MeasurementTime1, y = middayDeca$albedo))
