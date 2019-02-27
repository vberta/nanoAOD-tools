from ROOT import *
from ROOT import gStyle
import argparse
gROOT.Reset()
gROOT.SetBatch(True)
gStyle.SetOptStat("eMRuoi")  #(012211100)
from definitions import variables


parser = argparse.ArgumentParser("Fast Plotter for postprocessing")
parser.add_argument('-Nevents',     '--Nevents',        type=int,  default=100,               action='store', help='number of events to plot')
parser.add_argument('-inputFile',   '--inputFile',      type=str,                             action='store', help='input file. No default provided')
parser.add_argument('-outputFile',  '--outputFile',     type=str, default='DQM_output.root',  action='store', help='output file name')
parser.add_argument('-dataset',     '--dataset',        type=str, default='dataset',          action='store', help='dataset name')

args = parser.parse_args()
Nevents     = args.Nevents
inputFile   = args.inputFile
outputFile  = args.outputFile
dataset     = args.dataset


myfile = TFile(inputFile)
mytree = myfile.Events

print("tree entries",mytree.GetEntries())

variables
canvaslist = {}
histolist = {}
output = TFile(outputFile,"recreate")

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
        # print(hName, var["name"])
        mytree.Project(hName,var["name"],"Vtype=="+goodV,"",Nevents)
        # print(histolist[hName].GetEntries())
        histolist[hName].GetXaxis().SetTitle(var["title"])

        canvaslist['c_'+key_part+'_'+key_var] = TCanvas('c_'+key_part+'_'+key_var,'c_'+key_part+'_'+key_var, 800,600)
        canvaslist['c_'+key_part+'_'+key_var].cd()
        histolist[hName].Draw()
        canvaslist['c_'+key_part+'_'+key_var].SetGrid()

        legSample = TLegend(0.1,0.95,0.7,0.9);
        legSample.SetHeader(dataset)
        legSample.SetBorderSize(0)
        legSample.Draw("SAME")
        legSample.SetFillStyle(0);

        canvaslist['c_'+key_part+'_'+key_var].SaveAs(dataset+'_'+key_part+'_'+key_var+'.png')

        output.cd()
        canvaslist['c_'+key_part+'_'+key_var].Write()
        histolist[hName].Write()
