library(dplyr)
library(readxl)
library(knitr)
library(miceadds)
library(aods3)
library(car)
library(tidyverse)
library(ggplot2)
library(grid)
library(ggDiagnose)
library(gridExtra)


# all crime: 2018-2020
crime_1820 <- read_excel("crime_3yrs.xlsx")
# remove first and last week of the year since they do not
# fall into any month by our categorization
crime_1820_df <- crime_1820[!(crime_1820$Week_Group == "0"),]
crime_1820_df$Year <- as.factor(crime_1820_df$Year)

# Remove weeks greater than week 38 for 2020
crime_1820_df <- crime_1820_df %>% filter(Week <= 38 | Year != "2020")

# Create new response variables
crime_1820_df$Burglary_avg_byPop <- (crime_1820_df$`Burglary All_avg`*52*100000)/crime_1820_df$Population
crime_1820_df$Burglary_diff_byPop <- (100000*crime_1820_df$`Burglary All`*52)/crime_1820_df$Population - crime_1820_df$Burglary_avg_byPop

# Filter out cities that aren't in top 70
crime_1820_df <- crime_1820_df %>% 
  filter(!City %in% c("Baton Rouge", "Chattanooga",
                      "Gainesville", "Hartford",
                      "Tacoma", "Tempe"))

# Remove first 11 weeks of 2019 for Kansas City due to the
# data being unavailable
crime_1820_df <- crime_1820_df %>% filter(!(City == "Kansas City" & Week %in% 1:11 & Year == "2019"))

# Clean Closeness index to make openness index
crime_1820_df <- mutate(crime_1820_df, 
                        Openness_Index =
                          abs(Closeness_Index - 14))

# Create new variable: 2020 flag to be used in interactions for month model
crime_1820_df$Year_2020 <- ifelse(crime_1820_df$Year == "2020", 1, 0)
crime_1820_df$Month <- as.factor(crime_1820_df$Month) #Otherwise, the first month isn't absorbed

#create data frame for openness index and biweekly lockdown models; stops at week 21
crime_openness <- crime_1820_df %>% filter(Week < min(Week[Surge_Protest_Week == 1]) | Year != "2020") 

#create data frame for openness index; these cities do
#not have openness index data available
crime_openness_idx <- crime_openness %>% filter(!City %in% c("Tulsa", "Mesa",
                                                             "Raleigh", "Milwaukee",
                                                             "Saint Paul"))

# Remove week 21 from St. Paul to check for sensitivity of results
burg_df <- crime_openness %>% filter(City != "Saint Paul" |
                                       Week != 21 | Year != 2020)

##### HERE IS THE MODEL #####
burg_biweek <- lm.cluster(data=burg_df, Burglary_diff_byPop ~ Year + Month + `LD_-1/0` + `LD_1/2` + `LD_3/4` + `LD_5/6` + `LD_7/8` + `LD_9/10`,
                          cluster = 'City')

summary(burg_biweek)

##### Diagnostics

burg_biweek_lm <- lm(data = burg_df, formula=Burglary_diff_byPop ~ Year + Month + `LD_-1/0` + `LD_1/2` + `LD_3/4` + `LD_5/6` + `LD_7/8` + `LD_9/10`)

multi_panel_diag(burg_biweek_lm, "all")


##### Results Plot (Fig. B1)

burg_open_std_errors <- diag(sqrt(vcov(burg_biweek)))
burg_open_graph_df <- data.frame("BiweekVar" = c("-1/0", "1/2",
                                                 "3/4", "5/6",
                                                 "7/8", "9/10"),
                                 "Coef" = coef(burg_biweek)[15:20],
                                 "Upper" = coef(burg_biweek)[15:20] +
                                   (1.96*burg_open_std_errors[15:20]),
                                 "Lower" = coef(burg_biweek)[15:20] -
                                   (1.96*burg_open_std_errors[15:20]))

ggplot(burg_open_graph_df, aes(x = BiweekVar, y = Coef)) +
  geom_point(color = "dark green") + geom_errorbar(aes(ymin = Lower,
                                                       ymax = Upper), color = "dark green") +
  labs(x = "Weeks since Lockdown", y = "Lockdown Impact") +
  geom_hline(yintercept = 0, linetype = "dotted") +
  ylim(-200, 1000)
