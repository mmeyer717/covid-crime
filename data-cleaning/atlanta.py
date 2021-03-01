import pandas as pd


# importing list of codes and descriptions
codes = pd.read_excel('atlanta_lookup.xlsx')
codes.index = codes.index.astype(str, copy = False)

# import city data and get year, week
atlanta = pd.read_csv("atlanta.csv")
atlanta['Date'] = pd.to_datetime(atlanta['Occur Date'], errors = "coerce")
atlanta['Year'] = [a.year for a in atlanta['Date']]

#Choose year

atlanta = atlanta[atlanta.Year > 2017]

#populate week

atlanta['Week'] = atlanta['Date'].dt.strftime('%U')




atlanta = atlanta.reset_index()


atlanta = atlanta.join(codes.set_index('Code'), on = "UCR Literal")


atlanta = atlanta.drop_duplicates(subset = ["Report Number",'Offense_grp'])

               
atlanta_agg = atlanta.groupby(['Year','Week','Offense_grp']).size().unstack().reset_index()
atlanta_agg.to_excel('atlanta_agg.xlsx')
atlanta.to_excel('atlanta_df.xlsx')


