#Purpose:    Precrocess precipitation data.
#Created:    27.11.2020
#Author:     BeNrn
#--------------------------------------------------------------

#set working directory and load libs
workingDir <- path.expand("<path_to_testdata>/Testdata/")

library(stringr)
library(ggplot2)
#-------------------------------------------------------

#load precipitation data
rainfall <- read.csv(paste0(workingDir, "Plogger_h.csv"), stringsAsFactors = FALSE)

#restructure date formate
rainfall$DateTime2 <- as.POSIXct(NA)

for(i in 1:nrow(rainfall)){
  rainfall[i,27] <- as.POSIXct(rainfall[i,1], format = "%d.%m.%Y %H:%M:%S")
  print(i)
}

#change order to the initial structure
#original date is kept, to compare
rainfall <- cbind(rainfall[27], rainfall[1], rainfall[2:26])
names(rainfall)[1] <- "DateTime"
names(rainfall)[2] <- "OriginalDate"

#save the table / load the table for later use
# write.csv(rainfall, "<path_to_testdata>/01_precipitation.csv", row.names = FALSE)
rainfall <- read.csv(paste0(workingDir, "01_precipitation.csv"), stringsAsFactors = FALSE)
rainfall$DateTime <- as.POSIXct(rainfall$DateTime)

#the last 3 columns only contain NA values and are removed
rainfall <- rainfall[1:24]

#identify  NAs
rainfall[which(is.na(rainfall$DateTime)),1:2]
# -> NAs are caused by time shift

#filter date which is relevant for decagon
#decagon data covers a time period from 10.2015 to 02.2016
#filter rainfall data at a yearly resolution
rainfall <- rainfall[str_sub(rainfall$DateTime, 1, 4) == 2016 | str_sub(rainfall$DateTime, 1, 4) == 2015,]

#filter NA because they do not overlap with the decagon time interval as it can be shown by the originalDate column
rainfall <- rainfall[!is.na(rainfall$DateTime),]
unique(str_sub(rainfall$DateTime, 1, 4))

#----------------------------------------------------------
#determine the relevant precipitation  (yearly resolution)
index = NA
for(i in 3:ncol(rainfall)){
  if(length(unique(rainfall[,i])) != 1 & is.na(index)){
   index <- i
  }else if(length(unique(rainfall[,i])) != 1){
   lngt <- length(index)
   index[lngt+1] <- i
  }
}

#bind the sensors which delivered data for the examination period to the new data frame
tempRain <- cbind(rainfall[1:2])

for(j in 1:length(index)){
  tempRain <- cbind(tempRain, rainfall[index[j]])
}
ppCleared <- tempRain
rm(tempRain)

#pEcs = ECSF climate station                      [suitable for decagon data]
#pMrr = MRR station near ECSF                     [s.]
#pTor = Torres Climate Station near ECSF          [s.]
#pGeg = Gegenhang Climate station near ECSF       [s.]
#pFar = Farn station near ECSF climate station    [s.]
#pTir = El Tiro station                           [not s.]
#pBom = Climate station Bombuscaro                [not s.]

ppCleared <- ppCleared[1:7]
#caution: the "pTor" and "pFar" data show a sorted structure for low(first) or all(second) precipitation

#save the table / load the table for later use
# write.csv(ppCleared, paste0(workingDir, "02_precipitationCleared.csv"), row.names = FALSE)
# ppCleared <- read.csv(paste0(workingDir, "02_precipitationCleared.csv"), stringsAsFactors = FALSE)
# ppCleared$DateTime <- as.POSIXct(ppCleared$DateTime)


#determine relevant precipitation data for decagon data
decagon <- read.csv(paste0(workingDir, "decagon_noDouble.csv"), stringsAsFactors = FALSE)
decagon$MeasurementTime1 <- as.POSIXct(decagon$MeasurementTime1)

#########################################################################
# Ausrei�er sollten zuerst identifiziert werden
# Dann m�ssen bestenfalls die ECSF Daten verwendet werden
#########################################################################

#chose data by mothly time resolution
#resulting in df with only relevant precipitation data at monthly resolution scale
unique(str_sub(ppCleared$DateTime, 1, 7))
combi <- unique(str_sub(decagon$MeasurementTime1, 1, 7))


for (i in 1:length(combi)){
  if(i == 1){
    df <- ppCleared[str_sub(ppCleared$DateTime, 1, 7) == combi[i],]
  }else{
    df <- rbind(df, ppCleared[str_sub(ppCleared$DateTime, 1, 7) == combi[i],])
  }
}

ppCleared <- df
nrow(df[is.na(ppCleared$pEcs),])

#remove df$pMrr and df$pFar because they do not contain any values
ppCleared <- cbind(ppCleared[1:3], ppCleared[5:6])

#save the table / load the table for later use
# write.csv(ppCleared, paste0(workingDir, "03_precipitationFinal.csv"), row.names = FALSE)
# ppCleared <- read.csv(paste0(workingDir, "03_precipitationFinal.csv"), stringsAsFactors = FALSE)
# ppCleared$DateTime <- as.POSIXct(ppCleared$DateTime)
##################################################################
#not yet reviewed

#outliers
ppCleared$span <- NA

for(i in 1:nrow(ppCleared)){
  ppCleared$span[i] <- max(ppCleared[i,3:5]) - min(ppCleared[i,3:5])
}

#plot
#NA values for span if one measurement value is missing
#thats correct as there is no way of calculating the span in a different way properly
ggplot(data = ppCleared)+
  geom_point(mapping = aes(x = DateTime, y = span), color = "darkgreen")+
  ggtitle("Span of pEcs, pTor and pGeg")+
  xlab("Date (ppCleared)")+
  ylab("Span")
