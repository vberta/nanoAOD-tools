#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

from preselection import *
from lepSelection import *
from CSVariables import *
from Wproducer import *

#input_file = "/gpfs/ddn/srm/cms/store/mc/RunIISummer16NanoAODv3/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/120000/06544C90-EFDF-E811-80E6-842B2B6F5D5C.root" 
input_file = "/gpfs/ddn/srm/cms/store/mc/RunIISummer16NanoAODv3/DYJetsToLL_Pt-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v2/280000/26DE6A2F-9329-E911-8766-002590DE6E8A.root"

p = PostProcessor(outputDir=".",        
                  inputFiles=[input_file],
                  modules=[puAutoWeight(), preselection(), leptonSelectModule(), CSAngleModule(), WproducerModule()],
                  provenance=True,
                  outputbranchsel="keep_and_drop.txt")
p.run()



