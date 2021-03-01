import pandas as pd

tulsa = pd.read_csv("tulsa.csv")

tulsa["Date"] = pd.to_datetime((pd.to_datetime(tulsa["incident_date"])).dt.date)
tulsa["Year"] = pd.DatetimeIndex(tulsa["incident_date"]).year
tulsa["Week"] = tulsa["Date"].dt.strftime('%U')

#tulsa = tulsa[tulsa["UCC_PART"] ==1]

tulsa_agg = tulsa.groupby(["Year","Week","ucc_crime_class_description"]).size().unstack().reset_index()

tulsa.to_excel("tulsa_df.xlsx")

tulsa_agg.to_excel("tulsa_agg.xlsx")

