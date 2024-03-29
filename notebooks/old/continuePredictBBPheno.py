# %%
# %%
from src.models.trainBB import makeImageDatasets, train_model, getTFModel
from src.data.fileManagement import convertDate, getModelDetails
from src.models import modelTools
from pathlib import Path
import numpy as np
import time
import sys
import datetime

from torchvision import models
from torch.optim import lr_scheduler
import torch.nn as nn
import torch
import torch.optim as optim

# %%
homePath = Path('..')
oldModel = 'classifySingleCellCrop-721082'
oldModelPath = homePath / 'results' / 'classificationTraining' / f'{oldModel}.out'

modelID, idSource = modelTools.getModelID(sys.argv)
modelSaveName = homePath / 'models' / 'classification' / f'classifySingleCellCrop-{modelID}.pth'
modelInputs = getModelDetails(oldModelPath)

# Make relevant replacements - new model name, and list old models
if 'oldModels' not in modelInputs.keys():
    modelInputs['oldModels'] = modelInputs['modelName']
else:
    modelInputs['oldModels'] += f',{modelInputs["modelName"]}'
modelInputs['modelName'] = modelSaveName.parts[-1]
modelInputs['modelIDSource'] = idSource


modelTools.printModelVariables(modelInputs)
experiment = modelInputs['experiment']
# %%
dataPath = Path(f'../data/{experiment}/raw/phaseContrast')
datasetDictPath = Path(f'../data/{experiment}/split16/{experiment}DatasetDictNoBorder.npy')
datasetDicts = np.load(datasetDictPath, allow_pickle=True)
co = ['B7','B8','B9','B10','B11','C7','C8','C9','C10','C11','D7','D8','D9','D10','D11','E7','E8','E9','E10','E11']
datasetDicts = [seg for seg in datasetDicts if seg['file_name'].split('_')[1] in co]
# %%
dataloaders, dataset_sizes = makeImageDatasets(datasetDicts, 
                                               dataPath,
                                               modelInputs
                                            )
# %%
inputs, classes = next(iter(dataloaders['train']))
# %%
# plt.imshow(inputs[16].numpy().transpose((1,2,0)))
# %%
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

if not modelSaveName.parent.exists():
    raise NotADirectoryError('Model directory not found')

model = getTFModel(modelInputs['modelType'])
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.001)

# %%
# Scheduler to update lr
# Every 7 epochs the learning rate is multiplied by gamma
setp_lr_scheduler = lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

model = train_model(model, 
                    criterion, 
                    optimizer, 
                    setp_lr_scheduler, 
                    dataloaders, 
                    dataset_sizes, 
                    modelSaveName, 
                    num_epochs=modelInputs['num_epochs']
                    )