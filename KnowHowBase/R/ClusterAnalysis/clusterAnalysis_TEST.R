#Rework the Silhouette function in:
# - Handl, A., & Kuhlenkasper, T. (2017). Multivariate Analysemethoden. https://doi.org/10.1007/978-3-662-54754-0 (Kapitel 13 - Clusteranalyse)

# Der Kern ist eine Ableitung der Abstände des Elements i in Gruppe k von den Elementen 
# in seiner Gruppe, ausgedrückt durch a, und von den anderen Gruppen durch b
library(magrittr)

e
dm

#1. define the number of the class for each element
e$cluster


#2. Create a df with the basic structure of the data
groupNumber <- e$cluster %>% unique() %>% length()

a <- numeric(0)
df <- data.frame(elementNumber = NULL, index = NULL, groupNum = NULL)
for(i in 1:groupNumber){
  #data values for class i
  groupElements <- alter[e$cluster == i]
  #index of each element 
  distCalc<- which(alter %in% groupElements)
  df_temp <- data.frame(elementNumber = groupElements, index = distCalc, groupNum = i)
  df <- rbind(df,df_temp)
}

df <- df[order(df$index),]
#3. calculate the mean distance of every element to the other elements in its group
df$a <- NA

#distance within group calculation
for(i in 1:nrow(df)){
  #all indices of the same group
  allDist <- dm[df$index[i],]
  indexDist <- df$index[df$groupNum == df$groupNum[i]]
  inGroupDist <- allDist[indexDist]
  inGroupDist <- inGroupDist[inGroupDist != 0]
  #calculate a (in group distance)
  df$a[i] <- mean(inGroupDist)
}

#4. calculate the mean distance to each other group and pick the nearest other group
outGroupDF <- data.frame(index = NULL, ingroup = NULL, outgroup = NULL, b = NULL)

for(i in 1:nrow(df)){
  groupNames <- unique(df$groupNum)
  #all other group numbers/names
  groupNames <- groupNames[-df$groupNum[i]]
  for(j in 1:length(groupNames)){
    allDist <- dm[df$index[i],]
    index_others <- df$index[df$groupNum == groupNames[j]]
    outGroupDist <- allDist[index_others]
    #mean of the out group distance to group j (for more than 2 groups there are 
    #multiple other groups)
    b <- mean(outGroupDist)
    #store them in a df
    outGroupDF_temp <- data.frame(index = df$index[i], ingroup = df$groupNum[i],
                                  outgroup = groupNames, meanDist = b)
    outGroupDF <- rbind(outGroupDF, outGroupDF_temp)
  }
}

df$nearestGroup <- NA
df$b <- NA
for(i in 1:nrow(df)){
  distToAllOtherGroups <- outGroupDF[outGroupDF$index == i,]
  nearestGroup <- distToAllOtherGroups$outgroup[distToAllOtherGroups$meanDist == min(distToAllOtherGroups$meanDist)]
  df$nearestGroup[i] <- nearestGroup
  df$b[i] <- min(distToAllOtherGroups$meanDist)
}

#5. calculate s(i)
df$s_i <- NA

for(i in 1:nrow(df)){
  df$s_i[i] <- ((df$b[i] - df$a[i])/pmax(df$a[i], df$b[i]))
}

#6. mean s(i) over all groups
meanSI <- numeric(0)
for(i in 1:length(unique(df$groupNum))){
  meanSI_temp <- df$s_i[df$groupNum == i] %>% mean()
  meanSI <- c(meanSI, meanSI_temp)
}

#7. Silhouette coefficient
silcoeff <- mean(df$s_i)

#8. data output
dat <- matrix(0, nrow(df), 3)
dat[,1] <- df$groupNum
dat[,2] <- df$nearestGroup
dat[,3] <- df$s_i

list(dat, meanSI, silcoeff)
