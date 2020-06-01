# Dissertation
ttH production

This repository contains python scripts for data analysis during the dissertation project.

# 1. MC data
ttH.root

## Reconstruction of Higgs mass
ttH.py
  python2 ttH.py ttH.root h.root
This will creat a h.root file containing the reconstructed Higgs mass.

fit.py
  python2 fit.py h.root plots.pdf
This will fit the previous result with a Gaussian function.

## Reconstruction of ttpair mass
tt.py
  python2 tt.py ttH.root tt.root
This will creat a tt.root file containing the reconstructed tt pair mass.
