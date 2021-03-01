import pandas as pd

mesa = pd.read_csv("mesa.csv")

mesa = mesa[~mesa["Occurred Date"].isna()]
mesa["Date"] = pd.to_datetime(mesa["Occurred Date"],errors='coerce')
mesa['Year'] = [int(a.year) for a in mesa['Date']]
mesa["Week"] = mesa["Date"].dt.strftime('%U')

mesa = mesa[mesa["City"] == "MESA"]
mesa = mesa[mesa["Year"] > 2017]

mesa_agg = mesa.groupby(["Year","Week","Crime Type"]).size().unstack().reset_index()

mesa.to_excel("mesa_df.xlsx")

mesa_agg.to_excel("mesa_agg.xlsx")

