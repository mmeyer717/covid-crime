import pandas as pd

mil = pd.read_csv("milwaukee.csv")

mil["Year"] = mil["ReportedYear"]
mil['Date'] = pd.to_datetime(mil['ReportedDateTime'])
mil['Week'] = mil['Date'].dt.strftime('%U')
		
mil = mil[mil.Year > 2017]
mil["Aggravated Assault"] = mil["AssaultOffense"]
mil["Rape"] = mil["SexOffense"]
mil["Larceny"] = mil["Theft"] +mil["LockedVehicle"]
mil["Auto-Theft"] = mil["VehicleTheft"]
mil = mil[["Year","Week","Aggravated Assault","Burglary","Homicide","Robbery","Rape",
           "Larceny","Auto-Theft"]]

mil_agg = mil.groupby(['Year','Week']).sum().reset_index()
mil_agg.to_excel("milwaukee_agg.xlsx")
                
