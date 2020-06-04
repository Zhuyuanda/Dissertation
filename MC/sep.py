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

# creat 4 empty hist
t1 = ROOT . TH1D ( "tlvb" ," m_{t->lvb} , data " ,150 ,0 ,600 )
t1 . Sumw2 ()

t2 = ROOT . TH1D ( "tqqb" ," m_{t->qqb} , data " ,150 ,0 ,600 )
t2 . Sumw2 ()

w1 = ROOT . TH1D ( "wlv" ," m_{w->lv} , data " ,150 ,0 ,600 )
w1 . Sumw2 ()

w2 = ROOT . TH1D ( "wqq" ," m_{w->qq} , data " ,150 ,0 ,600 )
w2 . Sumw2 ()


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
  nE = np.sqrt(npx**2+npy**2)
  nu . SetPxPyPzE ( npx , npy , npz , nE)

  # jets
  q1 = ROOT . TLorentzVector ()
  q2 = ROOT . TLorentzVector ()
  b1 = ROOT . TLorentzVector ()
  b2 = ROOT . TLorentzVector ()


  if (getattr(tree, "jet_btag77")):
    bpt = getattr ( tree , "jet_pt" )
    beta = getattr ( tree , "jet_eta" )
    bphi = getattr ( tree , "jet_phi" )
    bE = getattr ( tree , "jet_E" )

    b1 . SetPtEtaPhiE ( bpt[0] , beta[0] , bphi[0] , bE[0])
    b2 . SetPtEtaPhiE ( bpt[1] , beta[1] , bphi[1] , bE[1])

  else:
    qpt = getattr ( tree , "jet_pt" )
    qeta = getattr ( tree , "jet_eta" )
    qphi = getattr ( tree , "jet_phi" )
    qE = getattr ( tree , "jet_E" )

    q1 . SetPtEtaPhiE ( qpt[0] , qeta[0] , qphi[0] , qE[0])
    q2 . SetPtEtaPhiE ( qpt[1] , qeta[1] , qphi[1] , qE[1])
  

  # W mass
  wlv = lepton + nu  # w1
  w1m = wlv.M()      

  wqq = q1 + q2      # w2
  w2m = wqq.M()

  # Top mass
  w1b1 = (wlv + b1).M()
  w2b2 = (wqq + b2).M()

  w1b2 = (wlv + b2).M()
  w2b1 = (wqq + b1).M()

  chi1 = (w1b1 - 173)**2 + (w2b2 - 173)**2
  chi2 = (w1b2 - 173)**2 + (w2b1 - 173)**2

  if chi1 <= chi2:
    tlvb = w1b1
    tqqb = w2b2

  else:
    tlvb = w1b2
    tqqb = w2b1

  # Fill the hist
  w1 . Fill ( w1m )
  w2 . Fill ( w2m )
  t1 . Fill ( tlvb )
  t2 . Fill ( tqqb )

# write new root file
w1 . SetDirectory (0)
w2 . SetDirectory (0)
t1 . SetDirectory (0)
t2 . SetDirectory (0)
inFile . Close ()
outHistFile = ROOT . TFile . Open ( outFileName , "RECREATE" )
outHistFile . cd ()
w1 . Write ()
w2 . Write ()
t1 . Write ()
t2 . Write ()
outHistFile . Close ()



