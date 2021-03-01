import pandas as pd

denver = pd.read_csv("denver.csv")
denver['Date'] = pd.to_datetime(denver['FIRST_OCCURRENCE_DATE'])
denver['Year'] = [a.year for a in denver['Date']]




#Choose year

#denver = denver[denver.Year > 2017]

#populate week

denver['Week'] = denver['Date'].dt.strftime('%U')

denver = denver.reset_index()

codes = pd.read_excel('denver_lookup.xlsx')
denver["temp"] = ""
unq_offense_ls = ["burglary","sexual-assault"]
for i in range(0, len(denver)):

    a = denver["OFFENSE_CATEGORY_ID"][i]
    if a in unq_offense_ls:
                  a = denver["OFFENSE_TYPE_ID"][i]

    
    denver["temp"][i] = a
denver = denver.join(codes.set_index('Code'), on = "temp")


denver_agg = denver.groupby(['Year','Week','Offense_grp']).size().unstack().reset_index()
denver_agg.to_excel('denver_agg.xlsx')
denver.to_excel('denver_df.xlsx')
