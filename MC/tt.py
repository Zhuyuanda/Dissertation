import ROOT
import sys
import numpy as np

if len ( sys . argv ) != 3:
  print " USAGE : % s < input file > < output file > " %( sys . argv [0])
  sys . exit (1)
inFileName = sys . argv [1]
outFileName = sys . argv [2]
print " Reading from " , inFileName , " and writing to " , outFileName

# read in data
inFile = ROOT . TFile . Open ( inFileName , " READ " )
tree = inFile . Get ( "ttHyyTree" )

# creat an empty hist
tt = ROOT . TH1D ( "data" ," m_{tt} , data " ,150 ,0 ,1500 )
tt . Sumw2 ()

for entryNum in range (0 , tree . GetEntries ()):
  # read
  tree . GetEntry ( entryNum )

  # Event Selection: 4jets, 2bjets, 1lepton, 1neutrino
  # 4 jets
  if len(getattr ( tree , "jet_pt" )) != 4:
    continue

  # 2 b-jets
  if getattr ( tree , "n_bjets25_60" ) != 2:
    continue

  # 1 lepton
  if (getattr ( tree , "n_el" ) + getattr ( tree , "n_mu" )) != 1:
    continue

  # Lorentz vectors
  # lepton
  lepton = ROOT . TLorentzVector ()

  if getattr ( tree , "n_el" ) == 1 and getattr ( tree , "n_mu" ) == 0:
    lpt = getattr ( tree , "el_pt" )
    leta = getattr ( tree , "el_eta" )
    lphi = getattr ( tree , "el_phi" )
    lm = 0.000511 # electron mass


  if getattr ( tree , "n_mu" ) == 1 and getattr ( tree , "n_el" ) == 0:
    lpt = getattr ( tree , "mu_pt" )
    leta = getattr ( tree , "mu_eta" )
    lphi = getattr ( tree , "mu_phi" )
    lm = 0.10566 # muon mass

  lepton . SetPtEtaPhiM ( lpt[0] , leta[0] , lphi[0] , lm) 

  # neutrino
  nu = ROOT . TLorentzVector ()
  npx = - getattr ( tree , "met_x" )
  npy = - getattr ( tree , "met_y" )
  npz = 0
  nE = - np.sqrt((getattr ( tree , "met_x" ))**2 + (getattr ( tree , "met_y" ))**2)
  nu . SetPxPyPzE ( npx , npy , npz , nE)

  # jets
  q1 = ROOT . TLorentzVector ()
  q2 = ROOT . TLorentzVector ()
  q3 = ROOT . TLorentzVector ()
  q4 = ROOT . TLorentzVector ()


  qpt = getattr ( tree , "jet_pt" )
  qeta = getattr ( tree , "jet_eta" )
  qphi = getattr ( tree , "jet_phi" )
  qE = getattr ( tree , "jet_E" )

  q1 . SetPtEtaPhiE ( qpt[0] , qeta[0] , qphi[0] , qE[0])
  q2 . SetPtEtaPhiE ( qpt[1] , qeta[1] , qphi[1] , qE[1])
  q3 . SetPtEtaPhiE ( qpt[2] , qeta[2] , qphi[2] , qE[2])
  q4 . SetPtEtaPhiE ( qpt[3] , qeta[3] , qphi[3] , qE[3])
  
  # tt mass
  ttpair = lepton + nu + q1 + q2 + q3 + q4
  ttMass = ttpair . M ()

  # Fill the hist
  tt . Fill ( ttMass )

# write new root file
tt . SetDirectory (0)
inFile . Close ()
outHistFile = ROOT . TFile . Open ( outFileName , "RECREATE" )
outHistFile . cd ()
tt . Write ()
outHistFile . Close ()



