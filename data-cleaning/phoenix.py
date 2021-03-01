import pandas as pd




# import city data and get year, week
phoenix = pd.read_csv("phoenix.csv")
phoenix['Date'] = pd.to_datetime(phoenix['OCCURRED ON'])
phoenix['Year'] = [a.year for a in phoenix['Date']]

phoenix = phoenix[phoenix.Year > 2017]

phoenix['Week'] = phoenix['Date'].dt.strftime('%U')

phoenix = phoenix.reset_index()

phoenix["offense_grp"] = phoenix["UCR CRIME CATEGORY"]

        

phoenix_agg = phoenix.groupby(['Year','Week','offense_grp']).size().unstack().reset_index()
phoenix_agg.to_excel('phoenix_agg.xlsx')
phoenix.to_excel('phoenix_df.xlsx')
