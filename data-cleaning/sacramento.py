import pandas as pd

# importing list of codes and descriptions
codes = pd.read_excel('sacramento_lookup.xlsx')
codes = codes.set_index('Code')
codes.index = codes.index.astype(str, copy = False)


# import city data and get year, week
sacramento = pd.read_csv("sacramento.csv")
sacramento['Date'] = pd.to_datetime(sacramento['Occurence_Date'])
sacramento['Year'] = [int(a.year) for a in sacramento['Date']]

#delete incidents before 2019
sacramento = sacramento[sacramento.Year > 2017]
sacramento = sacramento.reset_index()

sacramento['Week'] = sacramento['Date'].dt.strftime('%U')




sacramento['Offense_grp'] = ' '


# get offense and offense_detail for each row

for i in range(0,len(sacramento)):
    
    
    try:
        code = str(int(sacramento['Offense_Code'][i]))

        if code == '999':
            code = str(sacramento['Description'][i])

        elif code == '2404':
            code = str(sacramento['Offense_Category'][i])
        
        a = codes.at[code,'Offense_grp']
 
        
    except:
        a = ' '


    sacramento['Offense_grp'][i] = a


# aggregation (grouping) change as needed

sacramento_agg = sacramento.groupby(['Year','Week','Offense_grp']).size().unstack().reset_index()



#writing aggregate and final df to excel
sacramento_agg.to_excel('sacramento_agg.xlsx')
sacramento.to_csv('sacramento_df.csv')


