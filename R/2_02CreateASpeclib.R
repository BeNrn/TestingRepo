#Purpose:    Create a spectral library.
#Created:    27.06.2019
#Author:     BeNrn
#--------------------------------------------------------------

file_base <- path.expand("<path_to_test_data>/")
# file_base <- path.expand("/media/limberger/Ben/KlimaAG_StudiStelle/03_Daten/")

require(hsdar)
#-------------------------------------------------------

# 1.1 read VIS data

exampleData <- read.csv(paste0(file_base, "pasture_reflectance_NIR.csv"), stringsAsFactors = FALSE)
#-------------------------------------------------------

# 1.2 Create Speclib 

#create the spectra matrix

## 1.2.1 unique spectra == IDs
value <- c()
for(i in 1:length(unique(exampleData$wavelength))){
  value[i] <- length(exampleData$wavelength[exampleData$wavelength == unique(exampleData$wavelength[i])])
}
unique(value)

exmpl_spec <- unique(value)

ID <- c(1:exmpl_spec)
rm(value)

## 1.2.2 number of spectral data for each spectrum
wavelngth <- unique(exampleData$wavelength)

#test if all spectra have the same number of reflectance values
#wavelength elements of the first object
# nrow(exampleData[exampleData$wavelength == wavelngth[1],])

# count = 0
# 
# for(i in 1:length(wavelngth)){
#  if(nrow(exampleData[exampleData$wavelength == wavelngth[i],]) == 95){
#    count <- count+1
#  }
# }

#all spectra have the same number of elements, the maximum is 95

#create an empty matrix and assign the reflectance values
spec_exmp <- matrix(NA, nrow = exmpl_spec, ncol = length(wavelngth))

for(i in 1:length(wavelngth)){
  temp <- exampleData$reflectance[exampleData$wavelength == wavelngth[i]]
  #print(i)
  #add the reflectance values to the wavelength (cols)
  if(length(temp) == 95){
    #just add them if they have the maximum length
    spec_exmp[,i] <- temp
  }else{
    #introduce NAs for the rest of the data
    numberOfNA <- 347 - length(temp)
    NAvector <- rep(NA, numberOfNA)
    temp <- append(temp, NAvector)
    spec_exmp[i,] <- temp
  }
}

ExmpSpeclib <- speclib(spectra = spec_exmp, wavelength = wavelngth)
ExmpSpeclib

#IDs and additional information
idSpeclib(ExmpSpeclib) <- as.character(ID)

#SI
nrow(exampleData[exampleData$ID == unique(exampleData$ID)[5],])
#every 512 rows a new spectrum begins
# -> every 512 plotLocation+acquisitionDate+ID is an SI element
index <- seq(from = 512, to = nrow(exampleData), by = 512)

#SI <- data.frame(plotLocation <- NA, acquisitionDate <- NA, ID <- NA)
for(i in 1:length(index)){
  temp <- exampleData[index[i],1:3]
  if(i == 1){
    SI <- temp
  }else{
    SI <- rbind(SI, temp) 
  }
}

SI(ExmpSpeclib) <- SI
