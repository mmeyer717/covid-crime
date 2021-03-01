import pandas as pd

# import city data and get year, week
la = pd.read_csv("LA.csv")
la['Date'] = pd.to_datetime(la['DATE OCC'])
la['Year'] = [int(a.year) for a in la['Date']]
la['Week'] = la['Date'].dt.strftime('%U')


codes = pd.read_excel('la_lookup.xlsx')
la = la.join(codes.set_index('Code'), on = "Crm Cd Desc")


la_agg = la.groupby(['Year','Week','Offense_grp']).size().unstack().reset_index()


#writing aggregate and final df to excel
la_agg.to_excel('la_agg.xlsx')
#la.to_excel('la_df.xlsx')
