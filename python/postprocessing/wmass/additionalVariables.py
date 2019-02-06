import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TLorentzVector
import math
from math import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


def evaluateMt(mu_pt, mu_phi, met_pt, met_phi) :
    muvec = TLorentzVector()
    muvec.SetPtEtaPhiM(mu_pt,0,mu_phi,0)
    metvec = TLorentzVector()
    metvec.SetPtEtaPhiE(met_pt,0,met_phi,0)
    deltaphi=metvec.DeltaPhi(muvec)
    mt = sqrt(2*mu_pt*met_pt*(1-cos(deltaphi)))
    return mt

def evaluateRecoil(mu_pt, mu_phi, met_pt, met_phi) :
    p_x = mu_pt*sin(mu_phi)
    p_y = mu_pt*cos(mu_phi)
    met_x = met_pt*sin(met_phi)
    met_y = met_pt*cos(met_phi)
    h_x =  -p_x-met_x
    h_y =  -p_y-met_y
    h = sqrt((h_x)**2+(h_y)**2)
    return h

def evaluateMtRecoBased(mu_pt, mu_phi, met_pt, met_phi) :
    p_x = mu_pt*sin(mu_phi)
    p_y = mu_pt*cos(mu_phi)
    met_x = met_pt*sin(met_phi)
    met_y = met_pt*cos(met_phi)
    h_x =  -p_x-met_x
    h_y =  -p_y-met_y
    mt_h = sqrt(2*(mu_pt*sqrt((p_x+h_x)**2+(p_y+h_y)**2)+mu_pt**2+p_x*h_x+p_y*h_y))
    return mt_h


class additionalVariables(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Muon_mt", "F", lenVar="nMuons")
        self.out.branch("Muon_recoil", "F", lenVar="nMuons")
        self.out.branch("Muon_mt_tk", "F", lenVar="nMuons")
        self.out.branch("Muon_recoil_tk", "F", lenVar="nMuons")
        # self.out.branch("Muon_mt_recoil", "F", lenVar="nMuons")#recoil based Mt



    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        #collections
        muons = Collection(event, "Muon")
        met_pt = event.MET_pt
        met_phi = event.MET_phi
        met_pt_trk= event.TkMET_pt
        met_phi_trk = event.TkMET_phi

        #final vectors
        Mt_vec = []
        Recoil_vec = []
        Mt_trk_vec = []
        Recoil_trk_vec = []
        # Mt_recoil_vec = []

        for mu in muons :

            #transverse mass
            mt = evaluateMt(mu.pt, mu.phi,met_pt,met_phi)

            #recoil
            h = evaluateRecoil(mu.pt, mu.phi,met_pt,met_phi)

            #tk based variables
            mt_trk = evaluateMt(mu.pt, mu.phi,met_pt_trk,met_phi_trk)
            h_trk = evaluateRecoil(mu.pt, mu.phi,met_pt_trk,met_phi_trk)

            #transvese mass recoil based
            # mt_h = evaluateMtRecoBased(mu.pt, mu.phi,met_pt,met_phi)

            Mt_vec.append(mt)
            Recoil_vec.append(h)
            Mt_trk_vec.append(mt_trk)
            Recoil_trk_vec.append(h_trk)
            # Mt_recoil_vec.append(mt_h)

        self.out.fillBranch("Muon_mt", Mt_vec)
        self.out.fillBranch("Muon_recoil", Recoil_vec)
        self.out.fillBranch("Muon_mt_tk", Mt_trk_vec)
        self.out.fillBranch("Muon_recoil_tk", Recoil_trk_vec)
        # self.out.fillBranch("Muon_mt_recoil", Mt_recoil_vec)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

addVarModule = lambda : additionalVariables()
