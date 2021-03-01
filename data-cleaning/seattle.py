import pandas as pd

# importing list of codes and descriptions
nibrs = pd.read_excel('NIBRS.xlsx')
nibrs = nibrs.set_index('Code')
nibrs.index = nibrs.index.astype(str, copy = False)


# import city data and get year, week
seattle = pd.read_csv("seattle.csv")
seattle['Date'] = pd.to_datetime(seattle['Report DateTime'])
seattle['Year'] = [a.year for a in seattle['Date']]
seattle['Week'] = seattle['Date'].dt.strftime('%U')


seattle['Offense_grp'] = ' '


seattle = seattle[seattle.Year > 2017]
seattle = seattle.reset_index()

# get offense and offense_detail for each row

for i in range(0,len(seattle)):
    
    code = seattle['Offense Code'][i]
    try:
        
        a = nibrs.at[code,'Offense_grp']

        
    except:
        a = ' '


    seattle['Offense_grp'][i] = a


# aggregation (grouping) change as needed

seattle_agg = seattle.groupby(['Year','Week','Offense_grp']).size().unstack().reset_index()


#writing aggregate and final df to excel
seattle_agg.to_excel('seattle_agg.xlsx')
seattle.to_excel('seattle_df.xlsx')


