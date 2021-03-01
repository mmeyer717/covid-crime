import pandas as pd

stpaul = pd.read_csv("stpaul.csv")
stpaul['Date'] = pd.to_datetime(stpaul['DATE'])
stpaul['Year'] = [a.year for a in stpaul['Date']]



stpaul = stpaul[stpaul["Year"] > 2017]
stpaul['Week'] = stpaul['Date'].dt.strftime('%U')

stpaul = stpaul.reset_index()

codes = pd.read_excel('stpaul_lookup.xlsx')


stpaul = stpaul.join(codes.set_index('Code'), on = "CODE")

stpaul = stpaul.drop_duplicates(subset = ["CASE NUMBER" , "Offense_grp"])


stpaul_agg = stpaul.groupby(["Year","Week","Offense_grp"]).size().unstack().reset_index()
stpaul_agg.to_excel("stpaul_agg.xlsx")

