# [Title]: Count pre and post-fallowing land-uses
# [Subtitle]: Basin and States
# [Name]: Kevin Neal


### Data importing and formating
# Importing every CSV file that starts with ""crop_eco" and "crop_state"fallowcrops" and storing it in one variable
input_csv <- "~/fallow_cropland/csvs/fallowcrops.csv"


cdl.raw <- read.csv(input_csv,
                header = T)

cdl <- cdl.raw[, c(4 : 14)]
cdl.classes <- c(1:254 , 999)
years <- c(2008 : 2018)

### Create matrix to store reuslts
# A for after (post-fallowing land-use)
# B for before (pre-fallowing land-use)
land.use.B <- matrix(data = NA , 
                     nrow = length(cdl[, 1]) , 
                     ncol = length(years))
land.use.A <- matrix(data = NA ,
                     nrow = length(cdl[, 1]) ,
                     ncol = length(years))
use.total.B <- matrix(NA ,
                      nrow = length(cdl.classes) ,
                      ncol = length(years))
use.total.A <- matrix(NA ,
                      nrow = length(cdl.classes) ,
                      ncol = length(years))
classA.totals <- matrix(data = NA ,
                        nrow = 0 , 
                        ncol = length(years))
classB.totals <- matrix(data = NA ,
                        nrow = 0 ,
                        ncol = length(years))
classA <- matrix(data = NA ,
                 nrow = 0 ,
                 ncol = length(years))
classB <- matrix(data = NA ,
                 nrow = 0 ,
                 ncol = length(years))

classB.index <- NA # rep(0 , 1)
classA.index <- NA # rep(0 , 1)
A.classes <- NA
B.classes <- NA

colnames(land.use.A) <- years
colnames(land.use.B) <- years
colnames(use.total.A) <- years
colnames(use.total.B) <- years

### Calculates the land use class for every point the year before and after a land classification of 61 is observed
for(i in 1 : length(cdl[, 1])){                                  ### Point data land classifcation BEFORE
  class.temp.B <- as.integer(cdl[i ,])
  
  for(j in 1 : length(years)){
    if(class.temp.B[j] == 61){
      if(j == 1){
        land.use.B[i , j] <- 999

      }
      if(j > 1){
        land.use.B[i , j] <- class.temp.B[j - 1]
        
      }
    }
  }
}
                                                
for(i in 1 : length(cdl[, 1])){                                  ### Point data land classifcation AFTER
  class.temp.A <- as.integer(cdl[i ,])
  
  for(j in 1 : length(years)){
    if(class.temp.A[j] == 61){
      if(j == length(years)){
        land.use.A[i , j] <- 999
        
      }
      if(j < length(years)){
        land.use.A[i , j] <- class.temp.A[j + 1]
        
      }
    }
  }
}

land.use.B[is.na(land.use.B) == T] <- 0                        # Converting NA to 0
land.use.A[is.na(land.use.A) == T] <- 0

### Populates a matrix that sums up the each land use changes that was observed for that year
### Summing up each land classification BEFORE
for(i in 1 : length(years)){                                   
  temp.year.B <- land.use.B[, i]                               # Selects year(column) for evaluation
  class.B <- unique(temp.year.B)                               # Finds unique values of crops observed from that year
  class.B <- class.B[class.B != 0]                             # Removes zero
  
  for(j in 1 : length(class.B)){
    crop <- class.B[j]                                         # The crop pixel value
    crop.index <- match(crop , cdl.classes)                    # Find the index of the crop pixel value
    use.total.B[crop.index , i] <- sum(temp.year.B == crop)    # Totals up how many times that crop appeared BEFORE barren
  }
}
### Summing up each land classification AFTER
for(i in 1 : length(years)){
  temp.year.A <- land.use.A[, i]                               # Selects year(column) for evaluation
  class.A <- unique(temp.year.A)                               # Finds unique values of crops observed from that year
  class.A <- class.A[class.A != 0]                             # Removes zero
  
  for(j in 1 : length(class.A)){
    crop <- class.A[j]                                         # The crop pixel value
    crop.index <- match(crop , cdl.classes)                    # Find the index of the crop pixel value
    use.total.A[crop.index , i] <- sum(temp.year.A == crop)    # Totals up how many times that crop appeared AFTER barren
  }
}

use.total.B[is.na(use.total.B) == T] <- 0                      # Converting NA to 0
use.total.A[is.na(use.total.A) == T] <- 0

### Removes rows that no land classification was observed throughout the years
for(i in 1 : length(use.total.B[, 1])){                        # Shortening matrix BEFORE
  temp.B <- use.total.B[i ,]
  
  if(sum(temp.B) > 0){
    classB <- rbind(classB , temp.B)
    B.classes <- c(B.classes , i)
  }
}

for(i in 1 : length(use.total.A[,1])){                         # Shortening matrix AFTER
  temp.A <- use.total.A[i ,]
  
  if(sum(temp.A) > 0){
    classA <- rbind(classA , temp.A)
    A.classes <- c(A.classes , i)
  }
}

B.classes <- na.omit(B.classes)                               # Removing NAs
A.classes <- na.omit(A.classes)

B.classes[length(B.classes)] <- 999           # Replacing 255 with 999: Shows pixels that were 61 or 131 in 2008 or 2017
A.classes[length(A.classes)] <- 999           # and we cannot look outside of that timeseries

rownames(classB) <- B.classes                 # Adding land use classification to their corresponding rows
rownames(classA) <- A.classes

### What crop appears before or after a fallow pixel is observed.

after_csv <- "~/Land_Use_Change_AFTER_WHOLE.csv"
before_csv <- "~/Land_Use_Change_BEFORE_WHOLE.csv"


write.csv(classA,
          after_csv)       # What happens before or after a barren or fallow is observed
write.csv(classB,
          before_csv)