library(readxl)
library(ggplot2)

All_70_UCR <- read_excel("C:/Users/meyer/Downloads/Boxplot Data Used.xlsx",
                         sheet = "All 70 UCR Cities")
##UCR_data_our_cities.allcrime <- read_excel("Boxplot Data Used.xlsx",
#                                           sheet = "UCR Data, Our Cities")
Our_cities_our_data.allcrime <- read_excel("C:/Users/meyer/Downloads/Boxplot Data Used.xlsx",
                                           sheet = "Our cities, our data")

data_sets <- c(rep("UCR Top 70", nrow(All_70_UCR)),
              # rep("UCR Data, Our Cities", nrow(UCR_data_our_cities.allcrime)),
               rep("Our Data, Our Cities", nrow(Our_cities_our_data.allcrime)))

### Fig. C1: Homicide
homicide_df <- data.frame("DataSet" = data_sets,
                          "HomicideRate" = c(All_70_UCR$MurderRate,
                                              #UCR_data_our_cities.allcrime$MurderRate,
                                              Our_cities_our_data.allcrime$Homicide_Rate))

ggplot(homicide_df, aes(x = DataSet, y = HomicideRate)) +
  geom_boxplot() + labs(y = "Homicide Rate") + 
  theme(axis.title.x = element_blank()) + 
  scale_x_discrete(labels=c("Our Data, Our Cities" = 
                              "29 Cities Providing Weekly Crime Data", 
                            "UCR Top 70" = 
                              "Largest 70 Cities (UCR)"))

### Fig. C2: Auto Theft
at_df <- data.frame("DataSet" = data_sets,
                    "ATRate" = c(All_70_UCR$MotorVehicleTheftRate,
                                 #UCR_data_our_cities.allcrime$MotorVehicleTheft,
                                 Our_cities_our_data.allcrime$Auto_Theft_Rate))

ggplot(at_df, aes(x = DataSet, y = ATRate)) +
  geom_boxplot() + labs(y = "Auto Theft Rate") + 
  theme(axis.title.x = element_blank()) + 
  scale_x_discrete(labels=c("Our Data, Our Cities" = 
                              "29 Cities Providing Weekly Crime Data", 
                            "UCR Top 70" = 
                              "Largest 70 Cities (UCR)"))

### Fig. C3: Burglary
burg_df <- data.frame("DataSet" = data_sets,
                      "BurglaryRate" = c(All_70_UCR$Burglaryrate,
                                         #UCR_data_our_cities.allcrime$Burglaryrate,
                                         Our_cities_our_data.allcrime$Burglary_Rate))

ggplot(burg_df, aes(x = DataSet, y = BurglaryRate)) +
  geom_boxplot() + labs(y = "Burglary Rate") + 
  theme(axis.title.x = element_blank()) + 
  scale_x_discrete(labels=c("Our Data, Our Cities" = 
                              "29 Cities Providing Weekly Crime Data", 
                            "UCR Top 70" = 
                              "Largest 70 Cities (UCR)"))

### Fig. C4: Robbery
rob_df <- data.frame("DataSet" = data_sets,
                     "RobberyRate" = c(All_70_UCR$RobberyRate,
                                        #UCR_data_our_cities.allcrime$RobberyRate,
                                        Our_cities_our_data.allcrime$Robbery_Rate))

ggplot(rob_df, aes(x = DataSet, y = RobberyRate)) +
  geom_boxplot() + labs(y = "Robbery Rate") + 
  theme(axis.title.x = element_blank()) + 
  scale_x_discrete(labels=c("Our Data, Our Cities" = 
                              "29 Cities Providing Weekly Crime Data", 
                            "UCR Top 70" = 
                              "Largest 70 Cities (UCR)"))

### Fig. C5: Larceny
larceny_df <- data.frame("DataSet" = data_sets,
                         "LarcenyRate" = c(All_70_UCR$`Larceny/TheftRate`,
                                           # UCR_data_our_cities.allcrime$LarcenyTheftRate,
                                            Our_cities_our_data.allcrime$Larceny_Rate))

ggplot(larceny_df, aes(x = DataSet, y = LarcenyRate)) +
  geom_boxplot() + labs(y = "Larceny Rate") + 
  theme(axis.title.x = element_blank()) + 
  scale_x_discrete(labels=c("Our Data, Our Cities" = 
                              "29 Cities Providing Weekly Crime Data", 
                            "UCR Top 70" = 
                              "Largest 70 Cities (UCR)"))
