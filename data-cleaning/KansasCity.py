import pandas as pd

# importing list of codes and descriptions
nibrs = pd.read_excel('NIBRS.xlsx')
nibrs = nibrs.set_index('Code')
nibrs.index = nibrs.index.astype(str, copy = False)


# import city data and get year, week
kansas_city = pd.read_csv("KansasCity.csv")
kansas_city['Date'] = pd.to_datetime(kansas_city['From_Date'])
kansas_city.dropna(subset=['Date'], inplace=True)


kansas_city['Year'] = [a.year for a in kansas_city['Date']]
kansas_city['Week'] = kansas_city['Date'].dt.strftime('%U')

kansas_city = kansas_city[kansas_city.Year > 2017]
kansas_city['Offense_grp'] = ' '
kansas_city = kansas_city.reset_index()


# get offense and offense_detail for each row

for i in range(0,len(kansas_city)):
    
    code = kansas_city['IBRS'][i]
        
    try:
        
        a = nibrs.at[code,'Offense_grp']

        
    except:
        a = ' '


    kansas_city['Offense_grp'][i] = a


# aggregation (grouping) change as needed

kansas_city_agg = kansas_city.groupby(['Year','Week','Offense_grp']).size().unstack().reset_index()


#writing aggregate and final df to excel
kansas_city_agg.to_excel('kansas_city_agg.xlsx')
#kansas_city.to_excel('kansas_city_df.xlsx')


