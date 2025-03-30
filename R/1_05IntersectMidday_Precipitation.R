#Purpose:    a script for the intersection of decagon albedo values and precipitation values 
#Created:    27.11.2020
#Author:     BeNrn
#--------------------------------------------------------------

workingDir <- "<path_to_test_data>/Testdata"

require(stringr)
require(ggplot2)
#-------------------------------------------------------

middayDeca <- read.csv(paste0(workingDir, "decagon_midday.csv"), stringsAsFactors = FALSE)
middayDeca$MeasurementTime1 <- as.POSIXct(middayDeca$MeasurementTime1)

rainfall <- read.csv(paste0(workingDir, "03_precipitationFinal.csv"), stringsAsFactors = FALSE)
rainfall$DateTime <- as.POSIXct(rainfall$DateTime)

#-------------------------------------------------------
#an albedo measurement is only defined as reliable result if the last rain fall at least two hours ago
#using the ECSF data

# 1 cutting the rain hours
rainfall <- rainfall[as.numeric(str_sub(rainfall$DateTime, 12,13)) > 7 & as.numeric(str_sub(rainfall$DateTime, 12,13)) < 14,]
rainfall$validMeasurementTime <- NA
#checking for precipitation
#if precipitation occured a zero is assigned, meaning the measurement is valid
for(i in 1:nrow(rainfall)){
  if(rainfall$pEcs[i] == 0){
    #in case of no precipitation
    rainfall$validMeasurementTime[i] <- 1
  }else{
    rainfall$validMeasurementTime[i] <- 0
  }
}

# 2 evaluating the decagon data
middayDeca$validMeasurementTime <- NA

#iterate over all days
for(i in 1:length(unique(str_sub(middayDeca$MeasurementTime1, 1, 10)))){
  #the day with the date i
  date <- unique(str_sub(middayDeca$MeasurementTime1, 1, 10))[i]
  
  #the data at date i
  rainTemp <- rainfall[str_sub(rainfall$DateTime, 1,10) == date,]
  decaTemp <- middayDeca[str_sub(middayDeca$MeasurementTime1, 1,10) == date,]
  
  #a measurement is valid if no precipitation occured at the moment of the measurement and at the 2 hours before the measurement
  #request these 3 precipitation values
  values <- c(8,9,10,11,12,13)
  index_values <- c(1,2,3,4,5,6)

  #for all 4 defined midday hours of the day i
  for(j in 1:4){
    #the 3 values
    vals <- index_values[as.numeric(j):as.numeric(j+2)]
    if(sum(rainTemp$validMeasurementTime[vals]) == 3){
      decaTemp$validMeasurementTime[str_sub(decaTemp$MeasurementTime1, 12,13) == as.character(values[as.numeric(j+2)])] <- 1
    }else{
      decaTemp$validMeasurementTime[str_sub(decaTemp$MeasurementTime1, 12,13) == as.character(values[as.numeric(j+2)])] <- 0
    }
  }
  #add the values to the decagon dataframe
  middayDeca$validMeasurementTime[str_sub(middayDeca$MeasurementTime1, 1,10) == date] <- decaTemp$validMeasurementTime
  
}

#-------------------------------------------------------
filterDeca <- middayDeca[middayDeca$validMeasurementTime == 1,]
filterDeca$validMeasurementTime <- NULL

#save the table / load the table for later use
# write.csv(filterDeca, paste0(workingDir, "processed/decagon_filtered.csv"), row.names = FALSE)
# filterDeca <- read.csv(paste0(workingDir, "processed/decagon_filtered.csv"), stringsAsFactors = FALSE)
# filterDeca$MeasurementTime1 <- as.POSIXct(filterDeca$MeasurementTime1)

#testing-------------------------------------

filterDeca$albedo <- ((filterDeca$P3_SRS.Pr_532nm*6.28)/filterDeca$P2_SRS.Pi_532nm)*100
filterDeca$albedo2 <- ((filterDeca$P3_SRS.Pr_532nm*6.28)/filterDeca$P2_SRS.Pi_532nm)*100
filterDeca$albedo3 <- ((filterDeca$P3_SRS.Pr_532nm*6.28)/filterDeca$P2_SRS.Pi_532nm)*100
filterDeca$albedo4 <- ((filterDeca$P3_SRS.Pr_532nm*6.28)/filterDeca$P2_SRS.Pi_532nm)*100

albedoDat <- filterDeca[filterDeca$albedo <= 100,]
albedoDat <- albedoDat[albedoDat$albedo < 20,]

ggplot(data = albedoDat)+
  geom_point(mapping = aes(x = albedoDat$MeasurementTime1, y = albedoDat$albedo))

singleDays <- unique(str_sub(albedoDat$MeasurementTime1, 1,10))[6]
albedoDat1 <- albedoDat[str_sub(albedoDat$MeasurementTime1, 1, 10) == singleDays,]

ggplot(data = albedoDat1)+
  geom_line(mapping = aes(x = albedoDat1$MeasurementTime1, y = albedoDat1$albedo))

#plot
ggplot(data = filterDeca)+
  geom_point(mapping = aes(x = filterDeca$MeasurementTime1, y = filterDeca$albedo))
ggplot(data = filterDeca)+
  geom_point(mapping = aes(x = filterDeca$MeasurementTime1, y = filterDeca$albedo2))
ggplot(data = filterDeca)+
  geom_point(mapping = aes(x = filterDeca$MeasurementTime1, y = filterDeca$albedo3))
ggplot(data = filterDeca)+
  geom_point(mapping = aes(x = filterDeca$MeasurementTime1, y = filterDeca$albedo4))
#only the 800nm band is useful for albedo calcultion

# TODO:
# correlation with precipitation sums of 3, 5, 10 days before measurement
# only 800nm sensor
# seminar meeting, thursday, 11.00 -> Boris Thies
# graph Precipitation (line), albedo points
# correlation table