#Purpose:    Script for correcting Decagon albedo data with daytime and precipitation
#            subsequently, a GAM is created to estimate the correlation of albedo value and precipitation
#Created:    27.11.2020
#Author:     BeNrn
#--------------------------------------------------------------

workingDir <- "<path_to_test_data>/Testdata"

library(stringr)
library(gdata)
library(ggplot2)
library(mgcv)
#-------------------------------------------------------------------------------
#1 LOAD THE DATA
#-------------------------------------------------------------------------------
#the albedo dots
#10-2015 to 02-2016
#read the file
decagon <- read.csv(paste0(file_base, "decagon_POSIXDate.csv"), stringsAsFactors = FALSE)
decagon <- read.csv(paste0(workingDir,"decagon_noDouble.csv"), stringsAsFactors = FALSE)
decagon$MeasurementTime1 <- as.POSIXct(decagon$MeasurementTime1)

#calculate albedo
decagon$albedo <- ((decagon$P3_SRS.Pr_532nm*6.28)/decagon$P2_SRS.Pi_532nm)*100

#filter non valid albedo values
albedoDat <- decagon[decagon$albedo <= 100 & !is.na(decagon$albedo),]
albedoDat <- albedoDat[albedoDat$albedo < 25,]

#plot
# ggplot(data = albedoDat)+
#   geom_point(mapping = aes(x = albedoDat$MeasurementTime1, y = albedoDat$albedo), color = "darkgreen")+
#   ggtitle("Albedo derived from the unprocessed decagon dataset")+
#   xlab("Measurement Time")+
#   ylab("Albedo")

