# MC data
ttH.root

# Scripts

## Reconstruction of Higgs mass
### ttH.py

  python2 ttH.py ttH.root h.root
  
This will creat a h.root file containing the reconstructed Higgs mass.

### fit.py

  python2 fit.py h.root plots.pdf
  
This will fit the previous result with a Gaussian function.

### plot_H.pdf

The fitting result.

## Reconstruction of mass and angle variables
### transverse mass.ipynb

A jupyter notebook for reconstructing transverse masses of 2 tops and 2 W bosons. 

Results are:
wlv.png, wlvb.png, wqq.png and tqqb.png

### 12 variables.ipynb

A jupyter notebook for reconstructing variables from the paper.

### 12 variables (no boost).ipynb

No frame of reference changing is applied in this notebook. The result seems to be more symmetric and close to the paper.

### 12 variables (big).ipynb

Same reconstruction code applying on bigger MC data. 

### 12 variables (combine).ipynb

Combined result for the reconstruction of 12 variables from signal and background MC data. The background data is further divided into sidebands and near signal region. The result can be seen from 'combine.pdf'. 

### alpha.ipynb

Combined result for the reconstruction of 12 variables from MC data with CP mixing angles equal to 0, 30 and 60. The result can be seen from 'alpha.pdf'. 
