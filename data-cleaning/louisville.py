import pandas as pd

# importing list of codes and descriptions
nibrs = pd.read_excel('NIBRS.xlsx')
nibrs = nibrs.set_index('Code')
nibrs.index = nibrs.index.astype(str, copy = False)


# import city data and get year, week
louisville = pd.read_csv("louisville.csv")
louisville['Date'] = pd.to_datetime(louisville['DATE_OCCURED'])
louisville['Year'] = [a.year for a in louisville['Date']]
louisville['Week'] = louisville['Date'].dt.strftime('%U')


louisville = louisville[louisville.Year > 2017]
louisville = louisville.reset_index()

louisville['Offense_grp'] = ' '


# get offense and offense_detail for each row

for i in range(0,len(louisville)):
    
    code = louisville['NIBRS_CODE'][i]
    try:
        
        a = nibrs.at[code,'Offense_grp']

        
    except:
        a = ' '


    louisville['Offense_grp'][i] = a


# aggregation (grouping) change as needed

louisville_agg = louisville.groupby(['Year','Week','Offense_grp']).size().unstack().reset_index()


#writing aggregate and final df to excel
louisville_agg.to_excel('louisville_agg.xlsx')
#louisville.to_excel('louisville_df.xlsx')


