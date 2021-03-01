import pandas as pd
import numpy as np



cities_ls = ['austin','atlanta','baltimore','boston','chicago',
             'cinncinati','dallas','dc','denver','detroit',
             'houston','kansas_city','la','lincoln','louisville','nashville',
             'ny','phoenix','philly','pitt','sacramento','seattle','sfo','stlouis',
             'stpaul','tulsa','milwaukee','mesa', 'raleigh']


# handling citynames 
cityname_codes = pd.read_excel('citynames_lookup.xlsx')
cityname_codes = cityname_codes.set_index('Code')
cityname_codes.index = cityname_codes.index.astype(str, copy = False)


#-------------------Crime Aggregate---------


# all the different column header names in city_agg files
aggassault_ls = ["AGGRAVATED ASSAULT","Aggravated Assault","AGGRAVATED ASSAULTS","aggravated-assault"]
autotheft_ls = ["AUTO THEFT","Auto Theft","Auto-Theft","AUTO_THEFT","MOTOR VEHICLE THEFT","Vehicle Theft","Auto-theft","auto-theft"
                ,"Auto_Theft",'Motor Vehicle Theft']
homicide_ls = ["Murder","Homicide","Homicide ","MURDER AND NON-NEGLIGENT MANSLAUGHTER","HOMICIDE","murder","hartford",]
rape_ls = ["rape","Rape","RAPE","Forcible Rape"]
robbery_ls = ["robbery","Robbery","ROBBERY"]
larceny_ls = ["Theft","theft","THEFT","Larceny","LARCENY","larceny","LARCENY-THEFT","Larceny Theft"]
resburglary_ls = ["Residential Burglary","burglary-residential","Burglary Residential","Burglary - Residential"]
nonresburglary_ls = ["Non Residential Burglary","Non-Residential Burglary","Non- Residential Burglary","Burglary Non-Residential"]
comburglary_ls = ["Commercial Burglary","burglary-commercial","Burglary Commercial","Burglary - Commercial"]
otherburglary_ls = ["Other Burglary","burglary-other","Burglary - Other","Burglary - Other"]
hotprowlburglary_ls =["Burglary - Hot Prowl"]
generalburglary_ls = ["BURGLARY/BREAKING ENTERING","Burglary","burglary","BURGLARY"]






#initialize final merged df
merge_df = pd.DataFrame(columns= ["City","State","Year","Population","Week","Status Change Date" , "Status Chage Type","Reopen_phase","Openness Index", "Aggravated Assault",
                                  "Auto Theft","Homicide","Rape","Larceny","Robbery","Burglary All","Total Part1","Residential Burglary","Commercial Burglary","Burglary - Unspecified","Non-Residential Burglary","Other Burglary",
                                  "Other Burglary - hotprowl","Arrest: Aggravated Assault", "Arrest: Auto Theft","Arrest: Robbery","Arrest: Larceny",
                                  "Arrest: Burglary", "Arrest: Homicide","Arrest: Rape","Arrest: PartB",
                                  "Lockdown Week", "ReOpen1 Week", "Reopen2 Week",'join_index','wk_lock_index'])

#Collect Crime & Arrest data from agg files

for i in range(0, len(cities_ls)):
    
    helper_df = pd.DataFrame()
    city = cities_ls[i]
    
    city_df = pd.read_excel(city + "_agg.xlsx")
    city_cols = city_df.columns

    
    helper_df["Week"] = city_df["Week"]
    helper_df["Year"] = city_df["Year"]
    helper_df["City"] = cityname_codes.at[city,'City']
    helper_df["State"] = cityname_codes.at[city,'State']
    helper_df["Population"] = cityname_codes.at[city,'Population']
    helper_df["County Population"] = cityname_codes.at[city,'County Population']
    helper_df["city_abbrev"] = city

    for j in range(0,len(city_cols)):

        if city_cols[j] in aggassault_ls:
            helper_df["Aggravated Assault"] = city_df[city_cols[j]]

        elif city_cols[j] in autotheft_ls:
            helper_df["Auto Theft"] = city_df[city_cols[j]]

        elif city_cols[j] in homicide_ls:
            helper_df["Homicide"] = city_df[city_cols[j]]

        elif city_cols[j] in rape_ls:
            helper_df["Rape"] = city_df[city_cols[j]]

        elif city_cols[j] in robbery_ls:
            helper_df["Robbery"] = city_df[city_cols[j]]

        elif city_cols[j] in larceny_ls:
            helper_df["Larceny"] = city_df[city_cols[j]]

        elif city_cols[j] in resburglary_ls:
            helper_df["Residential Burglary"] = city_df[city_cols[j]]

        elif city_cols[j] in nonresburglary_ls:
            helper_df["Non-Residential Burglary"] = city_df[city_cols[j]]
            
        elif city_cols[j] in comburglary_ls:
            helper_df["Commercial Burglary"] = city_df[city_cols[j]]

        elif city_cols[j] in otherburglary_ls:
            helper_df["Other Burglary"] = city_df[city_cols[j]]
            
        elif city_cols[j] in hotprowlburglary_ls:
            helper_df["Other Burglary - hotprowl"] = city_df[city_cols[j]]
                        
        elif city_cols[j] in generalburglary_ls:
            helper_df["Burglary - Unspecified"] = city_df[city_cols[j]]

    merge_df = merge_df.append(helper_df)



    

# Creating unique row id to join to other sources

merge_df = merge_df.reset_index()

for i in range (0,len(merge_df)):
    
    merge_df['join_index'][i] = merge_df['City'][i] + merge_df['State'][i] + str(merge_df['Year'][i]) + str(merge_df['Week'][i])
    merge_df['wk_lock_index'][i] = merge_df['City'][i] + str(merge_df['Year'][i]) + str(merge_df['Week'][i])


#---------lockdown prep-------------

    
lockdown_df = pd.read_excel("cities_lock_open.xlsx")
lockdown_df['index'] = ""
lockdown_df['Date'] = pd.to_datetime(lockdown_df['Change_Date'])
lockdown_df['Year'] = [int(a.year) for a in lockdown_df['Date']]
lockdown_df['Week'] = lockdown_df['Date'].dt.strftime('%U')

for i in range (0,len(lockdown_df)):
    
    lockdown_df['index'][i] = lockdown_df['City'][i] + lockdown_df['State'][i] + str(lockdown_df['Year'][i]) + str(lockdown_df['Week'][i])

lockdown_df = lockdown_df.set_index('index')
lockdown_df.index = lockdown_df.index.astype(str, copy = True)

lockdown_df.index.name = None


#----- adding lockdown

for i in range (0,len(merge_df)):

    code = merge_df['join_index'][i]



    #----lockdown

    try: 
        h = lockdown_df.at[code,"Change_Date"]
        k = lockdown_df.at[code,"Change_Type"]
        kk = lockdown_df.at[code,"Reopen_phase"]
        xyz = lockdown_df.at[code,"Openness Index"]

    except:
        h = ""
        k = ""
        kk = ""
        xyz = "flag"    

    try:
        x = int(lockdown_df.loc[lockdown_df["Change_Type_grp"] == "Lockdown"].at[code,"Week"])

    except:
        x = 0
    try:
        y = int(lockdown_df.loc[lockdown_df["Change_Type_grp"] == "Open1"].at[code,"Week"])


    except:
        y = 0


    try:
        z = int(lockdown_df.loc[lockdown_df["Change_Type_grp"] == "Open2"].at[code,"Week"])


    except:

        z = 0

        
    merge_df["Status Change Date"][i] = h
    merge_df["Status Chage Type"][i] = k
    merge_df["Reopen_phase"][i] = kk
    merge_df["Lockdown Week"][i] = x
    merge_df["ReOpen1 Week"][i] = y
    merge_df["Reopen2 Week"][i] = z

    if xyz != "flag":
        merge_df["Openness Index"][i] = int(xyz)

    elif  merge_df["index"][i] == 0 or i == 0 :
        merge_df["Openness Index"][i] = 14
    else:
        merge_df["Openness Index"][i] = merge_df["Openness Index"][i-1]
        


#some column additions

merge_df.fillna(0, inplace=True)
merge_df["Burglary All"] = (merge_df["Residential Burglary"])  +  (merge_df["Commercial Burglary"])+ merge_df["Burglary - Unspecified"] + merge_df["Non-Residential Burglary"] + merge_df["Other Burglary"] + merge_df["Other Burglary - hotprowl"]
merge_df["Violent Crime"] = merge_df["Rape"] + merge_df["Homicide"] + merge_df["Robbery"] + merge_df["Aggravated Assault"]
merge_df["Violent w/o rape"] =  merge_df["Homicide"] + merge_df["Robbery"] + merge_df["Aggravated Assault"]

merge_df["Non-Violent Crime"] = merge_df["Auto Theft"] + merge_df["Burglary All"] + merge_df["Larceny"]
merge_df["Total Part1"] = merge_df["Aggravated Assault"] + merge_df["Auto Theft"] + merge_df["Homicide"] + merge_df["Rape"] + merge_df["Larceny"] + merge_df["Robbery"] + merge_df["Burglary All"]
merge_df["Total Arrests"] = merge_df["Arrest: Aggravated Assault"] + merge_df["Arrest: Auto Theft"] + merge_df["Arrest: Robbery"] + merge_df["Arrest: Larceny"]+ merge_df["Arrest: Burglary"] + merge_df["Arrest: Homicide"] + merge_df["Arrest: Rape"] + merge_df["Arrest: PartB"]                                                                                                                                          
merge_df["Closeness_Index"] = (merge_df['Openness Index'] - 14).abs()
merge_df = merge_df[merge_df["Year"] > 2017]
merge_df = merge_df[merge_df["Year"] < 2021]


#weeks from lockdown calculation

some_df = pd.DataFrame()
for city in cities_ls:

    

    helper_df = merge_df[merge_df["city_abbrev"] == city]
    helper_df = helper_df[["City","Year","Week","Lockdown Week"]]
    helper_df["Weeks_from_lockdown"] = 0
    lockdown_week = max(helper_df["Lockdown Week"])
    
    helper_df.loc[helper_df["Year"] == 2018,"Weeks_from_lockdown"] = helper_df["Week"] -52 -lockdown_week -52
    helper_df.loc[helper_df["Year"] == 2019,"Weeks_from_lockdown"] = helper_df["Week"] -52 -lockdown_week
    helper_df.loc[helper_df["Year"] == 2020,"Weeks_from_lockdown"] = helper_df["Week"] - lockdown_week
    
    helper_df["index_lckdwn"] = 0
    helper_df = helper_df.reset_index()
    for i in range(0,len(helper_df)):
        helper_df["index_lckdwn"][i] = helper_df["City"][i] + str(helper_df["Year"][i]) + str(helper_df["Week"][i])

    if lockdown_week == 0:
        helper_df["Weeks_from_lockdown"] = "NA"

    helper_df = helper_df[["index_lckdwn","Weeks_from_lockdown"]]
    some_df = some_df.append(helper_df)


merge_df = merge_df.join(some_df.set_index('index_lckdwn'), on='wk_lock_index')



merge_df = merge_df[['City', 'State', 'Year', 'Population', 'Week',  'Openness Index', 'Aggravated Assault', 'Auto Theft', 'Homicide',
       'Rape', 'Larceny', 'Robbery', 'Burglary All', 'Total Part1',
       'Violent Crime',
       'Non-Violent Crime',"Violent w/o rape", 'Closeness_Index',
       'Weeks_from_lockdown' ,'Lockdown Week', 'ReOpen1 Week', 'Reopen2 Week', 'city_abbrev']]


merge_df.to_excel("merge.xlsx")


