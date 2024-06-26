# %%
import os
from pathlib import Path
from skimage.io import imread, imsave
import matplotlib.pyplot as plt
from skimage import exposure
# %%
# Division amount
amt = 3

subPopPath = Path('../../data/TJ2201/raw/')
subPopFile = '_B7_5_2022y04m10d_12h00m.png'

subPopPhase = imread(subPopPath / 'phaseContrast' / Path('phaseContrast' + subPopFile))
subPopComposite = imread(subPopPath / 'composite' / Path('composite' + subPopFile))
subPopHighContrast = exposure.equalize_adapthist(subPopPhase)

axis1, axis2 = subPopHighContrast.shape


subPopComposite = subPopComposite[0:int(axis1/amt), 0:int(axis2/amt)]

plt.subplot(121)
plt.imshow(subPopHighContrast, cmap = 'gray')
plt.subplot(122)
plt.imshow(subPopComposite)

imsave('../../figures/publication/exemplar/esamCoPhase.png', subPopHighContrast)
imsave('../../figures/publication/exemplar/esamCoComposite.png', subPopComposite)

# %%
lineagePath = Path('../../data/TJ2302/raw/')
lineageFile = '_E7_1_2023y03m02d_23h47m.png'

lineagePhase = imread(lineagePath / 'phaseContrast' / Path('phaseContrast' + lineageFile))
lineageComposite = imread(lineagePath / 'composite' / Path('composite' + lineageFile))
lineageHighContrast = exposure.equalize_adapthist(lineagePhase)

axis1, axis2 = lineageHighContrast.shape

lineageHighContrast = lineageHighContrast[0:int(axis1/amt), 0:int(axis2/amt)]
lineageComposite = lineageComposite[0:int(axis1/amt), 0:int(axis2/amt)]

plt.subplot(121)
plt.imshow(lineageHighContrast, cmap = 'gray')
plt.subplot(122)
plt.imshow(lineageComposite)

imsave('../../figures/publication/exemplar/lineagePhase.png', lineageHighContrast)
imsave('../../figures/publication/exemplar/lineageComposite.png', lineageComposite)

# %%
untreatedPath = Path('../../data/TJ2201/raw/')
untreatedFile = '_B2_6_2022y04m09d_16h00m.png'

untreatedPhase = imread(untreatedPath / 'phaseContrast' / Path('phaseContrast' + untreatedFile))
untreatedHighContrast = exposure.equalize_adapthist(untreatedPhase)

treatedPath = Path('../../data/TJ2301-231C2/raw/')
treatedFile = '_B2_9_2023y08m14d_11h00m.png'

treatedPhase = imread(treatedPath / 'phaseContrast' / Path('phaseContrast' + treatedFile))
treatedHighContrast = exposure.equalize_adapthist(treatedPhase)

axis1, axis2 = treatedHighContrast.shape

untreatedHighContrast = untreatedHighContrast[0:int(axis1/amt), 0:int(axis2/amt)]
treatedHighContrast = treatedHighContrast[0:int(axis1/amt), 0:int(axis2/amt)]


factor = 200/322 #200 um/ 322 px
pxIncrease = int(100/factor)
# pxAmt = 2
initStart = 300
initEnd = int(initStart+pxIncrease)
untreatedHighContrast = untreatedHighContrast[0:int(axis1/amt), 0:int(axis2/amt)]
untreatedHighContrast[310:315, initStart:initEnd] = 0
# Make line for scale bar
plt.imshow(untreatedHighContrast, cmap = 'gray')
plt.axis('off')
print(f'Pixel bar is {30} um')


plt.subplot(121)
plt.imshow(untreatedHighContrast, cmap = 'gray')
plt.subplot(122)
plt.imshow(treatedHighContrast, cmap = 'gray')

imsave('../../figures/publication/exemplar/untreated.png', untreatedHighContrast)
imsave('../../figures/publication/exemplar/treated.png', treatedHighContrast)

# %%
amt = 3

path436 = Path('../../data/TJ2453-436Co/raw/')
file436 = '_E9_3_2024y04m09d_08h02m.png'
subPopPhase = imread(path436 / 'phaseContrast' / Path('phaseContrast' + file436))
subPopComposite = imread(path436 / 'composite' / Path('composite' + file436))
subPopHighContrast = exposure.equalize_adapthist(subPopPhase)

axis1, axis2 = subPopHighContrast.shape


subPopHighContrast = subPopHighContrast[0:int(axis1/amt), 0:int(axis2/amt)]
subPopComposite = subPopComposite[0:int(axis1/amt), 0:int(axis2/amt)]

plt.subplot(121)
plt.imshow(subPopHighContrast, cmap = 'gray')
plt.subplot(122)
plt.imshow(subPopComposite)

imsave('../../figures/publication/exemplar/436CoPhase.png', subPopHighContrast)
imsave('../../figures/publication/exemplar/436CoComposite.png', subPopComposite)
# %%