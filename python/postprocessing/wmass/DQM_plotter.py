from ROOT import *
import argparse
gROOT.Reset()
gROOT.SetBatch(True)
from definitions import variables


parser = argparse.ArgumentParser("Fast Plotter for postprocessing")
parser.add_argument('-Nevents',     '--Nevents',        type=int,  default=100,               action='store', help='number of events to plot')
parser.add_argument('-inputFile',   '--inputFile',      type=str,                             action='store', help='input file. No default provided')
parser.add_argument('-outputFile',   '--outputFile',    type=str, default='DQM_output.root',  action='store', help='output file name')

args = parser.parse_args()
Nevents     = args.Nevents
inputFile   = args.inputFile
outputFile  = args.outputFile

myfile = TFile(inputFile)
mytree = myfile.Events

print("tree entries",mytree.GetEntries())

variables
canvaslist = {}
histolist = {}
outputFile = TFile("outputFile","recreate")

#dimuon????? check!
for key_part, part in variables.items() :
    if(key_part=="W") :
        goodV = "0"
    elif(key_part=="Z") :
        goodV = "2"
    else :
        goodV = "1"
    for key_var, var in part.items() :

        hName = key_part+'_'+var["name"]
        histolist[hName] = TH1F(hName,hName,var["Nbin"],var["min"],var["max"])
        print(hName, var["name"])
        mytree.Project(hName,var["name"],"Vtype=="+goodV,"",Nevents)
        print(histolist[hName].GetEntries())
        histolist[hName].GetXaxis().SetTitle(var["title"])

        canvaslist['c_'+key_part+'_'+key_var] = TCanvas('c_'+key_part+'_'+key_var,'c_'+key_part+'_'+key_var, 800,600)
        canvaslist['c_'+key_part+'_'+key_var].cd()
        histolist[hName].Draw()
        canvaslist['c_'+key_part+'_'+key_var].SaveAs(key_part+'_'+key_var+'.png')

        outputFile.cd()
        histolist[hName].Write()
