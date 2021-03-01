import pandas as pd

# importing list of codes and descriptions
codes = pd.read_excel('Dallas_lookup.xlsx')
codes = codes.set_index('Code')
codes.index = codes.index.astype(str, copy = False)


# import city data and get year, week
dallas = pd.read_csv("dallas.csv")
dallas['Date'] = pd.to_datetime(dallas['Date1 of Occurrence'])
dallas['Year'] = [int(a.year) for a in dallas['Date']]

#delete incidents before 2019
dallas = dallas[dallas.Year > 2017]
dallas = dallas.reset_index()

dallas['Week'] = dallas['Date'].dt.strftime('%U')




dallas['Offense_grp'] = ''


# get offense and offense_detail for each row

for i in range(0,len(dallas)):
    
    
    try:
        code = str(dallas['Type of Incident'][i])
        
        a = codes.at[code,'Offense_grp']
 
        
    except:
        a = ' '


    dallas['Offense_grp'][i] = a


# aggregation (grouping) change as needed

dallas = dallas.drop_duplicates(subset = ["Incident Number w/year",'Offense_grp'])

dallas_agg = dallas.groupby(['Year','Week','Offense_grp']).size().unstack().reset_index()



#writing aggregate and final df to excel
dallas_agg.to_excel('dallas_agg.xlsx')
dallas.to_excel('dallas_df.xlsx')


