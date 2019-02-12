import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TLorentzVector
import math
from math import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


def evaluateMt(mu_pt, mu_phi, met_pt, met_phi) :
    muvec = TLorentzVector()
    muvec.SetPtEtaPhiM(mu_pt,0.0,mu_phi,0.106)
    metvec = TLorentzVector()
    metvec.SetPtEtaPhiM(met_pt,0.0,met_phi,0.0)
    hvec = -(muvec + metvec)
    (mt, h_pt, h_phi, met_par, met_per) = (hvec.M(), hvec.Pt(), hvec.Phi(), 
                                           metvec.Vect().Dot(muvec.Vect().Unit()), metvec.Vect().Cross(muvec.Vect().Unit()).Pz())
    return  (mt, h_pt, h_phi, met_par, met_per) 

class additionalVariables(Module):
    def __init__(self, isMC=True, doJESVar=False, doJERVar=False, doUnclustVar=False):
        self.metdict = {
            "pf"    : { "tag" : "MET",      "var"  : [""] },
            "tk"    : { "tag" : "TkMET",    "var"  : [""] },
            "puppi" : { "tag" : "PuppiMET", "var"  : [""] },
            }
        if isMC:
            self.metdict["gen"] = {"tag" : "GenMET", "var"  : [""]}
            if doJERVar:
                self.metdict["pf"]["var"].extend( ["_nom", "_jerUp", "_jerDown"] )
            if doJESVar:
                self.metdict["pf"]["var"].extend( ["_jesTotalUp", "_jesTotalDown"] )
            if doUnclustVar:
                self.metdict["pf"]["var"].extend( ["_unclustEnUp", "_unclustEnDown"] )
        pass

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for key,met in self.metdict.items() :
            for ivar,var in enumerate(met["var"]):
                self.out.branch("Muon_%s%s_mt" % (met["tag"], var), "F", lenVar="nMuons", title="Transverse mass using "+met["tag"]+" syst "+var+" MET")
                self.out.branch("Muon_%s%s_recoil_pt"  % (met["tag"], var), "F", lenVar="nMuons", title="Recoil Pt using "+met["tag"]+" syst "+var+" MET")
                self.out.branch("Muon_%s%s_recoil_phi" % (met["tag"], var), "F", lenVar="nMuons", title="Recoil Phi using "+met["tag"]+" syst "+var+" MET")
                self.out.branch("Muon_%s%s_met_par" % (met["tag"], var), "F", lenVar="nMuons", title="MET projected along mu using "+met["tag"]+" syst "+var+" MET")
                self.out.branch("Muon_%s%s_met_per" % (met["tag"], var), "F", lenVar="nMuons", title="MET perpendicular to mu using "+met["tag"]+" syst "+var+" MET")
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        #collections
        muons = Collection(event, "Muon")

        #final vectors
        Mt_vec         = [0.0]*len(muons)
        Recoil_pt_vec  = [0.0]*len(muons)
        Recoil_phi_vec = [0.0]*len(muons)
        met_par_vec    = [0.0]*len(muons)
        met_per_vec    = [0.0]*len(muons)

        for key,met in self.metdict.items() :
            for ivar,var in enumerate(met["var"]):
                met_pt  = getattr(event,"%s_pt%s"  % (met["tag"], var))
                met_phi = getattr(event,"%s_phi%s" % (met["tag"], var))
                for imu,mu in enumerate(muons) :
                    (mt,hpt,hphi,met_par,met_per) = evaluateMt(mu.pt, mu.phi, met_pt, met_phi)
                    Mt_vec[imu] = mt
                    Recoil_pt_vec[imu] = hpt
                    Recoil_phi_vec[imu] = hphi
                    met_par_vec[imu] = met_par
                    met_per_vec[imu] = met_per
                self.out.fillBranch("Muon_%s%s_mt" % (met["tag"], var), Mt_vec)
                self.out.fillBranch("Muon_%s%s_recoil_pt"  % (met["tag"], var), Recoil_pt_vec)
                self.out.fillBranch("Muon_%s%s_recoil_phi" % (met["tag"], var), Recoil_phi_vec)
                self.out.fillBranch("Muon_%s%s_met_par" % (met["tag"], var), met_par_vec)
                self.out.fillBranch("Muon_%s%s_met_per" % (met["tag"], var), met_per_vec)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

addVarModule = lambda : additionalVariables()
