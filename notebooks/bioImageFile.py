# %%
import os
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import datetime
from src.data import fileManagement
# %%
dataDir = '../data/upload'
filePaths = []
annotations = []
annotationDict = {'TJ2201':         '231Subpop1 and 231Subpop2 coculture',
                  'TJ2454-2311kb32':'MDA-MB-231 untreated population',
                  'TJ2301-231C2':   'MDA-MB-231 treated population',
                  'TJ2453-436Co':   '436Subpop1 and 436Subpop2 coculture'}
i = 0
TJ2201Keep = pd.read_csv('../data/TJ2201Keep.csv')['0'].tolist()

co = ['B7','B8','B9','B10','B11','C7','C8','C9','C10','C11','D7','D8','D9','D10','D11','E7','E8','E9','E10','E11']

# %%
def checkTJ2201(fileName, co = co):
    
    well = fileName.split('_')[1]
    if well not in co:
        return True
    strDate = '_'.join(fileName.split('_')[3:5])
    date = fileManagement.convertDate(strDate)
    if date > datetime.datetime(2022, 4, 8, 12, 0):
        return True
    else:
        return False
# %%
filePathsDel = []
TJ2201Remove = []
TJ2201Keep2 = []
for root, dirs, files in tqdm(os.walk(dataDir)):

    if len(files)>0 and files[0] == 'fileList.tsv':
        continue
    if len(files) < 1:
        continue
    
    for file in files:
        filePath = os.path.join(root, file)

        if not file.endswith('.png'):
            # filePathsDel.append(filePath)
            continue

        experiment = root.split('/')[3]
        if experiment == 'TJ2201':
            denied = checkTJ2201(file)
            if denied:
                TJ2201Remove.append(filePath)
                continue
            else:
                TJ2201Keep2.append(filePath)
        # print(file)


        if 'composite' in filePath:
            filePath2 = filePath.replace('composite', 'phaseContrast')
            if not Path(filePath2).exists():
                filePathsDel.append(filePath)
            
        annotations.append(annotationDict[experiment])
        filePaths.append(filePath)

# %%

assert len(filePathsDel) < 10
for filePath in filePathsDel:
    os.remove(filePath)
    
for filePath in TJ2201Remove:
    os.remove(filePath)
# %%
filePaths = [filePath.replace('../data/upload/', 'upload/') if filePath.startswith('..') else filePath for filePath in filePaths]
bioImage = pd.DataFrame({'Files': filePaths, 'Description': annotations})

bioImage.to_csv('../data/upload/fileList.tsv', sep = '\t', index=False)
# %%