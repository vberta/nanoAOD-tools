import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class preselection(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Muon_selIdx", "I")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        # Trigger bit
        #triggers = Collection(event, "HLT")       
        #muon_bits = triggers.IsoMu24

        # Muon selection
        all_muons = Collection(event, "Muon")

        sel_muons = [ [mu,imu] for imu,mu in enumerate(all_muons) if (abs(mu.eta)<2.4 and mu.pt>15 and mu.isPFcand and mu.pfRelIso04_all<0.30)]
        if len(sel_muons)!=1: return False
        (muon,imuon) = (sel_muons[0][0], sel_muons[0][1])
        if not(muon.pt>20 and muon.mediumId): return False
        self.out.fillBranch("Muon_selIdx", imuon)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

preselectionModule = lambda : preselection() 
