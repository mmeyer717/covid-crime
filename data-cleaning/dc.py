import pandas as pd

# import city data and get year, week
dc = pd.read_csv("DC.csv")
dc['Date'] = pd.to_datetime(dc['START_DATE'])

dc['Year'] = [int(a.year) for a in dc['Date']]
dc['Week'] = dc['Date'].dt.strftime('%U')

dc = dc[dc.Year > 2017]

codes = pd.read_excel('dc_lookup.xlsx')
dc = dc.join(codes.set_index('Code'), on = "OFFENSE")

dc_agg = dc.groupby(['Year','Week','Offense_grp']).size().unstack().reset_index()


#writing aggregate and final df to excel
dc_agg.to_excel('dc_agg.xlsx')
#dc.to_csv('dc_df.csv')
