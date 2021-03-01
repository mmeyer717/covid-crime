import pandas as pd




# import city data and get year, week
austin = pd.read_csv("austin.csv")

austin['Date'] = pd.to_datetime(austin['Occurred Date'])
austin['Year'] = [a.year for a in austin['Date']]

austin = austin[austin.Year > 2017]

austin['Week'] = austin['Date'].dt.strftime('%U')

austin = austin.reset_index()


austin_agg = austin.groupby(['Year','Week','Category Description']).size().unstack().reset_index()
austin_agg.to_excel('austin_agg.xlsx')


