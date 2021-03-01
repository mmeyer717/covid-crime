import pandas as pd




# import city data and get year, week
cinncinati = pd.read_csv("cinncinati.csv")
cinncinati['Date'] = pd.to_datetime(cinncinati['DATE_FROM'])
cinncinati['Year'] = [a.year for a in cinncinati['Date']]

cinncinati = cinncinati[cinncinati.Year > 2017]

#homicide exclusion
hom_excl_ls = ["INVOL MANSLAUGHTER - RESULT OF MISDEMEANOR", "NEGLIGENT HOMICIDE",
               "INVOLUNTARY MANSLAUGHTER", "RECKLESS HOMICIDE"]

cinncinati = cinncinati[~cinncinati.OFFENSE.isin(hom_excl_ls)]

cinncinati['Week'] = cinncinati['Date'].dt.strftime('%U')

cinncinati = cinncinati.reset_index()

cinncinati["offense_grp"] = cinncinati["UCR_GROUP"]

cinncinati = cinncinati.reset_index()
for i in range(0,len(cinncinati)):
    if cinncinati["offense_grp"][i] == "THEFT":
        theft_type = str(cinncinati["THEFT_CODE"][i])
        if theft_type == "24O-MOTOR VEHICLE THEFT":
            cinncinati["offense_grp"][i] = "Auto Theft"
            
        
        
    

cinncinati = cinncinati.drop_duplicates(subset = ["INSTANCEID","INCIDENT_NO",'offense_grp'])           




cinncinati_agg = cinncinati.groupby(['Year','Week','offense_grp']).size().unstack().reset_index()
cinncinati_agg.to_excel('cinncinati_agg.xlsx')
cinncinati.to_excel('cinncinati_df.xlsx')
