#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

#from lepSelection import *
#from CSVariables import *
#from Wproducer import *
from preselection import *

p=PostProcessor(".",
                ["/gpfs/ddn/srm/cms/store/mc/RunIISummer16NanoAODv3/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/120000/06544C90-EFDF-E811-80E6-842B2B6F5D5C.root"],
                #[leptonSelectModule(),CSAngleModule(), WproducerModule()],
                modules=[preselection()],
                provenance=True,
                outputbranchsel="keep_and_drop.txt")
p.run()



