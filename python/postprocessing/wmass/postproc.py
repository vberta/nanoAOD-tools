#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from lepSelection import *
from CSVariables import *
from Wproducer import *

p=PostProcessor(".",["../../../../NanoAOD/test/test80X_NANO.root"],"","",[leptonSelectModule(),CSAngleModule(), WproducerModule()],provenance=True)
p.run()
