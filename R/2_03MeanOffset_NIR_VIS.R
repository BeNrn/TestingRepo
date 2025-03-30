#Purpose:    Restructure data.
#Created:    17.06.2019
#Author:     BeNrn
#--------------------------------------------------------------

file_base <- path.expand("<path_to_test_data>/Testdata")

require(hsdar)
require(stringr)
#-------------------------------------------------------
# 1 read the data
VISdata <- read.csv(paste0(file_base, "reflectance_dataHDX.csv"), stringsAsFactors = FALSE)
VISdata$reflectance <- as.numeric(VISdata$reflectance)
#change data type

#NA values, occurence unknown
VISdata[is.na(VISdata$reflectance),]
#error rows 283361:283364
VISdata <- rbind(VISdata[1:283360,], VISdata[283365:nrow(VISdata),])

VISdata$wavelength <- as.numeric(VISdata$wavelength)
#------------------------------------------------------
NIRdata <- read.csv(paste0(file_base, "reflectance_dataNIR.csv"), stringsAsFactors = FALSE)
#change data type
NIRdata$reflectance <- as.numeric(NIRdata$reflectance)
NIRdata$wavelength <- as.numeric(NIRdata$wavelength)
#------------------------------------------------------

plot(VISdata$wavelength[1:5000], VISdata$reflectance[1:5000])
plot(NIRdata$wavelength[1:5000], NIRdata$reflectance[1:5000])



