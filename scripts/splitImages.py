# %% [markdown]
"""
# Splits images into sub-images
Hopefully this will help Mask-RCNN not get overwhelmed with a large image with too many marked objects
"""
# %%
import cv2
import skimage
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
# %% Test loading image
fname = '../data/AG2021/phaseContrast/phaseContrast_C5_1_2020y06m19d_03h33m.jpg'
im = cv2.imread(fname)
plt.imshow(im)
# %%
def imSplit(im, nIms=16):
    """
    Splits images into given number of tiles
    Inputs:
    im: Image to be split
    nIms: Number of images (must be a perfect square)
    """
    div = int(np.sqrt(nIms))

    nRow = im.shape[0]
    nCol = im.shape[1]

    M = nRow//div
    N = nCol//div
    tiles = []
    for y in range(0,im.shape[1],N): # Column
        for x in range(0,im.shape[0],M): # Row
            tiles.append(im[x:x+M,y:y+N])
    return tiles

tiles = imSplit(im, 16)
for tile in tiles:
    plt.figure()
    plt.imshow(tile)
# %% Split masks
# Access files in mask and phaseContrast directories, split them,
# then save to split directory
dataDir = '../data/AG2021'
splitDir = '../data/AG2021Split'
# Split up masks
maskNames = os.listdir(os.path.join(dataDir, 'mask'))

for maskName in maskNames:
    # Read and split mask
    mask = cv2.imread(os.path.join(dataDir, 'mask', maskName), cv2.IMREAD_UNCHANGED)
    maskSplit = imSplit(mask, 4)

    # For each mask append a number, then save it
    for num, mask in enumerate(maskSplit):
        newMaskName =  '.'.join([maskName.split('.')[0]+'_'+str(num+1), maskName.split('.')[1]])
        newMaskPath = os.path.join(splitDir, 'mask', newMaskName)
        cv2.imwrite(newMaskPath, mask)
# %%
dataDir = '../data/AG2021'
splitDir = '../data/AG2021Split'
# Split up masks
imNames = os.listdir(os.path.join(dataDir, 'phaseContrast'))

for imName in imNames:
    # Read and split mask
    im = cv2.imread(os.path.join(dataDir, 'phaseContrast', imName))
    tiles = imSplit(im, 4)

    # For each mask append a number, then save it
    for num, im in enumerate(tiles):
        newImName =  '.'.join([imName.split('.')[0]+'_'+str(num+1), imName.split('.')[1]])
        newImPath = os.path.join(splitDir, 'phaseContrast', newImName)
        # print(newImPath)
        cv2.imwrite(newImPath, im)
# %%