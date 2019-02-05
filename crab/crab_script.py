#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from PhysicsTools.NanoAODTools.postprocessing.wmass.lepSelection import *
from PhysicsTools.NanoAODTools.postprocessing.wmass.CSVariables import *
from PhysicsTools.NanoAODTools.postprocessing.wmass.Wproducer import *

p=PostProcessor(".",inputFiles(),"",modules=[leptonSelectModule(),CSAngleModule(), WproducerModule()],provenance=True,fwkJobReport=True,jsonInput=runsAndLumis(),outputbranchsel="keep_and_drop.txt")
p.run()

print "DONE"
os.system("ls -lR")

