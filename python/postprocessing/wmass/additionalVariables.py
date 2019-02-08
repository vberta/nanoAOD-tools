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

def evaluateRecoilPt(mu_pt, mu_phi, met_pt, met_phi) :
    p_x = mu_pt*sin(mu_phi)
    p_y = mu_pt*cos(mu_phi)
    met_x = met_pt*sin(met_phi)
    met_y = met_pt*cos(met_phi)
    h_x =  -p_x-met_x
    h_y =  -p_y-met_y
    h = sqrt((h_x)**2+(h_y)**2)
    return h

def evaluateRecoilPhi(mu_phi, met_phi) :
    hphi = mu_phi+met_phi
    hphi = hphi % (2*math.pi)
    return hphi

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
        self.metdict = {
        "pf" : "",
        "gen" : "Gen",
        "tk" : "Tk",
        "puppi" : "Puppi"
        }
        pass

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for met in self.metdict :
            self.out.branch("Muon_mt_%s" % self.metdict[met], "F", lenVar="nMuons")
            self.out.branch("Muon_recoil_pt_%s" % self.metdict[met], "F", lenVar="nMuons")
            self.out.branch("Muon_recoil_phi_%s" % self.metdict[met], "F", lenVar="nMuons")
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        #collections
        muons = Collection(event, "Muon")

        for met in self.metdict :

            #collections
            met_pt = getattr(event,"%sMET_pt" % self.metdict[met])
            met_phi = getattr(event,"%sMET_phi" % self.metdict[met])

            #final vectors
            Mt_vec = []
            Recoil_pt_vec = []
            Recoil_phi_vec = []

            for mu in muons :

                #transverse mass
                mt = evaluateMt(mu.pt, mu.phi,met_pt,met_phi)

                #recoil
                h = evaluateRecoilPt(mu.pt, mu.phi,met_pt,met_phi)
                hphi = evaluateRecoilPhi( mu.phi,met_phi)

                Mt_vec.append(mt)
                Recoil_pt_vec.append(h)
                Recoil_phi_vec.append(hphi)

            self.out.fillBranch("Muon_mt_%s" % self.metdict[met], Mt_vec)
            self.out.fillBranch("Muon_recoil_pt_%s" % self.metdict[met], Recoil_pt_vec)
            self.out.fillBranch("Muon_recoil_phi_%s" % self.metdict[met], Recoil_phi_vec)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

addVarModule = lambda : additionalVariables()
