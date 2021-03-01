import pandas as pd


ny = pd.read_csv("ny.csv")


ny = ny[ny["CRM_ATPT_CPTD_CD"] =="COMPLETED"]
# importing list of codes and descriptions
codes = pd.read_excel('NY_lookup.xlsx')
codes = codes.set_index('Code')
codes.index = codes.index.astype(str, copy = False)


# import city data and get year, week
ny['Date'] = pd.to_datetime(ny['CMPLNT_FR_DT'],errors='coerce')
ny = ny.dropna(subset= ['Date'])
ny['Year'] = [int(a.year) for a in ny['Date']]

#delete incidents before 2018
ny = ny[ny.Year > 2017]
ny = ny.reset_index()

ny['Week'] = ny['Date'].dt.strftime('%U')




ny['Offense_grp'] = ''

detail_off_ls = ['BURGLARY','FELONY ASSAULT', 'RAPE','SEX CRIMES']
# get offense and offense_detail for each row

for i in range(0,len(ny)):
    
    
    try:
        code = str(ny['OFNS_DESC'][i])

        if code in  detail_off_ls:
            code = str(ny['PD_DESC'][i])
            
        
        a = codes.at[code,'Offense_grp']
 
        
    except:
        a = ' '


    ny['Offense_grp'][i] = a


# aggregation (grouping) change as needed

ny_agg = ny.groupby(['Year','Week','Offense_grp']).size().unstack().reset_index()



#writing aggregate and final df to excel
#ny_agg.to_excel('ny_agg_1918.xlsx')
#ny.to_excel('ny_df_1918.xlsx')

ny_agg.to_excel('ny_agg_2020.xlsx')
ny.to_excel('ny_df_2020.xlsx')


