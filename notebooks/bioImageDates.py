# %%
import pandas as pd
from src.data import fileManagement

# %%
TJ2201Keep = pd.read_csv('../data/TJ2201Keep.csv')['0'].tolist()
# %%
dates = []
co = ['B7','B8','B9','B10','B11','C7','C8','C9','C10','C11','D7','D8','D9','D10','D11','E7','E8','E9','E10','E11']
for fileName in TJ2201Keep:
    well = fileName.split('_')[1]
    if well not in co:
        continue
    strDate = '_'.join(fileName.split('_')[3:5])
    date = fileManagement.convertDate(strDate)
    dates.append(date)