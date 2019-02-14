#!/usr/bin/env python
import os, sys
import ROOT
import argparse
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *

from PhysicsTools.NanoAODTools.postprocessing.wmass.preselection import *
from PhysicsTools.NanoAODTools.postprocessing.wmass.additionalVariables import *
from PhysicsTools.NanoAODTools.postprocessing.wmass.lepSelection import *
from PhysicsTools.NanoAODTools.postprocessing.wmass.CSVariables import *
from PhysicsTools.NanoAODTools.postprocessing.wmass.Wproducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer import *

parser = argparse.ArgumentParser("")
parser.add_argument('-jobNum', '--jobNum',   type=int, default=1,      help="")
parser.add_argument('-passall', '--passall', type=int, default=0,      help="")
parser.add_argument('-isMC', '--isMC',       type=int, default=1,      help="")
parser.add_argument('-dataYear', '--dataYear',type=int, default=2016, help="")
parser.add_argument('-jesUncert', '--jesUncert',type=str, default="Total", help="")
parser.add_argument('-redojec', '--redojec',  type=int, default=0,      help="")
args = parser.parse_args()
isMC = args.isMC
passall = args.passall
dataYear = args.dataYear
jecTag=("Summer16_07Aug2017_V11_MC" if dataYear==2016 else "Fall17_17Nov2017_V32_MC")
jmeUncert=[x for x in args.jesUncert.split(",")]

print "isMC =", isMC, ", passall =", passall, ", dataYear =", dataYear
if isMC:
    print "JECTag =", jecTag, "jesUncertainties =", jmeUncert, " redoJec =", args.redojec

jmeCorrections = lambda : jetmetUncertaintiesProducer(era=str(dataYear), globalTag=jecTag, jesUncertainties = jmeUncert, redoJEC= args.redojec)

muonScaleRes = muonScaleRes2016
if dataYear==2017:
    muonScaleRes = muonScaleRes2017

modules = []
if isMC:
    modules = [puAutoWeight(), 
               preselection(isMC=isMC, passall=passall, dataYear=dataYear), 
               lepSF(),
               muonScaleRes(),
               jmeCorrections(),
               additionalVariables(isMC=isMC, doJESVar=True, doJERVar=True, doUnclustVar=True, dataYear=dataYear), 
               leptonSelectModule(), 
               CSAngleModule(), 
               WproducerModule()]
else:
    modules = [preselection(isMC=isMC, passall=passall, dataYear=dataYear), 
               muonScaleRes(),
               additionalVariables(isMC=isMC)]

p = PostProcessor(outputDir=".",        
                  inputFiles=inputFiles(),
                  modules=modules,
                  provenance=True,
                  outputbranchsel="keep_and_drop_"+("MC" if isMC else "Data")+".txt",
                  fwkJobReport=True,
                  jsonInput=runsAndLumis())
p.run()

print "DONE"
os.system("ls -lR")


