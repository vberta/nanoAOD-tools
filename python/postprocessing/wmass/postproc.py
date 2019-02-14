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
from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer import *

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

jetmetUncertainties = jetmetUncertainties2016
if dataYear==2017:
    jetmetUncertainties = jetmetUncertainties2017

if isMC:
    if dataYear==2016:
        input_files.append( 
            input_dir+"mc/RunIISummer16NanoAODv3/DYJetsToLL_Pt-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v2/280000/26DE6A2F-9329-E911-8766-002590DE6E8A.root")
    else:
        input_files.append(        
            input_dir+"/mc/RunIIFall17NanoAODv4/DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/00000/CE931735-B298-B24F-A127-ADB477C76D83.root"
            )
    modules = [puAutoWeight(), 
               preselection(isMC=isMC, passall=passall, dataYear=dataYear), 
               lepSF(),
               muonScaleRes(),
               jetmetUncertainties(),
               additionalVariables(isMC=isMC, doJESVar=True, doJERVar=True, doUnclustVar=True, dataYear=dataYear), 
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
                  cut="Entry$<=10000",
                  modules=modules,
                  provenance=True,
                  outputbranchsel="keep_and_drop_"+("MC" if isMC else "Data")+".txt")
p.run()

print "DONE"
os.system("ls -lR")


