import pandas as pd

ral = pd.read_csv("raleigh.csv")
ral['Date'] = pd.to_datetime(ral['reported_date'])
ral['Year'] = [a.year for a in ral['Date']]


ral = ral.reset_index()
ral = ral[ral["city"] == "RALEIGH"]
ral = ral[ral["Year"] > 2017]

ral['Week'] = ral['Date'].dt.strftime('%U')

ral = ral.reset_index()

codes = pd.read_excel('raleigh_lookup.xlsx')
ral["temp"] = ""
unq_offense_ls = ["SEX OFFENSES","MURDER" , "ASSAULT"]
for i in range(0, len(ral)):

    a = ral["crime_category"][i]
    if a in unq_offense_ls:
                  a = ral["crime_description"][i]

    
    ral["temp"][i] = a
ral = ral.join(codes.set_index('Code'), on = "temp")



ral_agg = ral.groupby(["Year","Week","Offense_grp"]).size().unstack().reset_index()
ral_agg.to_excel("raleigh_agg.xlsx")
