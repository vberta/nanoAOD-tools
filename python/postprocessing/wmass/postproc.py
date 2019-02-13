#!/usr/bin/env python
import os, sys
import ROOT
import argparse

ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *

from preselection import *
from additionalVariables import *
from lepSelection import *
from CSVariables import *
from Wproducer import *

parser = argparse.ArgumentParser("")
parser.add_argument('-jobNum', '--jobNum',    type=int, default=1,      help="")
parser.add_argument('-passall', '--passall',  type=int, default=0,      help="")
parser.add_argument('-isMC', '--isMC',        type=int, default=1,      help="")
parser.add_argument('-dataYear', '--dataYear',type=int, default=2016, help="")
args = parser.parse_args()
isMC    = args.isMC
passall = args.passall
dataYear = args.dataYear
print "isMC =", isMC, ", passall =", passall, ", dataYear =", dataYear

input_dir = "/gpfs/ddn/srm/cms/store/"

input_files = []
modules = []

#Rochester correction for muons
muonScaleRes = muonScaleRes2016
if dataYear==2017:
    muonScaleRes = muonScaleRes2017

if isMC:
    input_files.append( 
        #input_dir+"mc/RunIISummer16NanoAODv3/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/120000/06544C90-EFDF-E811-80E6-842B2B6F5D5C.root",
        input_dir+"mc/RunIISummer16NanoAODv3/DYJetsToLL_Pt-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v2/280000/26DE6A2F-9329-E911-8766-002590DE6E8A.root",
        )
    modules = [puAutoWeight(), 
               preselection(isMC=isMC, passall=passall, dataYear=dataYear), 
               muonScaleRes(),
               jetmetUncertaintiesProducer(era=str(dataYear), globalTag=("Summer16_23Sep2016V4_MC" if dataYear==2016 else "Fall17_17Nov2017_V6_MC"), jesUncertainties=["Total"]), 
               additionalVariables(isMC=isMC, doJESVar=True, doJERVar=True, doUnclustVar=True), 
               leptonSelectModule(), 
               CSAngleModule(), 
               WproducerModule()]
else:
    input_files.append(
        input_dir+"data/Run2016D/DoubleEG/NANOAOD/Nano14Dec2018-v1/280000/481DA5C0-DF96-5640-B5D1-208F52CAC829.root"
        )
    modules = [preselection(isMC=isMC, passall=passall, dataYear=dataYear), 
               muonScaleRes(),
               additionalVariables(isMC=isMC)]

p = PostProcessor(outputDir=".",        
                  inputFiles=input_files,
                  modules=modules,
                  provenance=True,
                  outputbranchsel="keep_and_drop_"+("MC" if isMC else "Data")+".txt")
p.run()

print "DONE"
os.system("ls -lR")


