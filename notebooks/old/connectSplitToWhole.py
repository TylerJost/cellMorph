# %% [markdown]
"""
Connects split image coordinates to whole image coordinates
"""
# %%
import numpy as np
import os 
import matplotlib.pyplot as plt

from skimage.io import imread
# %%
def splitName2Whole(imgName: str):
    """
    Strips split number from image name

    Inputs:
        - imgName: Name of image in format:
            imagingType_Well_IncucyteNum_Date_Time_ImgNum.extension
    Outputs:
        - imgNameWhole: Name of image in format:
            imagingType_Well_IncucyteNum_Date_Timeß.extension

    """
    extSplit = imgName.split('.')
    ext = extSplit[-1]
    imgName = extSplit[0]

    imgNameWhole = '_'.join(imgName.split('_')[0:-1])+'.'+ext
    return imgNameWhole

def split2WholeCoords(nIms, wholeImgSize):
    """
    Returns coordinates to connect split images to whole images

    Inputs:
        - nIms: This is the number of images an original image was split into
        - wholeImgSize: 1x2 list of type [nRows, nCols]

    Outputs:
        - coordinates: A dictionary where keys are the split number and 

    Example:
    coordinates = split2WholeCoords(nIms=16, wholeImg=img)
    # polyx and polyy are the initial segmentation coordinates
    polyxWhole = polyx + coordinates[int(splitNum)][0]
    polyyWhole = polyy + coordinates[int(splitNum)][1]
    """ 

    div = int(np.sqrt(nIms))
    nRow = wholeImgSize[0]
    nCol = wholeImgSize[1]

    M = nRow//div
    N = nCol//div
    tiles = []
    imNum = 1
    coordinates = {}
    for x in range(0,wholeImgSize[1],N): # Column
        for y in range(0,wholeImgSize[0],M): # Row
            coordinates[imNum] = [x, y]
            imNum += 1

    return coordinates

def expandImageSegmentation(poly, bb, splitNum, coords, padNum=200):
    """
    Takes segmentation information from split image and outputs it for a whole (non-split) image
    
    Inputs:
    - poly: Polygn of segmentation from datasetDict
    - bb: Bounding box of segmentation from datasetDict
    - padNum: Amount of padding around image
    - coords: Coordinates to relate split image to whole image

    Outputs:
    - polyxWhole, polyyWhole: polygon coordinates for whole image
    - bbWhole: bounding box for whole image
    """
    poly = np.array(poly)
    polyx = poly[::2]
    polyy = poly[1::2]

    cIncrease = coords[int(splitNum)]
    bbWhole = bb.copy()
    bbWhole[1] += cIncrease[1] + padNum
    bbWhole[3] += cIncrease[1] + padNum
    bbWhole[0] += cIncrease[0] + padNum
    bbWhole[2] += cIncrease[0] + padNum

    polyxWhole = polyx + cIncrease[0] + padNum
    polyyWhole = polyy + cIncrease[1] + padNum
    
    return [polyxWhole, polyyWhole, bbWhole]

def bbIncrease(poly, bb, imgName, imgWhole, nIncrease=50, padNum=200):
    """
    Takes in a segmentation from a split image and outputs the segmentation from the whole image. 
    Inputs: 
    - poly: Polygon in datasetDict format
    - bb: Bounding box in datasetDict format
    - imageName: Name of the image where the segmentation was found
    - imgWhole: The whole image from which the final crop will come from
    - nIncrease: The amount to increase the bounding box
    - padNum: The padding on the whole image, necessary to segment properly

    Outputs:
    - imgBBWholeExpand: The image cropped from the whole image increased by nIncrease
    """
    splitNum = int(imgName.split('_')[-1].split('.')[0])
    coords = split2WholeCoords(nIms = 16, wholeImgSize = imgWhole.shape)
    imgWhole = np.pad(imgWhole, (padNum,padNum))
    polyxWhole, polyyWhole, bbWhole = expandImageSegmentation(poly, bb, splitNum, coords, padNum)
    bbWhole = [int(corner) for corner in bbWhole]
    colMin, rowMin, colMax, rowMax = bbWhole
    rowMin -= nIncrease
    rowMax += nIncrease
    colMin -= nIncrease
    colMax += nIncrease

    bbIncrease = [colMin, rowMin, colMax, rowMax]
    imgBBWholeExpand = imgWhole[bbIncrease[1]:bbIncrease[3], bbIncrease[0]:bbIncrease[2]]

    return imgBBWholeExpand, [polyxWhole, polyyWhole]

def getImgPath(datasetDicts, imgNum = -1):
    if imgNum < 0:
        imgNum = np.random.randint(len(datasetDicts))
    while True:
        # imgNum = 211
        # imgNum = 31
        imgSeg = datasetDicts[imgNum]
        splitNum = int(imgSeg['file_name'].split('_')[-1].split('.')[0])
        fileNameSplit = imgSeg['file_name'].split('/')[-1]
        fileNameWhole = splitName2Whole(fileNameSplit)
        if len(imgSeg['annotations']) == 0:
            imgNum += 1
        else:
            break

    return imgSeg, fileNameSplit

def getPolygonCentroid(polyx, polyy):
    polyx = polyFinal[0]
    polyy = polyFinal[1]
    A = .5*np.sum([polyx[i]*polyy[i+1] - polyx[i+1]*polyy[i] for i in range(0, len(polyx)-1)])
    Cx = 1/(6*A)*np.sum([(polyx[i]+polyx[i+1])*(polyx[i]*polyy[i+1]-polyx[i+1]*polyy[i]) for i in range(0, len(polyx)-1)])
    Cy = 1/(6*A)*np.sum([(polyy[i]+polyy[i+1])*(polyx[i]*polyy[i+1]-polyx[i+1]*polyy[i]) for i in range(0, len(polyx)-1)])
    return Cx, Cy
# %%
datasetDicts = np.load('../data/TJ2201/split16/TJ2201DatasetDict.npy', allow_pickle=True)
# %%
splitDir = '../data/TJ2201/split16/phaseContrast'
wholeDir = '../data/TJ2201/raw/phaseContrast'

# Find an image with segmentations
# np.random.seed(1234)
# imgNum = np.random.randint(len(datasetDicts))
# while True:
#     # imgNum = 211
#     # imgNum = 31
#     imgSeg = datasetDicts[imgNum]
#     splitNum = int(imgSeg['file_name'].split('_')[-1].split('.')[0])
#     fileNameSplit = imgSeg['file_name'].split('/')[-1]
#     fileNameWhole = splitName2Whole(fileNameSplit)
#     if len(imgSeg['annotations']) == 0:
#         imgNum += 1
#     else:
#         break

# %%
# imgSplit = imread(os.path.join(splitDir, fileNameSplit))
# imgWhole = imread(os.path.join(wholeDir, fileNameWhole))

# coords = split2WholeCoords(nIms = 16, wholeImgSize = imgWhole.shape)
# poly = np.array(imgSeg['annotations'][0]['segmentation'][0])
# bb = imgSeg['annotations'][0]['bbox']
# bb = np.array([int(corner) for corner in bb])
# polyx = poly[::2]
# polyy = poly[1::2]

# padNum = 200
# imgWhole = np.pad(imgWhole, (padNum,padNum))
# polyxWhole, polyyWhole, bbWhole = expandImageSegmentation(poly, bb, splitNum, coords, padNum=200)

# imgBB = imgSplit[bb[1]:bb[3], bb[0]:bb[2]]
# imgBBWhole = imgWhole[bbWhole[1]:bbWhole[3], bbWhole[0]:bbWhole[2]]

# nIncrease = 50
# colMin, rowMin, colMax, rowMax = bbWhole
# rowMin -= nIncrease
# rowMax += nIncrease
# colMin -= nIncrease
# colMax += nIncrease

# bbIncrease = [colMin, rowMin, colMax, rowMax]
# imgBBWholeExpand = imgWhole[bbIncrease[1]:bbIncrease[3], bbIncrease[0]:bbIncrease[2]]
# plt.figure(figsize=(75,50))
# plt.subplot(241)
# plt.imshow(imgSplit)
# plt.plot(polyx, polyy, c='red')
# plt.subplot(242)
# plt.imshow(imgBB)
# plt.subplot(243)
# plt.imshow(imgBBWhole, cmap='gray')
# plt.subplot(244)
# plt.imshow(imgWhole, cmap='gray')
# plt.plot(polyxWhole, polyyWhole, c='red', linewidth=1)
# plt.subplot(245)
# plt.imshow(imgBBWholeExpand, cmap='gray')
# print(imgNum)
# %%
# 46860
imgSeg, fileNameSplit = getImgPath(datasetDicts, imgNum = -1)
# %%
fileNameWhole = splitName2Whole(fileNameSplit)
imgSplit = imread(os.path.join(splitDir, fileNameSplit))
imgWhole = imread(os.path.join(wholeDir, fileNameWhole))
poly = np.array(imgSeg['annotations'][0]['segmentation'][0])
bb = imgSeg['annotations'][0]['bbox']
imgName = fileNameSplit
nIncrease = 50

finalCrop, polyFinal = bbIncrease(poly, bb, imgName, imgWhole, nIncrease=50)
plt.imshow(finalCrop, cmap='gray')
plt.scatter(finalCrop.shape[1]/2,finalCrop.shape[0]/2)
# plt.plot(polyFinal[0], polyFinal[1], c = 'red')
Cx, Cy = getPolygonCentroid(polyFinal[0], polyFinal[1])
diffx = Cx-finalCrop.shape[1]/2
diffy = Cy-finalCrop.shape[0]/2
plt.plot(polyFinal[0]-diffx, polyFinal[1]-diffy, c = 'red')

# plt.scatter(Cx, Cy)
# %%
plt.imshow(imgSplit)
plt.plot(poly[::2], poly[1::2])

