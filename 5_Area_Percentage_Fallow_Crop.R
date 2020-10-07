# [Title]: Calulate area and percentages
# [Subtitle]: States and Ecoregions
# [Author]: Kevin Neal and Sophie Plassin


### Data importing and formating
# Importing every CSV file that starts with "crop_eco" and "crop_state" and storing it in one variable

name.path.eco <- "~/crop_ecoregion/"
path.ecoregions <- list.files(path = name.path.eco, # Creates a vector of path names
                              pattern = ".csv" ,    # The pattern is whatever starts with "crop_eco"
                              full.names = F)


name.path.state <- "~/crop_state/"
path.states <- list.files(path = name.path.state,
                              pattern = ".csv" ,
                              full.names = F)


crop.eco.path <-

crop.state.path <-

# List index ecoregions and States
ecoregions.id <- c("99"  , "941"  , "943"  , "946"  , "951" ,
                   "961" , "1017" , "1024" , "1311" , "6214")

states.id <- c("99"  , "08"  , "35"  , "48")

sorted.path.eco <- rep(NA , length(path.ecoregions))

sorted.path.states <- rep(NA , length(path.states))


# Ecoregion sort index
for(i in 1 : length(path.ecoregions)){
  temp <- gsub("crop_eco" , "" , path.ecoregions[i])
  temp <- gsub(".csv" , "" , temp)

  sorted.index <- which(ecoregions.id == temp)

  sorted.path.eco[sorted.index] <- path.ecoregions[i]
}

sorted.path.eco <- paste(name.path.eco,
                         sorted.path.eco ,
                     sep = "")

ecoregions.list <- sapply(sorted.path.eco ,                                                  # Creates a list containing every .csv
                          read.csv ,
                          simplify = F)

# State sort index
for(i in 1 : length(path.states)){
  temp <- gsub("crop_state" , "" , path.states[i])
  temp <- gsub(".csv" , "" , temp)

  sorted.index <- which(states.id == temp)

  sorted.path.states[sorted.index] <- path.states[i]
}

sorted.path.states <- paste(name.path.state,
                     sorted.path.states ,
                     sep = "")

states.list <- sapply(sorted.path.states ,                                                  # Creates a list containing every .csv
                          read.csv ,
                          simplify = F)


# Creating vectors and functions for analysis
years <- c(2008 : 2018)
ecoregions <- c("Ecoregion 99"  , "Ecoregion 941"  , "Ecoregion 943"  , "Ecoregion 946"  , "Ecoregion 951" ,
                "Ecoregion 961" , "Ecoregion 1017" , "Ecoregion 1024" , "Ecoregion 1311" , "Ecoregion 6214")
names(ecoregions.list) <- ecoregions                                                        # Changes the name to something shorter than the path name


states <- c("State 99"  , "State 08"  , "State 35"  , "State 48")
names(states.list) <- states                                                        # Changes the name to something shorter than the path name



crops.total.fun <- function(df){
  crop.id.list <- c(1:60 , 66:77 , 204:254)                 # Creates a list of ID numbers that are considered crops:
                                                            # [ID]: 1 - 60
                                                            # [ID]: 66 - 77
                                                            # [ID]: 204 - 254
  crops.totals <- NA                        # Initializes vector to add values into

  # Loop to cycle through each year (2008 - 2018)
  for(i in 1 : length(df)){
    crops.totals[i] <- sum(df[, i] %in% crop.id.list == T)  # Appends the total pixels that are crops each year into a vector
  }

  return(crops.totals)
}

fallow.total.fun <- function(df){
  fallow.id <- 61                            # Initialize fallow pixel ID variable
  fallow.totals <- NA                        # Initialize fallow vector to add values

  # Loop to cycle through each year (2008 - 2018)
  for(i in 1 : length(df)){
    fallow.totals[i] <- sum(df[, i] == 61)   # Appends the total pixels that are fallow each year into a vector
  }

  return(fallow.totals)
}


max.extent.fun <- function(df){
  max.id.list <- c(1:254)                 # Creates a list of ID numbers that are considered crops:
  max.totals <- NA                        # Initializes vector to add values into

  # Loop to cycle through each year (2008 - 2018)
  for(i in 1 : length(df)){
    max.totals[i] <- sum(df[, i] %in% max.id.list == T)  # Appends the total pixels that are crops each year into a vector
  }

  return(max.totals)
}


# Creating data frames to store information about each year for each ecoregion

# fallow.sum: all pixels classified at least once as fallow/idle land between 2008 and 2018
df.fallow.sum.eco <- data.frame(ecoregions = ecoregions ,
                            cdl2008 = rep(NA , 10) , cdl2009 = rep(NA , 10) , cdl2010 = rep(NA , 10) ,
                            cdl2011 = rep(NA , 10) , cdl2012 = rep(NA , 10) , cdl2013 = rep(NA , 10) ,
                            cdl2014 = rep(NA , 10) , cdl2015 = rep(NA , 10) , cdl2016 = rep(NA , 10) ,
                            cdl2017 = rep(NA , 10) , cdl2018 = rep(NA , 10))

# crop.sum: all pixels classified at least once as cropland between 2008 and 2018
df.crop.sum.eco <- data.frame(ecoregions = ecoregions ,
                          cdl2008 = rep(NA , 10) , cdl2009 = rep(NA , 10) , cdl2010 = rep(NA , 10) ,
                          cdl2011 = rep(NA , 10) , cdl2012 = rep(NA , 10) , cdl2013 = rep(NA , 10) ,
                          cdl2014 = rep(NA , 10) , cdl2015 = rep(NA , 10) , cdl2016 = rep(NA , 10) ,
                          cdl2017 = rep(NA , 10) , cdl2018 = rep(NA , 10))

# Other.sum: all pixels classified at least once as other between 2008 and 2018
df.other.sum.eco <- data.frame(ecoregions = ecoregions ,
                               cdl2008 = rep(NA , 10) , cdl2009 = rep(NA , 10) , cdl2010 = rep(NA , 10) ,
                               cdl2011 = rep(NA , 10) , cdl2012 = rep(NA , 10) , cdl2013 = rep(NA , 10) ,
                               cdl2014 = rep(NA , 10) , cdl2015 = rep(NA , 10) , cdl2016 = rep(NA , 10) ,
                               cdl2017 = rep(NA , 10) , cdl2018 = rep(NA , 10))

# max.extent.fallow: Proportion of fallow land in the maximum agricultural areal extent
# (area of fallow divided by the maximum agricultural areal extent,
# i.e. all pixels classified at least once as cropland or fallow/idle land between 2008 and 2018)
df.max.extent.fallow.eco <- data.frame(ecoregions = ecoregions ,
                             cdl2008 = rep(NA , 10) , cdl2009 = rep(NA , 10) , cdl2010 = rep(NA , 10) ,
                             cdl2011 = rep(NA , 10) , cdl2012 = rep(NA , 10) , cdl2013 = rep(NA , 10) ,
                             cdl2014 = rep(NA , 10) , cdl2015 = rep(NA , 10) , cdl2016 = rep(NA , 10) ,
                             cdl2017 = rep(NA , 10) , cdl2018 = rep(NA , 10))

# max.extent.crop: Proportion of crop land in the maximum agricultural areal extent
# (area of cropland divided by the maximum agricultural areal extent,
# i.e. all pixels classified at least once as cropland or fallow/idle land between 2008 and 2018)
df.max.extent.crop.eco <- data.frame(ecoregions = ecoregions ,
                                     cdl2008 = rep(NA , 10) , cdl2009 = rep(NA , 10) , cdl2010 = rep(NA , 10) ,
                                     cdl2011 = rep(NA , 10) , cdl2012 = rep(NA , 10) , cdl2013 = rep(NA , 10) ,
                                     cdl2014 = rep(NA , 10) , cdl2015 = rep(NA , 10) , cdl2016 = rep(NA , 10) ,
                                     cdl2017 = rep(NA , 10) , cdl2018 = rep(NA , 10))


# max.extent.other: Proportion of other land in the maximum agricultural areal extent
# (area of other divided by the maximum agricultural areal extent,
# i.e. all pixels classified at least once as cropland or fallow/idle land between 2008 and 2018)
df.max.extent.other.eco <- data.frame(ecoregions = ecoregions ,
                                      cdl2008 = rep(NA , 10) , cdl2009 = rep(NA , 10) , cdl2010 = rep(NA , 10) ,
                                      cdl2011 = rep(NA , 10) , cdl2012 = rep(NA , 10) , cdl2013 = rep(NA , 10) ,
                                      cdl2014 = rep(NA , 10) , cdl2015 = rep(NA , 10) , cdl2016 = rep(NA , 10) ,
                                      cdl2017 = rep(NA , 10) , cdl2018 = rep(NA , 10))

# area.fallow: Proportion of fallow land divided by the yearly area of crops + fallow
df.area.fallow.eco <- data.frame(ecoregions = ecoregions ,
                                 cdl2008 = rep(NA , 10) , cdl2009 = rep(NA , 10) , cdl2010 = rep(NA , 10) ,
                                 cdl2011 = rep(NA , 10) , cdl2012 = rep(NA , 10) , cdl2013 = rep(NA , 10) ,
                                 cdl2014 = rep(NA , 10) , cdl2015 = rep(NA , 10) , cdl2016 = rep(NA , 10) ,
                                 cdl2017 = rep(NA , 10) , cdl2018 = rep(NA , 10))

# area.crop: Proportion of cropland divided by the yearly area of crops + fallow
df.area.crop.eco <- data.frame(ecoregions = ecoregions ,
                                 cdl2008 = rep(NA , 10) , cdl2009 = rep(NA , 10) , cdl2010 = rep(NA , 10) ,
                                 cdl2011 = rep(NA , 10) , cdl2012 = rep(NA , 10) , cdl2013 = rep(NA , 10) ,
                                 cdl2014 = rep(NA , 10) , cdl2015 = rep(NA , 10) , cdl2016 = rep(NA , 10) ,
                                 cdl2017 = rep(NA , 10) , cdl2018 = rep(NA , 10))

# Creating data frames to store information about each year for each state
# fallow.sum: all pixels classified at least once as fallow/idle land between 2008 and 2018
df.fallow.sum.state <- data.frame(states = states ,
                            cdl2008 = rep(NA , 4) , cdl2009 = rep(NA , 4) , cdl2010 = rep(NA , 4) ,
                            cdl2011 = rep(NA , 4) , cdl2012 = rep(NA , 4) , cdl2013 = rep(NA , 4) ,
                            cdl2014 = rep(NA , 4) , cdl2015 = rep(NA , 4) , cdl2016 = rep(NA , 4) ,
                            cdl2017 = rep(NA , 4) , cdl2018 = rep(NA , 4))

# crop.sum: all pixels classified at least once as cropland between 2008 and 2018
df.crop.sum.state <- data.frame(states = states ,
                                cdl2008 = rep(NA , 4) , cdl2009 = rep(NA , 4) , cdl2010 = rep(NA , 4) ,
                                cdl2011 = rep(NA , 4) , cdl2012 = rep(NA , 4) , cdl2013 = rep(NA , 4) ,
                                cdl2014 = rep(NA , 4) , cdl2015 = rep(NA , 4) , cdl2016 = rep(NA , 4) ,
                                cdl2017 = rep(NA , 4) , cdl2018 = rep(NA , 4))

# Other.sum: all pixels classified at least once as other between 2008 and 2018
df.other.sum.state <- data.frame(states = states ,
                                 cdl2008 = rep(NA , 4) , cdl2009 = rep(NA , 4) , cdl2010 = rep(NA , 4) ,
                                 cdl2011 = rep(NA , 4) , cdl2012 = rep(NA , 4) , cdl2013 = rep(NA , 4) ,
                                 cdl2014 = rep(NA , 4) , cdl2015 = rep(NA , 4) , cdl2016 = rep(NA , 4) ,
                                 cdl2017 = rep(NA , 4) , cdl2018 = rep(NA , 4))


# max.extent.fallow: Proportion of fallow land in the maximum agricultural areal extent
# (area of fallow divided by the maximum agricultural areal extent,
# i.e. all pixels classified at least once as cropland or fallow/idle land between 2008 and 2018)
df.max.extent.fallow.state <- data.frame(states = states ,
                                         cdl2008 = rep(NA , 4) , cdl2009 = rep(NA , 4) , cdl2010 = rep(NA , 4) ,
                                         cdl2011 = rep(NA , 4) , cdl2012 = rep(NA , 4) , cdl2013 = rep(NA , 4) ,
                                         cdl2014 = rep(NA , 4) , cdl2015 = rep(NA , 4) , cdl2016 = rep(NA , 4) ,
                                         cdl2017 = rep(NA , 4) , cdl2018 = rep(NA , 4))


# max.extent.crop: Proportion of crop land in the maximum agricultural areal extent
# (area of cropland divided by the maximum agricultural areal extent,
# i.e. all pixels classified at least once as cropland or fallow/idle land between 2008 and 2018)
df.max.extent.crop.state <- data.frame(states = states ,
                                       cdl2008 = rep(NA , 4) , cdl2009 = rep(NA , 4) , cdl2010 = rep(NA , 4) ,
                                       cdl2011 = rep(NA , 4) , cdl2012 = rep(NA , 4) , cdl2013 = rep(NA , 4) ,
                                       cdl2014 = rep(NA , 4) , cdl2015 = rep(NA , 4) , cdl2016 = rep(NA , 4) ,
                                       cdl2017 = rep(NA , 4) , cdl2018 = rep(NA , 4))


# max.extent.other: Proportion of other land in the maximum agricultural areal extent
# (area of other divided by the maximum agricultural areal extent,
# i.e. all pixels classified at least once as cropland or fallow/idle land between 2008 and 2018)
df.max.extent.other.state <- data.frame(states = states ,
                                        cdl2008 = rep(NA , 4) , cdl2009 = rep(NA , 4) , cdl2010 = rep(NA , 4) ,
                                        cdl2011 = rep(NA , 4) , cdl2012 = rep(NA , 4) , cdl2013 = rep(NA , 4) ,
                                        cdl2014 = rep(NA , 4) , cdl2015 = rep(NA , 4) , cdl2016 = rep(NA , 4) ,
                                        cdl2017 = rep(NA , 4) , cdl2018 = rep(NA , 4))



# area.fallow: Proportion of fallow land divided by the yearly area of crops + fallow
df.area.fallow.state <- data.frame(states = states ,
                                   cdl2008 = rep(NA , 4) , cdl2009 = rep(NA , 4) , cdl2010 = rep(NA , 4) ,
                                   cdl2011 = rep(NA , 4) , cdl2012 = rep(NA , 4) , cdl2013 = rep(NA , 4) ,
                                   cdl2014 = rep(NA , 4) , cdl2015 = rep(NA , 4) , cdl2016 = rep(NA , 4) ,
                                   cdl2017 = rep(NA , 4) , cdl2018 = rep(NA , 4))

# area.crop: Proportion of cropland divided by the yearly area of crops + fallow
df.area.crop.state <- data.frame(states = states ,
                                   cdl2008 = rep(NA , 4) , cdl2009 = rep(NA , 4) , cdl2010 = rep(NA , 4) ,
                                   cdl2011 = rep(NA , 4) , cdl2012 = rep(NA , 4) , cdl2013 = rep(NA , 4) ,
                                   cdl2014 = rep(NA , 4) , cdl2015 = rep(NA , 4) , cdl2016 = rep(NA , 4) ,
                                   cdl2017 = rep(NA , 4) , cdl2018 = rep(NA , 4))


### Loop to store all of the information in their respective data frames
for(i in 1 : length(ecoregions.list)){
  ecoregion <- names(ecoregions.list)[i]                                      # Selects the name of a csv within the ecoregions.list
  ecoregion.index <- match(ecoregion , ecoregions)                            # Finds the row index with the respective ecoregion

  df.ecoregion <- ecoregions.list[[i]]                                        # Creates a data frame from the CSV's stored in ecoregions.list
  df.ecoregion <- df.ecoregion[, (startsWith(names(df.ecoregion) , "CDL")) == T] # Formats data frame to only the columns starting with "CDL"

  crops.totals <- crops.total.fun(df.ecoregion)                   # Creates a vector that sums up the total crop pixels observed that year
  fallow.totals <- fallow.total.fun(df.ecoregion)                 # Creates a vector that sums up the total fallow pixels observed that year

  max.totals <- max.extent.fun(df.ecoregion)

  # These lines are saving those vectors into the respected ecoregion row of each data frame
  df.crop.sum.eco[ecoregion.index , c(2 : length(df.crop.sum.eco))]       <- crops.totals
  df.fallow.sum.eco[ecoregion.index , c(2 : length(df.fallow.sum.eco))]   <- fallow.totals
  df.other.sum.eco[ecoregion.index , c(2 : length(df.other.sum.eco))] <- max.totals - (fallow.totals + crops.totals) # Calculates other totals for each year

  df.area.fallow.eco[ecoregion.index , c(2 : length(df.area.fallow.eco))] <- round((fallow.totals / (crops.totals + fallow.totals)) * 100 ,
                                                                           digits = 2)
  df.area.crop.eco[ecoregion.index , c(2 : length(df.area.crop.eco))] <- round((crops.totals / (crops.totals + fallow.totals)) * 100 ,
                                                                                   digits = 2)
  df.max.extent.fallow.eco[ecoregion.index , c(2 : length(df.fallow.sum.eco))] <- round((fallow.totals / max.totals) * 100 ,
                                                                                digits = 2)
  df.max.extent.crop.eco[ecoregion.index , c(2 : length(df.crop.sum.eco))] <- round((crops.totals / max.totals) * 100 ,
                                                                              digits = 2)
  df.max.extent.other.eco[ecoregion.index , c(2 : length(df.other.sum.eco))] <- round(((max.totals - (fallow.totals + crops.totals)) / max.totals) * 100 ,
                                                                                digits = 2)

}


### Loop to store all of the information in their respective data frames
for(i in 1 : length(states.list)){
  state <- names(states.list)[i]                                      # Selects the name of a csv within the states.list
  state.index <- match(state , states)                            # Finds the row index with the respective state

  df.state <- states.list[[i]]                                        # Creates a data frame from the CSV's stored in states.list
  df.state <- df.state[, (startsWith(names(df.state) , "CDL")) == T] # Formats data frame to only the columns starting with "CDL"

  crops.totals <- crops.total.fun(df.state)                   # Creates a vector that sums up the total crop pixels observed that year
  fallow.totals <- fallow.total.fun(df.state)                 # Creates a vector that sums up the total fallow pixels observed that year

  max.totals <- max.extent.fun(df.state)

  # These lines are saving those vectors into the respected ecoregion row of each data frame
  df.crop.sum.state[state.index , c(2 : length(df.crop.sum.state))]       <- crops.totals
  df.fallow.sum.state[state.index , c(2 : length(df.fallow.sum.state))]   <- fallow.totals
  df.other.sum.state[state.index , c(2 : length(df.other.sum.state))] <- max.totals - (fallow.totals + crops.totals) # Calculates other totals for each year

  df.area.fallow.state[state.index , c(2 : length(df.area.fallow.state))] <- round((fallow.totals / (crops.totals + fallow.totals)) * 100 ,
                                                                           digits = 2)
  df.area.crop.state[state.index , c(2 : length(df.area.crop.state))] <- round((crops.totals / (crops.totals + fallow.totals)) * 100 ,
                                                                               digits = 2)
  df.max.extent.fallow.state[state.index , c(2 : length(df.fallow.sum.state))] <- round((fallow.totals / max.totals) * 100 ,
                                                                                digits = 2)
  df.max.extent.crop.state[state.index , c(2 : length(df.crop.sum.state))] <- round((crops.totals / max.totals) * 100 ,
                                                                                    digits = 2)
  df.max.extent.other.state[state.index , c(2 : length(df.other.sum.state))] <- round(((max.totals - (fallow.totals + crops.totals)) / max.totals) * 100 ,
                                                                                      digits = 2)

}


#

### Saving crop_eco CSV
write.csv(df.crop.sum.eco ,
         "~/Area_Crop[ecoregions].csv" ,
         row.names = F)
write.csv(df.fallow.sum.eco ,
          "~/Area_Fallow[ecoregions].csv" ,
          row.names = F)
write.csv(df.other.sum.eco ,
          "~/Area_Other[ecoregions].csv" ,
          row.names = F)
write.csv(df.area.fallow.eco ,
          "~/Percent_Fallow_TotalYear[ecoregions].csv" ,
          row.names = F)
write.csv(df.area.crop.eco ,
          "~/Percent_Crop_TotalYear[ecoregions].csv" ,
          row.names = F)
write.csv(df.max.extent.fallow.eco ,
          "~/Percent_Fallow_MaxExtent[ecoregions].csv" ,
          row.names = F)
write.csv(df.max.extent.crop.eco ,
          "~/Percent_Crop_MaxExtent[ecoregions].csv" ,
          row.names = F)
write.csv(df.max.extent.other.eco ,
          "~/Percent_Other_MaxExtent[ecoregions].csv" ,
          row.names = F)


### Saving crop_state CSV
write.csv(df.crop.sum.state ,
          "~/Area_Crop[states].csv" ,
          row.names = F)
write.csv(df.fallow.sum.state ,
          "~/Area_Fallow[states].csv" ,
          row.names = F)
write.csv(df.other.sum.state ,
          "~/Area_Other[states].csv" ,
          row.names = F)
write.csv(df.area.fallow.state ,
          "~/Percent_Fallow_TotalYear[states].csv" ,
          row.names = F)
write.csv(df.area.crop.state ,
          "~/Percent_Crop_TotalYear[states].csv" ,
          row.names = F)
write.csv(df.max.extent.fallow.state ,
          "~/Percent_Fallow_MaxExtent[states].csv" ,
          row.names = F)
write.csv(df.max.extent.crop.state ,
          "~/Percent_Crop_MaxExtent[states].csv" ,
          row.names = F)
write.csv(df.max.extent.other.state ,
          "~/Percent_Other_MaxExtent[states].csv" ,
          row.names = F)





