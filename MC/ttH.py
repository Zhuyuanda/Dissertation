import ROOT
import sys

if len ( sys . argv ) != 3:
  print " USAGE : % s < input file > < output file > " %( sys . argv [0])
  sys . exit (1)
inFileName = sys . argv [1]
outFileName = sys . argv [2]
print " Reading from " , inFileName , " and writing to " , outFileName

# read
inFile = ROOT . TFile . Open ( inFileName , " READ " )
tree = inFile . Get ( "ttHyyTree" )

mH = ROOT . TH1D ( "data" ," m_{H} , data " ,150 ,100 ,200 )
mH . Sumw2 ()

for entryNum in range (0 , tree . GetEntries ()):
  # read
  tree . GetEntry ( entryNum )

  # 2 b-jets
  if len(getattr ( tree , "jet_pt" )) != 2:
    continue

  # 4-vectors
  y0 = ROOT . TLorentzVector ()
  y1 = ROOT . TLorentzVector ()

  # y0
  pt0 = getattr ( tree , "y1_pt" )
  eta0 = getattr ( tree , "y1_eta" )
  phi0 = getattr ( tree , "y1_phi" )
  nrg0 = getattr ( tree , "y1_E" )
  y0 . SetPtEtaPhiE ( pt0 , eta0 , phi0 , nrg0)

  # y1
  pt1 = getattr ( tree , "y2_pt" )
  eta1 = getattr ( tree , "y2_eta" )
  phi1 = getattr ( tree , "y2_phi" )
  nrg1 = getattr ( tree , "y2_E" )
  y1 . SetPtEtaPhiE ( pt1 , eta1 , phi1 , nrg1)

  # weight
  #weight = getattr ( tree , "weight_total" )

  # Higgs mass
  higgs = y0 + y1
  higgsMass = higgs . M ()
  # Fill the hist
  mH . Fill ( higgsMass )

mH . SetDirectory (0)
inFile . Close ()
outHistFile = ROOT . TFile . Open ( outFileName , "RECREATE" )
outHistFile . cd ()
mH . Write ()
outHistFile . Close ()



