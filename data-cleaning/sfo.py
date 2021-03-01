import pandas as pd




# import city data and get year, week
sfo = pd.read_csv("sfo.csv")
sfo['Date'] = pd.to_datetime(sfo['Incident Date'])
sfo['Year'] = [a.year for a in sfo['Date']]

sfo = sfo[sfo.Year > 2017]


sfo['Week'] = sfo['Date'].dt.strftime('%U')

# keep only initial report incidents to avoid duplication
initial_ls = [ 'Initial' , 'Coplogic Initial' , 'Vehicle Initial']

sfo = sfo[sfo['Report Type Description'].isin(initial_ls)]
    

sfo = sfo.reset_index()

#crete lists for incident categories and subcategories of interest
inc_cat_ls = ['Larceny Theft','Motor Vehicle Theft','Robbery','Rape','Homicide',"Burglary"]
inc_subcat_ls = ['Aggravated Assault']


sfo["offense_grp"] = ""



for i in range(0, len(sfo)):

    

    if (sfo['Incident Category'][i] in inc_cat_ls ):
        sfo['offense_grp'][i] = sfo['Incident Category'][i]

    elif (sfo['Incident Subcategory'][i] in inc_subcat_ls ):
        sfo['offense_grp'][i] = sfo['Incident Subcategory'][i]



sfo = sfo.drop_duplicates(subset = ["Incident ID" , "offense_grp"])       

               




sfo_agg = sfo.groupby(['Year','Week','offense_grp']).size().unstack().reset_index()
sfo_agg.to_excel('sfo_agg.xlsx')
#sfo.to_excel('sfo_df.xlsx')
