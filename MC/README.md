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

## Reconstruction of W and top
### transverse mass.ipynb

A jupyter notebook for reconstructing transverse masses of 2 tops and 2 W bosons. 

Results are:
wlv.png, wlvb.png, wqq.png and wqqb.png
