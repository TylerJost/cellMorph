# Transcriptomic Subpopulation Prediction
## Please note that this repository is meant to archive code, not provide a novel model archicture or data loading structure
This is a repository to archive code to classify cells using their morphology. This respository can be used as a source to:

1. Train an instance segmentation algorithm using small numbers of masks. 
2. Predict cell identity (transcriptomic state, lineage, etc.) from information. 

This is meant to be a comprehensive set of scripts and functions which can train on an increasing complexity of features:
- [x] Morphology
- [x] Textural Information
- [x] Perimeter shapes
- [x] Convolutional Neural Networks

Instance segmentation is built on [detectron2](https://github.com/facebookresearch/detectron2). Only code is included, no data or trained model outputs. 

If you want to run any of the analysis, you must build `detectron2` from source using the resources above. You will also need pytorch, 

Currently, the project is structured like so:

```
├── computerVisionMinimal.yml
├── data
├── explore
├── output
├── README.md
├── results
└── scripts
```
Where:
* `data` is the image data for each experiment
* `output` is the model output from the segmentation model
* `results` are downstream analysis results
* `scripts` are the finalized tools and classes
* `explore` are the analysis scripts

Files in the `data` folder are organized like so:

```
├── data
│   ├── experiment
│   │   ├── composite
│   │   └── phaseContrast
```

Where:
* `composite` is the superimposed fluroescent and phase-contrast image
* `phaseContrast` is the full sized "HD" phase contrast image

Experiments 
Files within experiment directories are named like so:

`Directory_Base Information`

Where `Directory` is the immediate directory, and `Base Information` is the output from the Incucyte (`Well_Im#_Date`). 
