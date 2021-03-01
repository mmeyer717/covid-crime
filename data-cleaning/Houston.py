import pandas as pd

# importing list of codes and descriptions
nibrs = pd.read_excel('NIBRS.xlsx')
nibrs = nibrs.set_index('Code')
nibrs.index = nibrs.index.astype(str, copy = False)


# import city data and get year, week
houston = pd.read_excel("houston.xlsx")
houston['Date'] = pd.to_datetime(houston['Occurrence\nDate'])
houston['Year'] = [a.year for a in houston['Date']]
houston['Week'] = houston['Date'].dt.strftime('%U')


houston['Offense_grp'] = ' '


# get offense and offense_detail for each row

for i in range(0,len(houston)):
    
    code = str(houston['NIBRS\nClass'][i])
    try:
        
        a = nibrs.at[code,'Offense_grp']

        
    except:
        a = ' '


    houston['Offense_grp'][i] = a
 

# aggregation (grouping) change as needed

houston_agg = houston.groupby(['Year','Week','Offense_grp'])["Offense\nCount"].sum().unstack().reset_index()


#writing aggregate and final df to excel
houston_agg.to_excel('houston_agg_2020.xlsx')
houston.to_excel('houston_df.xlsx')


