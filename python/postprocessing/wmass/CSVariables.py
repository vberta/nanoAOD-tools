import ROOT
import math
import copy

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

#global definition of CS angles
def azimuth(phi):
    if phi<0.0:
        phi += 2*math.pi
    return phi

def getCSangles(muon,neutrino):

    Lp4  = ROOT.TLorentzVector(0.,0.,0.,0.)
    Np4 = ROOT.TLorentzVector(0.,0.,0.,0.)
    if hasattr(muon, "pt"):
        Lp4.SetPtEtaPhiM(muon.pt, muon.eta, muon.phi, muon.mass)
        Np4.SetPtEtaPhiM(neutrino.pt, neutrino.eta, neutrino.phi, 0.)
    else:
        Lp4.SetPtEtaPhiM(muon.Pt(), muon.Eta(), muon.Phi(), muon.M())
        Np4.SetPtEtaPhiM(neutrino.Pt(), neutrino.Eta(), neutrino.Phi(), 0.)
    Wp4 = Lp4 + Np4
    
    Wp4_rot = copy.deepcopy(Wp4)
    Lp4_rot = copy.deepcopy(Lp4)

    # align W/L along x axis
    Wp4_rot.RotateZ( -Wp4.Phi() )
    Lp4_rot.RotateZ( -Wp4.Phi() )

    # first boost
    boostL = Wp4_rot.BoostVector()
    boostL.SetX(0.0)
    boostL.SetY(0.0)
    Lp4_rot.Boost( -boostL )
    Wp4_rot.Boost( -boostL )

    # second boost
    boostT = Wp4_rot.BoostVector()
    Lp4_rot.Boost( -boostT )

    # the CS frame defines the z-axis according to the W pz in the lab 
    flip_z = -1 if Wp4.Rapidity()<0.0 else +1

    # compute PS point
    ps = (Lp4_rot.CosTheta()*flip_z, azimuth(Lp4_rot.Phi()*flip_z) )
    return ps


class CSVariables(Module):
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
            for v in ['theta', 'phi']:
                self.out.branch("CS_"+t+"_"+v, "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if event.genVtype != 14 :
            CStheta_bare, CSphi_bare     = 0.0, 0.0
            CStheta_preFSR, CSphi_preFSR = 0.0, 0.0
            CStheta_dress, CSphi_dress   = 0.0, 0.0
        else:
            genParticles = Collection(event, "GenPart")
            genDressedLeptons = Collection(event,"GenDressedLepton")
            bareMuonIdx = event.Idx_mu_bare
            NeutrinoIdx = event.Idx_nu
            preFSRMuonIdx = event.Idx_mu_preFSR
            dressMuonIdx = event.Idx_mu_dress
            if(bareMuonIdx>=0) :
                CStheta_bare, CSphi_bare  = getCSangles(genParticles[bareMuonIdx], genParticles[NeutrinoIdx])
            else :
                CStheta_bare, CSphi_bare = 0.0, 0.0
            if(preFSRMuonIdx>=0) :
                CStheta_preFSR, CSphi_preFSR = getCSangles(genParticles[preFSRMuonIdx], genParticles[NeutrinoIdx])
            else :
                CStheta_preFSR, CSphi_preFSR = 0.0, 0.0
            if(dressMuonIdx>=0) :
                CStheta_dress, CSphi_dress = getCSangles(genDressedLeptons[dressMuonIdx], genParticles[NeutrinoIdx])
            else :
                CStheta_dress, CSphi_dress = 0.0, 0.0

        self.out.fillBranch("CS_bare_theta",CStheta_bare)
        self.out.fillBranch("CS_bare_phi",CSphi_bare)

        self.out.fillBranch("CS_preFSR_theta",CStheta_preFSR)
        self.out.fillBranch("CS_preFSR_phi",CSphi_preFSR)

        self.out.fillBranch("CS_dress_theta",CStheta_dress)
        self.out.fillBranch("CS_dress_phi",CSphi_dress)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

CSAngleModule = lambda : CSVariables()
