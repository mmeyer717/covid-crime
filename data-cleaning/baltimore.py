import pandas as pd

# import city data and get year, week
baltimore = pd.read_csv("baltimore.csv")


#baltimore = pd.concat([file1,file2.rename(columns=str.lower)])


baltimore['Date'] = pd.to_datetime(pd.to_datetime(baltimore['CrimeDateTime']).dt.date)

baltimore['Year'] = [(a.year) for a in baltimore['Date']]
baltimore['Week'] = baltimore['Date'].dt.strftime('%U')


codes = pd.read_excel('baltimore_lookup.xlsx')
baltimore = baltimore.join(codes.set_index('Code'), on = "CrimeCode")

baltimore_agg = baltimore.groupby(['Year','Week','Offense_grp']).size().unstack().reset_index()


#writing aggregate and final df to excel
baltimore_agg.to_excel('baltimore_agg.xlsx')

baltimore.to_csv('baltimore_df.csv')

