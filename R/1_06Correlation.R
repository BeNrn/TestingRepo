#Purpose:    correlation between precipitation and albedo.
#Created:    27.11.2020
#Author:     BeNrn
#--------------------------------------------------------------

workingDir <- "<path_to_test_data>/Testdata"

library(stringr)
library(ggplot2)
library(mgcv)
library(magrittr)

#-------------------------------------------------------------------------------
#1 LOAD THE DATA
#-------------------------------------------------------------------------------
#decagon
#midday hours 5min resolution from 11.00 to 12.55
middayDeca <- read.csv(paste0(workingDir, "decagon_midday.csv"), stringsAsFactors = FALSE)
middayDeca$MeasurementTime1 <- as.POSIXct(middayDeca$MeasurementTime1)

#precipitation
#hourly resolution covering the date span of the decagon midday hours  
rainfall <- read.csv(paste0(workingDir, "03_precipitationFinal.csv"), stringsAsFactors = FALSE)
rainfall$DateTime <- as.POSIXct(rainfall$DateTime)

#-------------------------------------------------------------------------------
#2 CREATE DATAFRAME FOR CORRELATION
#-------------------------------------------------------------------------------

#2.1 sum daily pp with ecsf data
#--------------------------------
days <- unique(str_sub(middayDeca$MeasurementTime1, 1,10))

ppSums <- data.frame(days = days, dailyPP = NA)
ppSums$days <- as.character(ppSums$days)

for(i in 1:nrow(ppSums)){
  ppSums$dailyPP[i] <- sum(rainfall$pEcs[str_sub(rainfall$DateTime, 1, 10) == ppSums$days[i]]) 
}

#2.2 calculate pp sums of the last 3,5,10 days
#---------------------------------------------
#three days
ppSums$threeDays <- NA
for(i in 1:nrow(ppSums)){
  if(i <= 3){
    ppSums$threeDays[i] <- NA
  }else{
    ppSums$threeDays[i] <- sum(ppSums$dailyPP[(i-3):(i-1)])
  }
}

#5 days
ppSums$fiveDays <- NA
for(i in 1:nrow(ppSums)){
  if(i <= 5){
    ppSums$fiveDays[i] <- NA
  }else{
    ppSums$fiveDays[i] <- sum(ppSums$dailyPP[(i-5):(i-1)])
  }
}

#10 days
ppSums$tenDays <- NA
for(i in 1:nrow(ppSums)){
  if(i <= 10){
    ppSums$tenDays[i] <- NA
  }else{
    ppSums$tenDays[i] <- sum(ppSums$dailyPP[(i-10):(i-1)])
  }
}

#2.3 create the df
#-----------------
#restructure the existing df
#days without pp
noPP <- ppSums$days[ppSums$dailyPP == 0]

middayDeca$noPP <- 0
for(i in 1:nrow(middayDeca)){
  for(j in 1:length(noPP)){
    if(str_sub(middayDeca$MeasurementTime1[i], 1,10) == noPP[j]){
      middayDeca$noPP[i] <- 1
    }
  }
}

filterDeca <- middayDeca[middayDeca$noPP == 1,]
middayDeca$noPP <- NULL

middayLastDays <- cbind(filterDeca[1], filterDeca[10], filterDeca[13], filterDeca[15])
middayLastDays[5:7] <- NA
names(middayLastDays)[5:7] <- c("threeDays", "fiveDays", "tenDays")

#add data
#only days without pp included
for(i in 1:nrow(middayLastDays)){
  for(j in 1:nrow(ppSums)){
    if(str_sub(middayLastDays$MeasurementTime1[i], 1, 10) == str_sub(ppSums$days[j],1,10)){
      middayLastDays[i,5:7] <- ppSums[j,3:5]
    }
  }
}

#2.4 write the df to hard drive
#------------------------------
middayLastDays$albedo4 <- middayLastDays$P4_SRS.Ni_800nm/middayLastDays$P5_SRS.Nr_800nm
#write.csv(middayLastDays, paste0(workingDir, "decagon_cor_base.csv"), row.names = FALSE)
middayLastDays <- read.csv(paste0(workingDir, "decagon_cor_base.csv"), stringsAsFactors = FALSE)

#-------------------------------------------------------------------------------
#3 CORRELATION
#-------------------------------------------------------------------------------
#see: https://rstudio-pubs-static.s3.amazonaws.com/240657_5157ff98e8204c358b2118fa69162e18.html

#3.1 Correlation
#---------------
#cor(x, y, method = "pearson")
cor(middayLastDays$albedo4, middayLastDays$threeDays, use = "na.or.complete", method = "pearson")
# [1] -0.06430621
cor(middayLastDays$albedo4, middayLastDays$fiveDays, use = "na.or.complete", method = "pearson")
# [1] -0.03779579
cor(middayLastDays$albedo4, middayLastDays$tenDays, use = "na.or.complete", method = "pearson")
# [1] -0.04951119

#3.2 plot the created df
#-----------------------
ggplot(data = middayLastDays)+
  geom_point(mapping = aes(x = MeasurementTime1, y = albedo4))

ggplot(data = middayLastDays)+
  geom_point(mapping = aes(x = albedo4, y = threeDays))

ppSums<- ppSums[order(ppSums$days),]

plot(as.POSIXct(ppSums$days), ppSums$dailyPP, type = "l")

ggplot(data = ppSums, aes(x = days, y = dailyPP, group = 1))+
  geom_line()

#-------------------------------------------------------------------------------
#4 GAM
#-------------------------------------------------------------------------------
#4.1 load new data
#-------------------
decagon <- read.csv(paste0(workingDir, "decagon_filtered.csv"), stringsAsFactors = FALSE)
decagon$MeasurementTime1 <- as.POSIXct(decagon$MeasurementTime1)

decagon$albedo <- ((decagon$P3_SRS.Pr_532nm*6.28)/decagon$P2_SRS.Pi_532nm)*100
albedoDat <- decagon[decagon$albedo <= 100,]
albedoDat <- albedoDat[albedoDat$albedo < 20,]
albedoDat <- albedoDat[!is.na(albedoDat$MeasurementTime1),]

#assign single days
albedoDat$day <- NA

for(i in 1:nrow(albedoDat)){
  num <- str_which(str_sub(albedoDat$MeasurementTime1, 1, 10)[i] == unique(str_sub(albedoDat$MeasurementTime1, 1, 10)), "TRUE")
  albedoDat$day[i] <- num
}

#write.csv(albedoDat, paste0(workingDir, "decagon_GAM_1.csv"), row.names = FALSE) 
#albedoDat <- read.csv(paste0(workingDir, "decagon_GAM_1.csv"), stringsAsFactors = FALSE)
#albedoDat$MeasurementTime1 <- as.POSIXct(albedoDat$MeasurementTime1)

#remove all irrelevant columns
albedoDat[,2:14] <- NULL

testAlbedo <- albedoDat[albedoDat$day == 1,]
testAlbedo$xVals <- seq(1:nrow(testAlbedo))
testAlbedo$xVals <- as.numeric(testAlbedo$xVals)
df2 <- data.frame(x = testAlbedo$xVals, y = testAlbedo$albedo)

gammod <- mgcv::gam(y ~ s(x, k = 1, fx = FALSE), data = df2)
gammod

# Family: gaussian 
# Link function: identity 
# 
# Formula:
#   y ~ s(x, k = 1, fx = FALSE)
# 
# Estimated degrees of freedom:
#   1.92  total = 2.92 
# 
# GCV score: 0.3870452

px <- seq(min(df2$x), max(df2$x), 0.1)
gampred <- predict(gammod, list(x = px))

plot(df2$x, df2$y, xlab = "Measurements at each day", ylab = "Albedo values", main = "Non-linead albedo regression using GAM" )
lines(px, gampred, col = "red")

#plot for the 20 first days
dfPlot <- data.frame(x = c(1, 48), y = c(4, 11))
plot(dfPlot$x, dfPlot$y, xlab = "Measurements at each day", ylab = "Albedo values", main = "Non-linead albedo regression using GAM", col = "white")
cols <- palette(rainbow(20))
for(i in 1:20){
  testAlbedo <- albedoDat[albedoDat$day == i,]
  testAlbedo$xVals <- seq(1:nrow(testAlbedo))
  testAlbedo$xVals <- as.numeric(testAlbedo$xVals)
  df2 <- data.frame(x = testAlbedo$xVals, y = testAlbedo$albedo)
  
  gammod <- mgcv::gam(y ~ s(x, k = 1, fx = FALSE), data = df2)
  px <- seq(min(df2$x), max(df2$x), 0.1)
  gampred <- predict(gammod, list(x = px))
  lines(px, gampred, col = cols[i])
}