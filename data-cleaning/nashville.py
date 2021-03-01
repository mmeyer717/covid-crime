import pandas as pd

# importing list of codes and descriptions
nibrs = pd.read_excel('NIBRS.xlsx')
nibrs = nibrs.set_index('Code')
nibrs.index = nibrs.index.astype(str, copy = False)


# import city data and get year, week
nashville = pd.read_csv("Nashville.csv")
nashville['Date'] = pd.to_datetime(nashville['Incident Occurred'])
nashville['Year'] = [a.year for a in nashville['Date']]
nashville = nashville[nashville['Year'] > 2017]
nashville['Week'] = nashville['Date'].dt.strftime('%U')

#delete unfounded incidents
#nashville = nashville[~nashville["Incident Status Code"] == "O"]
nashville.drop(nashville.loc[nashville["Incident Status Code"]=="U"].index, inplace=True)

nashville = nashville.reset_index()


nashville = nashville.join(nibrs, on = 'Offense NIBRS')



# aggregation (grouping) change as needed

nashville = nashville.drop_duplicates(subset = ["Incident Number",'Offense_grp']) 
nashville_agg = nashville.groupby(['Year','Week','Offense_grp']).size().unstack().reset_index()


#writing aggregate and final df to excel
nashville_agg.to_excel('nashville_agg.xlsx')
nashville.to_excel('nashville_df.xlsx')


