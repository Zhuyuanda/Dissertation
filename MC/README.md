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
