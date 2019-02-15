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
parser.add_argument('-maxEvents', '--maxEvents', type=int, default=-1,	help="")
parser.add_argument('-dataYear', '--dataYear',type=int, default=2016,    help="")
parser.add_argument('-jesUncert', '--jesUncert',type=str, default="Total", help="")
parser.add_argument('-redojec', '--redojec',  type=int, default=0,       help="")
parser.add_argument('-runPeriod', '--runPeriod',  type=str, default="B", help="")
args = parser.parse_args()
isMC    = args.isMC
passall = args.passall
dataYear = args.dataYear


##create a dictionary for JEC tags
##2017 jec needs to be fixed
jecTagsMC={'2016' : 'Summer16_07Aug2017_V11_MC', '2017' : 'Fall17_17Nov2017_V32_MC'}

jecTagsDATA={ '2016B' : 'Summer16_07Aug2017BCD_V11_DATA', 
              '2016C' : 'Summer16_07Aug2017BCD_V11_DATA', 
              '2016D' : 'Summer16_07Aug2017BCD_V11_DATA', 
              '2016E' : 'Summer16_07Aug2017EF_V11_DATA', 
              '2016F' : 'Summer16_07Aug2017EF_V11_DATA', 
              '2016G' : 'Summer16_07Aug2017GH_V11_DATA', 
              '2016H' : 'Summer16_07Aug2017GH_V11_DATA', 
              '2016H' : 'Summer16_07Aug2017GH_V11_DATA', 
              '2017B' : 'Fall17_17Nov2017B_V32_DATA', 
              '2017C' : 'Fall17_17Nov2017C_V32_DATA', 
              '2017D' : 'Fall17_17Nov2017DE_V32_DATA', 
              '2017E' : 'Fall17_17Nov2017DE_V32_DATA', 
              '2017F' : 'Fall17_17Nov2017F_V32_DATA', 
            }   

jecTag=""
if isMC:
    jecTag=jecTagsMC[str(dataYear)]
else:
    jecTag=jecTagsDATA[str(dataYear) + args.runPeriod]

jmeUncert=[x for x in args.jesUncert.split(",")]

print "isMC =", isMC, ", passall =", passall, ", dataYear =", dataYear, " maxEvents=", args.maxEvents
print "JECTag =", jecTag, "jesUncertainties =", jmeUncert, " redoJec =", args.redojec

input_dir = "/gpfs/ddn/srm/cms/store/"

input_files = []
modules = []

#jme corrections
jmeCorrections=lambda : jetmetUncertaintiesProducer(era=str(dataYear), globalTag=jecTag, jesUncertainties = jmeUncert, redoJEC= args.redojec)

#Rochester correction for muons
muonScaleRes = muonScaleRes2016
if dataYear==2017:
    muonScaleRes = muonScaleRes2017

##This is temporary for testing purpose
ifileMC = "mc/RunIISummer16NanoAODv3/DYJetsToLL_Pt-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v2/280000/26DE6A2F-9329-E911-8766-002590DE6E8A.root"
if dataYear==2017:
    ifileMC = "mc/RunIIFall17NanoAODv4/DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/20000/41874784-9F25-7C49-B4E3-6EECD93B77CA.root"    
ifileDATA="data/Run2016D/DoubleEG/NANOAOD/Nano14Dec2018-v1/280000/481DA5C0-DF96-5640-B5D1-208F52CAC829.root"
if dataYear==2017:
    ifileDATA="data/Run2017E/DoubleMuon/NANOAOD/31Mar2018-v1/710000/A452D873-4B6E-E811-BE23-FA163E60E3B4.root"

if isMC:
    input_files.append( 
        input_dir+ifileMC
        )
    modules = [puAutoWeight(), 
               preselection(isMC=isMC, passall=passall, dataYear=dataYear), 
               lepSF(),
               jmeCorrections(),
               muonScaleRes(),
               additionalVariables(isMC=isMC, doJESVar=True, doJERVar=True, doUnclustVar=True, dataYear=dataYear), 
               leptonSelectModule(), 
               CSAngleModule(), 
               WproducerModule()]
else:
    input_files.append(
        input_dir+ifileDATA
        )
    modules = [preselection(isMC=isMC, passall=passall, dataYear=dataYear), 
               jmeCorrections(),
               muonScaleRes(),
               additionalVariables(isMC=isMC)]

treecut=("Entry$<" + str(args.maxEvents) if args.maxEvents > 0 else "")
p = PostProcessor(outputDir=".",  
                  inputFiles=input_files,
                  cut=treecut,      
                  modules=modules,
                  provenance=True,
                  outputbranchsel="keep_and_drop_"+("MC" if isMC else "Data")+".txt")
p.run()

print "DONE"
os.system("ls -lR")
