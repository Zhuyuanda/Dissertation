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
tt = ROOT . TH1D ( "data" ," m_{tt} , data " ,150 ,330 ,400 )
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

  # 1 neutrino
  if getattr ( tree , "met" ) == 0:
    continue  

  # Lorentz vectors
  # lepton
  lepton = ROOT . TLorentzVector ()

  if getattr ( tree , "n_el" ) == 1:
    lpt = getattr ( tree , "el_pt" )
    leta = getattr ( tree , "el_eta" )
    lphi = getattr ( tree , "el_phi" )
    lm = 0.00051 # electron mass
    lepton . SetPtEtaPhiM ( lpt , leta , lphi , lm)

  if getattr ( tree , "n_mu" ) == 1:
    lpt = getattr ( tree , "mu_pt" )
    leta = getattr ( tree , "mu_eta" )
    lphi = getattr ( tree , "mu_phi" )
    lm = 0.105 # muon mass
    lepton . SetPtEtaPhiM ( lpt , leta , lphi , lm) 

  # neutrino
  nu = ROOT . TLorentzVector ()
  npx = - getattr ( tree , "met_x" )
  npy = - getattr ( tree , "met_y" )
  npz = 0
  nE = np.sqrt((getattr ( tree , "met_x" ))**2 + (getattr ( tree , "met_y" ))**2)
  nu . SetPxPyPzE ( npx , npy , npz , nE)

  # jets
  q1 = ROOT . TLorentzVector ()
  q2 = ROOT . TLorentzVector ()
  b1 = ROOT . TLorentzVector ()
  b2 = ROOT . TLorentzVector ()

  # q1q2
  if getattr ( tree , "jet_btag77" ) == 0:
    qpt = getattr ( tree , "jet_pt" )
    qeta = getattr ( tree , "jet_eta" )
    qphi = getattr ( tree , "jet_phi" )
    qE = getattr ( tree , "jet_E" )

    q1 . SetPtEtaPhiE ( qpt[0] , qeta[0] , qphi[0] , qE[0])
    q2 . SetPtEtaPhiE ( qpt[1] , qeta[1] , qphi[1] , qE[1])
  
  if getattr ( tree , "jet_btag77" ) == 1:
    bpt = getattr ( tree , "jet_pt" )
    beta = getattr ( tree , "jet_eta" )
    bphi = getattr ( tree , "jet_phi" )
    bE = getattr ( tree , "jet_E" )

    b1 . SetPtEtaPhiE ( bpt[0] , beta[0] , bphi[0] , bE[0])
    b2 . SetPtEtaPhiE ( bpt[1] , beta[1] , bphi[1] , bE[1])

  # tt mass
  ttpair = lepton + nu + q1 + q2 + b1 + b2
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



