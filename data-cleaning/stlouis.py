import pandas as pd

stlouis = pd.read_csv("stlouis.csv", encoding='latin-1')
codes = pd.read_excel('stlouis_lookup.xlsx')
stlouis['Date'] = pd.to_datetime(stlouis['DateOccur'])
stlouis['Year'] = [a.year for a in stlouis['Date']]

#Choose year

stlouis = stlouis[stlouis.Year > 2017]

#populate week

stlouis['Week'] = stlouis['Date'].dt.strftime('%U')

stlouis['Code']= stlouis['Crime'].floordiv(10000)

stlouis = stlouis.join(codes.set_index('Code'), on = "Code")


stlouis_agg = stlouis.groupby(['Year','Week','Offense_grp'])['Count'].sum().unstack().reset_index()
stlouis_agg.to_excel('stlouis_agg.xlsx')
#stlouis.to_excel('stlouis_df.xlsx')
