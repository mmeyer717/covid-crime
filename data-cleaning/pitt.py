import pandas as pd

# importing list of codes and descriptions
codes = pd.read_excel('Pitt_lookup.xlsx')
codes = codes.set_index('Code')
codes.index = codes.index.astype(str, copy = False)


# import city data and get year, week
pitt = pd.read_csv("Pitt.csv")
pitt['Date'] = pd.to_datetime(pitt['INCIDENTTIME'])
pitt['Year'] = [int(a.year) for a in pitt['Date']]

#delete incidents before 2019
pitt = pitt[pitt.Year > 2017]
pitt = pitt.reset_index()

pitt['Week'] = pitt['Date'].dt.strftime('%U')




pitt['Offense_grp'] = ''


# get offense and offense_detail for each row

for i in range(0,len(pitt)):
    
    
    try:
        code = str(int(pitt['HIERARCHY'][i]))

        if code == "7":
            code = str(pitt["INCIDENTHIERARCHYDESC"][i])
        
        a = codes.at[code,'Offense_grp']
 
        
    except:
        a = ' '


    pitt['Offense_grp'][i] = a


# aggregation (grouping) change as needed

pitt_agg = pitt.groupby(['Year','Week','Offense_grp']).size().unstack().reset_index()



#writing aggregate and final df to excel
pitt_agg.to_excel('pitt_agg.xlsx')
pitt.to_excel('pitt_df.xlsx')


