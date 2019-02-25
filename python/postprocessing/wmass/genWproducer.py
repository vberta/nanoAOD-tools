import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

def getWvariables(muon, neutrino):
    m = ROOT.TLorentzVector()
    n = ROOT.TLorentzVector()
    w = ROOT.TLorentzVector()
    m.SetPtEtaPhiM(muon.pt, muon.eta, muon.phi, muon.mass)
    n.SetPtEtaPhiM(neutrino.pt, neutrino.eta, neutrino.phi, 0.)
    w = m + n
    return w.Pt(), w.Rapidity(), w.Phi(), w.M()

class genWproducer(Module):
    def __init__(self,  Wtypes=['bare', 'preFSR', 'dress']):
        self.Wtypes = Wtypes
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for t in self.Wtypes:
            for v in ['qt', 'y', 'phi', 'mass', 'charge']:                
                self.out.branch("W_"+t+"_"+v, "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        (Wpt_bare, Wrap_bare, Wphi_bare, Wmass_bare, Wcharge_bare) = (0., 0., 0., 0., -1)
        (Wpt_preFSR, Wrap_preFSR, Wphi_preFSR, Wmass_preFSR, Wcharge_preFSR) =  (0., 0., 0., 0., -1)
        (Wpt_dress, Wrap_dress, Wphi_dress, Wmass_dress, Wcharge_dress) =  (0., 0., 0., 0., -1)

        # reobtain the indices of the good muons and the neutrino
        if event.genVtype==14:
            genParticles = Collection(event, "GenPart")
            genDressedLeptons = Collection(event,"GenDressedLepton")
            bareMuonIdx = event.Idx_mu_bare
            NeutrinoIdx = event.Idx_nu
            preFSRMuonIdx = event.Idx_mu_preFSR
            dressMuonIdx = event.Idx_mu_dress
            if(bareMuonIdx>=0) :
                (Wpt_bare, Wrap_bare, Wphi_bare, Wmass_bare), Wcharge_bare = getWvariables(genParticles[bareMuonIdx], genParticles[NeutrinoIdx]), genParticles[bareMuonIdx].pdgId
            if(preFSRMuonIdx>=0) :
                (Wpt_preFSR, Wrap_preFSR, Wphi_preFSR, Wmass_preFSR), Wcharge_preFSR = getWvariables(genParticles[preFSRMuonIdx], genParticles[NeutrinoIdx]), genParticles[preFSRMuonIdx].pdgId
            if(dressMuonIdx>=0) :
                (Wpt_dress, Wrap_dress, Wphi_dress, Wmass_dress), Wcharge_dress = getWvariables(genDressedLeptons[dressMuonIdx], genParticles[NeutrinoIdx]), genDressedLeptons[dressMuonIdx].pdgId
        
        self.out.fillBranch("W_bare_qt",Wpt_bare)
        self.out.fillBranch("W_bare_y",Wrap_bare)
        self.out.fillBranch("W_bare_phi",Wphi_bare)
        self.out.fillBranch("W_bare_mass",Wmass_bare)
        self.out.fillBranch("W_bare_charge",Wcharge_bare)
        self.out.fillBranch("W_preFSR_qt",Wpt_preFSR)
        self.out.fillBranch("W_preFSR_y",Wrap_preFSR)
        self.out.fillBranch("W_preFSR_phi",Wphi_preFSR)
        self.out.fillBranch("W_preFSR_mass",Wmass_preFSR)
        self.out.fillBranch("W_preFSR_charge",Wcharge_preFSR)
        self.out.fillBranch("W_dress_qt",Wpt_dress)
        self.out.fillBranch("W_dress_y",Wrap_dress)
        self.out.fillBranch("W_dress_phi",Wphi_dress)
        self.out.fillBranch("W_dress_mass",Wmass_dress)
        self.out.fillBranch("W_dress_charge",Wcharge_dress)

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

genWproducerModule = lambda : genWproducer()
