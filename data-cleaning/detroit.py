import pandas as pd


# importing list of codes and descriptions
detroit_codes = pd.read_excel('detroit_lookup.xlsx')
detroit_codes = detroit_codes.set_index('Code')
detroit_codes.index = detroit_codes.index.astype(str, copy = False)

# import city data and get year, week
detroit = pd.read_csv("Detroit.csv")
detroit['Date'] = pd.to_datetime(detroit['incident_timestamp'])
detroit['Year'] = [a.year for a in detroit['Date']]

#Choose year

detroit = detroit[detroit.Year > 2017]

#populate week

detroit['Week'] = detroit['Date'].dt.strftime('%U')




detroit['Offense_group'] = ""

detroit = detroit.reset_index()


for i in range(0, len(detroit)):

    code = str(detroit['state_offense_code'][i])

    try:
        a = detroit_codes.at[code,'Offense_grp']
    except:
        a = " "

    detroit['Offense_group'][i] = a
    
    

#detroit = detroit.drop_duplicates(subset = ["INC NUMBER",'Offense_group']) 
               




detroit_agg = detroit.groupby(['Year','Week','Offense_group']).size().unstack().reset_index()
detroit_agg.to_excel('detroit_agg.xlsx')
detroit.drop(columns=['incident_timestamp'])
#detroit.to_csv('detroit_df.csv')


