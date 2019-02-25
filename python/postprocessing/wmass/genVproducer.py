import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

def getVvariables(muon, neutrino):
    m = ROOT.TLorentzVector()
    n = ROOT.TLorentzVector()
    w = ROOT.TLorentzVector()
    m.SetPtEtaPhiM(muon.pt, muon.eta, muon.phi, muon.mass)
    n.SetPtEtaPhiM(neutrino.pt, neutrino.eta, neutrino.phi, 0.)
    w = m + n
    return [w.Pt(), w.Rapidity(), w.Phi(), w.M()]

class genVproducer(Module):
    def __init__(self,  Wtypes=['bare', 'preFSR', 'dress']):
        self.Wtypes = Wtypes
        self.vars = ['qt', 'y', 'phi', 'mass', 'charge']
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for t in self.Wtypes:
            for v in self.vars:                
                self.out.branch("GenV_%s_%s" % (t,v), "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        results = {}
        for t in self.Wtypes:
            for v in self.vars:
                results[t+'_'+v] = 0.0 if v!="charge" else -1
            
        if event.genVtype in [13,14]:
            genParticles = Collection(event, "GenPart")
            genDressedLeptons = Collection(event,"GenDressedLepton")
            idx_nu = event.Idx_nu
            for t in self.Wtypes:
                genCollection = genParticles if t in ["bare", "preFSR"] else genDressedLeptons
                idx_mu1 = getattr(event, "Idx_"+t+"_mu1")
                idx_mu2 = getattr(event, "Idx_"+t+"_mu2")
                if idx_mu1>=0:
                    ps = getVvariables( genCollection[idx_mu1], (genParticles[idx_nu] if idx_nu>=0 else genCollection[idx_mu2]) )
                    ps.append(genCollection[idx_mu1].pdgId)
                    for iv,v in enumerate(self.vars):
                        results["%s_%s" % (t,v)] = ps[iv]

        for t in self.Wtypes:
            for v in self.vars:
                self.out.fillBranch("GenV_%s_%s" % (t,v), results["%s_%s" % (t,v)])

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

genVproducerModule = lambda : genVproducer()
