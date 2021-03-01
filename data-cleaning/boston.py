import pandas as pd


# importing list of codes and descriptions
bos_codes = pd.read_excel('boston_lookup.xlsx')
#bos_codes = bos_codes.set_index('Code')
bos_codes.index = bos_codes.index.astype(str, copy = False)

# import city data and get year, week
file1 = pd.read_csv("boston2020.csv")
file2 = pd.read_csv("boston2019.csv")
file3 = pd.read_csv("boston2018.csv")


boston = pd.concat([file1,file2,file3])
boston['Date'] = pd.to_datetime(boston['OCCURRED_ON_DATE'])
boston['Year'] = boston['YEAR']

#Choose year

boston = boston[boston.YEAR > 2017]

#populate week

boston['Week'] = boston['Date'].dt.strftime('%U')


boston = boston.reset_index()

boston = boston.join(bos_codes.set_index('Code'), on = 'OFFENSE_CODE')

    
boston = boston.drop_duplicates(subset = ["INCIDENT_NUMBER",'Offense_grp'])
               

boston_agg = boston.groupby(['Year','Week','Offense_grp']).size().unstack().reset_index()
boston_agg.to_excel('boston_agg.xlsx')
boston.to_excel('boston_df.xlsx')


