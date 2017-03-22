# Read data from ACS tables and merge them into a single ZIP code-level table
library(data.table)
setwd("C:/Users/Daniel/Documents/School/CSE 530/Project 1")

# Read income
income <- read.csv("./ACS Tables/ACS_15_5YR_S1901.csv")
income <- income[, c("GEO.display.label", "HC01_EST_VC13", "HC01_EST_VC15")]
names(income) <- c("Zip", "MedInc", "MeanInc")
income$Zip <- gsub("ZCTA5 ", "", income$Zip, fixed=TRUE)

# Read educational attainment
educ <- read.csv("./ACS Tables/ACS_15_5YR_S1501.csv")
educ <- educ[,c("GEO.display.label", "HC02_EST_VC14")]
names(educ) <- c("Zip", "PctBachelors")
educ$Zip <- gsub("ZCTA5 ", "", educ$Zip, fixed=TRUE)

# Read age and sex
agesex <- read.csv("./ACS Tables/ACS_15_5YR_S0101.csv")
agesex <- agesex[,c("GEO.display.label","HC01_EST_VC01","HC01_EST_VC35","HC02_EST_VC01", "HC03_EST_VC01")]
names(agesex) <- c("Zip","Pop","MedAge","Males","Females")
agesex$MalesPerFemales <- agesex$Males/agesex$Females
agesex$MalesPerFemales <- ifelse(is.finite(agesex$MalesPerFemales),agesex$MalesPerFemales,NA)
agesex$Zip <- gsub("ZCTA5 ", "", agesex$Zip, fixed=TRUE)
agesex <- agesex[,c("Zip","MedAge","MalesPerFemales")]

# Read labor force data
laborforce <- read.csv("./ACS Tables/ACS_15_5YR_S2301.csv")
laborforce <- laborforce[,c("GEO.display.label","HC04_EST_VC01","HC02_EST_VC01")]
names(laborforce) <- c("Zip","Unrate","LFPrate")
laborforce$Zip <- gsub("ZCTA5 ", "", laborforce$Zip, fixed=TRUE)

# Read geography data (county, state)
geogs <- data.table(read.csv("zipCountyState.csv", colClasses=c("character",rep("numeric",23))))
geogs[, maxPopPct := max(ZPOPPCT), by=ZCTA5]
geogs <- geogs[ZPOPPCT == maxPopPct,]
geogs <- geogs[, c("ZCTA5","STATE","COUNTY")]
names(geogs) <- c("Zip","State","County")

# Merge into one zip code table
zip <- merge(educ, income, by="Zip", all.x=TRUE, all.y=TRUE)
zip <- merge(zip, agesex, by="Zip", all.x=TRUE)
zip <- merge(zip, laborforce, by="Zip", all.x=TRUE)
zip <- merge(zip, geogs, by="Zip", all.x=TRUE)

# Save RData format
saveRDS(zip, "zip.RData")

# Export combined file as CSV
write.csv(zip,file="zip.csv",row.names=FALSE,na="NULL")