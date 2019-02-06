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
        self.out.branch("Muon_idx1", "I")
        self.out.branch("Muon_idx2", "I")
        self.out.branch("event_Vtype", "I")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        # Trigger bit
        #triggers = Collection(event, "HLT")       
        #muon_bits = triggers.IsoMu24

        # Muon selection
        all_muons = Collection(event, "Muon")

        loose_muons  = [ [mu,imu] for imu,mu in enumerate(all_muons) if (abs(mu.eta)<2.4 and mu.pt>10 and mu.isPFcand and mu.pfRelIso04_all<0.30)]
        medium_muons = [ [mu,imu] for imu,mu in enumerate(all_muons) if (abs(mu.eta)<2.4 and mu.pt>20 and mu.mediumId and mu.pfRelIso04_all<=0.10)]
        medium_aiso_muons = [ [mu,imu] for imu,mu in enumerate(all_muons) if (abs(mu.eta)<2.4 and mu.pt>20 and mu.mediumId and mu.pfRelIso04_all>0.10 and mu.pfRelIso04_all<0.30)]

        loose_muons.sort( key = lambda x: x[0].pt, reverse=True )
        medium_muons.sort(key = lambda x: x[0].pt, reverse=True )
        medium_aiso_muons.sort(key = lambda x: x[0].pt, reverse=True )

        event_flag = -1        
        # W-like event: 1 loose, 1 medium
        if len(medium_muons)==1 and len(loose_muons)==1:
            event_flag = 0
            (idx1, idx2) = (medium_muons[0][1], -1)
        # Fake-like event
        elif len(medium_muons)==0 and len(medium_aiso_muons)==1:
            event_flag = 1
            (idx1, idx2) = (medium_aiso_muons[0][1], -1)
        # Z-like event
        elif len(loose_muons)==2:
            (idx1, idx2) = (loose_muons[0][1], loose_muons[1][1])
            event_flag = 2 if (loose_muons[0][0].charge+loose_muons[1][0].charge)==0 else 3
        # anything else
        else:   
            event_flag = -1

        if event_flag not in [0,1,2,3]: return False

        self.out.fillBranch("Muon_idx1", idx1)
        self.out.fillBranch("Muon_idx2", idx2)
        self.out.fillBranch("event_Vtype", event_flag)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

preselectionModule = lambda : preselection() 
