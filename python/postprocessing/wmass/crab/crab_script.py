#!/usr/bin/env python
import os, sys
import ROOT
import argparse
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

from PhysicsTools.NanoAODTools.postprocessing.wmass.preselection import *
from PhysicsTools.NanoAODTools.postprocessing.wmass.additionalVariables import *
from PhysicsTools.NanoAODTools.postprocessing.wmass.lepSelection import *
from PhysicsTools.NanoAODTools.postprocessing.wmass.CSVariables import *
from PhysicsTools.NanoAODTools.postprocessing.wmass.Wproducer import *

parser = argparse.ArgumentParser("")
parser.add_argument('-jobNum', '--jobNum',   type=int, default=1,      help="")
parser.add_argument('-passall', '--passall', type=int, default=0,      help="")
parser.add_argument('-isMC', '--isMC',       type=int, default=1,      help="")
args = parser.parse_args()
isMC    = args.isMC
passall = args.passall
print "isMC =", isMC, ", passall=", passall

from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

modules = []
if isMC:
    modules = [puAutoWeight(), preselection(isMC=isMC, passall=passall), additionalVariables(), leptonSelectModule(), CSAngleModule(), WproducerModule()]
else:
    modules = [preselection(isMC=isMC, passall=passall), additionalVariables()]

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


