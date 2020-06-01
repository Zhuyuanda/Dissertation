import sys  # Import the sys(tem) library for arguments
import ROOT # Import the ROOT library for many uses
 
# Check that the user gave the correct number of arguments
if len(sys.argv) != 3: 
    # Wrong number of arguments, tell the user what you expected
    # Note that sys.argv[0] is how the user called the python script
    print "USAGE: %s <input histogram file> <output plot file>"%(sys.argv[0])
    # End the program
    sys.exit(1)

# Store the user arguments
histFileName = sys.argv[1]
plotFileName = sys.argv[2]

# Retrieve the data histogram from the file
# Open the file in read-only mode
histFile  = ROOT.TFile.Open(histFileName,"READ")
# Get the data histogram
dataHisto = histFile.Get("data")
# Make sure you got the histogram
if not dataHisto:
    print "Failed to get data histogram from the input file"
    sys.exit(1)
# Set the histogram to continue to exist after closing the file
dataHisto.SetDirectory(0)
# Close the input histogram file
histFile.Close()


# Basic style
# Turn off the statistics box
dataHisto.SetStats(0)
# Set the line color to red for MC and black for data
dataHisto.SetLineColor(ROOT.kBlack)
# Set the line width to 2 for MC and data
dataHisto.SetLineWidth(2)
# Set axis labels
dataHisto.GetYaxis().SetTitle("Number of events")
dataHisto.GetXaxis().SetTitle("m_{H} [GeV]")


# Prepare the canvas for plotting
# Make a canvas
canvas = ROOT.TCanvas("canvas")
# Move into the canvas (so anything drawn is part of this canvas)
canvas.cd()
# Set the y-axis to be logarithmic
canvas.SetLogy(True)


# Open the canvas for continuous printing
# This works for a few file types, most notably pdf files
# This allows you to put several plots in the same pdf file
# The key is the opening square-bracket after the desired file name
canvas.Print(plotFileName+"[")

# Draw the data histogram, as data Points with Errors
dataHisto.Draw("pe")
# Write the data histogram plot to the output file
canvas.Print(plotFileName)

# Fit a Gaussian to the histogram
# "gaus" is one of the built-in fit types
# Fit in the range of 81 to 101 GeV (near the Z-peak)
gaussFit = ROOT.TF1("gaussfit","gaus",80,150)
# Fit the function to the histogram using improved Error (uncertainty) treatment
dataHisto.Fit(gaussFit,"E")
dataHisto.Draw("pe")

# Add the fit results to the plot
# Create the TLatex object
latex = ROOT.TLatex()
# Set the coordinates to be percent-based
latex.SetNDC()
latex.SetTextSize(0.03)
# Get the chi2/ndof
chi2 = gaussFit.GetChisquare()
ndof = gaussFit.GetNDF()
# Draw the mean, width, and chi2/ndof
latex.DrawText(0.5,0.80,"Mean = %.1f GeV"%(gaussFit.GetParameter(1)))
latex.DrawText(0.5,0.75,"Width = %.1f GeV"%(gaussFit.GetParameter(0)))
latex.DrawText(0.5,0.7,"chi2/ndof = %.1f/%d = %.1f"%(chi2,ndof,chi2/ndof))
# Write the plot to the output file
canvas.Print(plotFileName)
canvas.Print(plotFileName + "]")
