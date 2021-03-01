import pandas as pd

# importing list of codes and descriptions
codes = pd.read_excel('Chicago_lookup.xlsx')
codes = codes.set_index('Code')
codes.index = codes.index.astype(str, copy = False)


# import city data and get year, week
chicago = pd.read_csv("chicago.csv")
chicago['Date'] = pd.to_datetime(chicago['Date'])
chicago['Year'] = [int(a.year) for a in chicago['Date']]

#delete incidents before 2018
chicago = chicago[chicago.Year > 2017]
chicago = chicago.reset_index()

chicago['Week'] = chicago['Date'].dt.strftime('%U')


chicago = chicago.join(codes, on = str("IUCR"))

"""
chicago['Offense_grp'] = ''


# get offense and offense_detail for each row

for i in range(0,len(chicago)):
    
    
    try:
        code = str(chicago['IUCR'][i])
        
        a = codes.at[code,'Offense_grp']
 
        
    except:
        a = 'PartB'


    chicago['Offense_grp'][i] = a

"""


# aggregation (grouping) change as needed

chicago_agg = chicago.groupby(['Year','Week','Offense_grp']).size().unstack().reset_index()



#arrest data
chicago['arrest_num'] = [1 if x  else 0 for x in chicago['Arrest']]

chicago_arr_agg = chicago.groupby(['Year','Week','Offense_grp'])['arrest_num'].sum().unstack().reset_index()

#writing aggregate and final df to excel
chicago_agg.to_excel('chicago_agg.xlsx')
chicago_arr_agg.to_excel('chicago_arr_agg.xlsx')
chicago.to_excel('chicago_df.xlsx')


