import pandas as pd

merge_df = pd.read_excel('merge.xlsx')



#Modelling aid-----------------------


#week groupings

d = {range(1, 5): "1", range(5, 9): "2", range(9, 13): '3' , range(13, 17): "4" , range(17, 21): "5", range(21, 25): "6" , range(25, 29): "7" ,
     range(29, 33): "8" , range(33, 37): "9" , range(37,41): "10", range(41,45): "11", range(45, 49) : "12" , range(49,52): "13"}

m = {range(1, 5): "1", range(5, 9): "2", range(9, 13): '3' , range(13, 18): "4" , range(18, 22): "5"
     , range(22, 26): "6" , range(26, 31): "7"
     ,
     range(31, 35): "8" , range(35, 40): "9" , range(40,44): "10", range(44,48): "11", range(48, 52) : "12"}



merge_df['Week_Group'] = merge_df['Week'].apply(lambda x: next((v for k, v in d.items() if x in k), 0))


merge_df['Month'] = merge_df['Week'].apply(lambda x: next((v for k, v in m.items() if x in k), 0))

# Normalize: Population,crime count normalized by population----------------------------------------

offense_ls = ["Aggravated Assault","Auto Theft","Homicide","Rape","Larceny","Robbery","Burglary All","Violent Crime",
              "Total Part1"]
hom_ls = ["Aggravated Assault","Auto Theft","Homicide","Rape","Larceny","Robbery","Burglary All","Violent Crime","Violent w/o rape","Non-Violent Crime"]



for o in offense_ls:

    merge_df["PP_" + o] = (merge_df[o].div(merge_df["Population"])) *100000

#Homicide 3 years normalized by 2018
#Calculating 2018 averages for Homicide for 2018 cities
hom_merge = merge_df
incomplete_cities_ls = ["Tucson" , "Tempe" , "Fort Worth"]
hom_merge = hom_merge[~(hom_merge["City"].isin(incomplete_cities_ls))]
hom_helper_avgs_df = hom_merge[["City",'Year','Week', "Aggravated Assault","Auto Theft","Homicide","Rape","Larceny","Robbery","Burglary All","Violent Crime","Violent w/o rape","Non-Violent Crime"]]
hom_df_2018 = hom_helper_avgs_df[hom_helper_avgs_df["Year"] == 2018]
hom_df_2019 = hom_helper_avgs_df[hom_helper_avgs_df["Year"] == 2019]
hom_df_2020 = hom_helper_avgs_df[hom_helper_avgs_df["Year"] == 2020]

#removing first and last week of 2018 from avg
hom_df_2018 = hom_df_2018[~(hom_df_2018['Week'] == 52)]
hom_df_2018 = hom_df_2018[~(hom_df_2018['Week'] == 0)]

#2018 averages

hom_avgs_df = hom_df_2018.groupby(['City']).mean().reset_index()

hom_merge = hom_merge.join(hom_avgs_df.set_index('City'), on='City', rsuffix = '_avg')






for o in hom_ls:

    hom_merge[o + "_avg_byPop"] = hom_merge[o + "_avg"].div(hom_merge["Population"])

for o in hom_ls:

    hom_merge[o + "_norm_new"] = hom_merge[o].div(hom_merge[o + "_avg_byPop"])


hom_merge = hom_merge[['City', 'State', 'Year', 'Population', 'Week','Month','Week_Group','Aggravated Assault', 'Auto Theft', 'Homicide', 'Rape', 'Larceny',
       'Robbery', 'Burglary All', 'Violent Crime', 'Non-Violent Crime',"Violent w/o rape","Non-Violent Crime",
       'Total Part1','Aggravated Assault_avg',
       'Auto Theft_avg', 'Homicide_avg', 'Rape_avg', 'Larceny_avg',
       'Robbery_avg', 'Burglary All_avg', 'Violent Crime_avg',"Violent w/o rape_avg","Non-Violent Crime_avg",
       'Weeks_from_lockdown','Closeness_Index']]


hom_merge["Pre_Lockdown_Flag"] = 0
hom_merge["LD_-1/0"] = 0
hom_merge["LD_1/2"] = 0
hom_merge["LD_3/4"] = 0
hom_merge["LD_5/6"] = 0
hom_merge["LD_7/8"] = 0
hom_merge["LD_9/10"] = 0
hom_merge["LD_11/14"] = 0
hom_merge["LD_15/18"] = 0
hom_merge["LD_19/22"] = 0
hom_merge["Surge_Protest_Week"] = 0
hom_merge.loc[(hom_merge["Weeks_from_lockdown"] < 0) ,"Pre_Lockdown_Flag"] = 1
hom_merge.loc[(hom_merge["Weeks_from_lockdown"] == -1) | (hom_merge["Weeks_from_lockdown"] == 0) ,"LD_-1/0"] = 1
hom_merge.loc[(hom_merge["Weeks_from_lockdown"] == 1) | (hom_merge["Weeks_from_lockdown"] == 2) ,"LD_1/2"] = 1
hom_merge.loc[(hom_merge["Weeks_from_lockdown"] == 3) | (hom_merge["Weeks_from_lockdown"] == 4) ,"LD_3/4"] = 1
hom_merge.loc[(hom_merge["Weeks_from_lockdown"] == 5) | (hom_merge["Weeks_from_lockdown"] == 6) ,"LD_5/6"] = 1
hom_merge.loc[(hom_merge["Weeks_from_lockdown"] == 7) | (hom_merge["Weeks_from_lockdown"] == 8) ,"LD_7/8"] = 1
hom_merge.loc[(hom_merge["Weeks_from_lockdown"] == 9) | (hom_merge["Weeks_from_lockdown"] == 10) ,"LD_9/10"] = 1
hom_merge.loc[(hom_merge["Weeks_from_lockdown"] == 11) | (hom_merge["Weeks_from_lockdown"] == 12) | (hom_merge["Weeks_from_lockdown"] == 13) | (hom_merge["Weeks_from_lockdown"] == 14) ,"LD_11/14"] = 1
hom_merge.loc[(hom_merge["Weeks_from_lockdown"] == 15) | (hom_merge["Weeks_from_lockdown"] == 16) | (hom_merge["Weeks_from_lockdown"] == 17) | (hom_merge["Weeks_from_lockdown"] == 18) ,"LD_15/18"] = 1
hom_merge.loc[(hom_merge["Weeks_from_lockdown"] == 19) | (hom_merge["Weeks_from_lockdown"] == 20) | (hom_merge["Weeks_from_lockdown"] == 22) | (hom_merge["Weeks_from_lockdown"] == 21) ,"LD_19/22"] = 1

hom_merge.loc[(hom_merge["Year"] == 2020) & (merge_df["Week"] == 22) ,"Surge_Protest_Week"] = 1


hom_merge.to_excel("crime_3yrs.xlsx")
 



hom_merge = hom_merge[['City', 'Year','Aggravated Assault', 'Auto Theft', 'Homicide', 'Rape', 'Larceny',
       'Robbery', 'Burglary All']]

year_agg = hom_merge.groupby(['Year','City']).sum()
year_agg.to_excel("year_agg.xlsx")


