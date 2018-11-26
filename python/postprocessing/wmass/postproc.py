#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from lepSelection import *
from CSVariables import *
from Wproducer import *

p=PostProcessor(".",["/scratch/emanca/WMass/NanoDevelopment/CMSSW_10_2_6/src/PhysicsTools/NanoAODTools/scripts/inputTree.root"],"","",[leptonSelectModule(),CSAngleModule(), WproducerModule()],provenance=True,outputbranchsel="keep_and_drop.txt")
p.run()



