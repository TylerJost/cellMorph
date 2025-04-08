# %%
import os
from pathlib import Path
import datetime

import matplotlib.pyplot as plt
import numpy as np

from src.visualization.trainTestRes import plotTrainingRes
from src.data.fileManagement import getModelDetails
# %%
resPath = '../results/classificationTraining'
maxTestAccs = {}
for trainingFile in Path(resPath).iterdir():
    trainingName = trainingFile.name
    if not trainingName.endswith('.txt'):
        continue
    if not trainingName.startswith('classifySingleCellCrop'):
        continue
    timeStamp = trainingFile.stem.split('-')[1]
    timeStamp = datetime.datetime.fromtimestamp(int(timeStamp))
    if not (timeStamp.year == 2025 and timeStamp.month == 4):
        continue
    trainLoss, trainAcc, testLoss, testAcc = plotTrainingRes(trainingFile, plot=False)
    modelDetails = getModelDetails(trainingFile)
    testWell = modelDetails['testWell']
    if len(testAcc) <= 4:
        continue
    if testWell in maxTestAccs.keys():
        print(f'{testWell} seen more than once')
    maxTestAccs[testWell] = np.max(testAcc)
# %%
plt.boxplot(maxTestAccs.values())