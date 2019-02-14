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
    def __init__(self, isMC=True, doJESVar=False, doJERVar=False, doUnclustVar=False, dataYear=2016):
        self.mudict = {
            "pf"     : { "tag" : "",             "var"  : [""] },
            "roccor" : { "tag" : "_corrected",   "var"  : [""] },
            }
        if dataYear==2017:
            self.mudict["roccor"]["var"] = ["", "_sys_uncertUp",  "_sys_uncertDown"]

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
        for key_mu,mu in self.mudict.items() :
            for ivar_mu,var_mu in enumerate(mu["var"]):
                for key_met,met in self.metdict.items() :
                    for ivar_met,var_met in enumerate(met["var"]):
                        title_label = "MET: "+met["tag"]+" (syst: "+var_met+"), Muon: "+mu["tag"]+" (syst: "+var_mu+")"
                        branch_label = "%s%s_%s%s" % (mu["tag"], var_mu, met["tag"], var_met)
                        self.out.branch("Muon%s_mt" % branch_label, "F", lenVar="nMuons", title="Mt, "+title_label)
                        self.out.branch("Muon%s_recoil_pt"  % branch_label, "F", lenVar="nMuons", title="Recoil pt, "+title_label)
                        self.out.branch("Muon%s_recoil_phi" % branch_label, "F", lenVar="nMuons", title="Recoil phi, "+title_label)
                        # these are MET-only variables, skip loop over muons
                        if mu["tag"]=="" and var_mu=="":
                            self.out.branch("Muon%s_MET_par" % branch_label, "F", lenVar="nMuons", title="MET || mu, "+title_label)
                            self.out.branch("Muon%s_MET_per" % branch_label, "F", lenVar="nMuons", title="MET T mu, "+title_label)                
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

        for keymu,mu in self.mudict.items() :
            for ivar_mu,var_mu in enumerate(mu["var"]):
                for key2,met in self.metdict.items() :
                    for ivar_met,var_met in enumerate(met["var"]):
                        branch_label = "%s%s_%s%s" % (mu["tag"], var_mu, met["tag"], var_met)
                        met_pt  = getattr(event,"%s_pt%s"  % (met["tag"], var_met))
                        met_phi = getattr(event,"%s_phi%s" % (met["tag"], var_met))
                        for imuon,muon in enumerate(muons) :
                            if var_mu=="":
                                mu_pt = getattr(muon, "pt"+mu["tag"])
                            else:
                                if "Up" in var_mu:
                                    mu_pt = max(getattr(muon, "pt"+mu["tag"]) + getattr(muon, "pt"+var_mu.rstrip("Up")), 0.0)
                                elif "Down" in var_mu:
                                    mu_pt = max(getattr(muon, "pt"+mu["tag"]) - getattr(muon, "pt"+var_mu.rstrip("Down")), 0.0)
                                else:
                                    print "Malformatted systematic in muon rocccor"                                
                            (mt,hpt,hphi,met_par,met_per) = evaluateMt( mu_pt, muon.phi, met_pt, met_phi)
                            Mt_vec[imuon] = mt
                            Recoil_pt_vec[imuon] = hpt
                            Recoil_phi_vec[imuon] = hphi
                            met_par_vec[imuon] = met_par
                            met_per_vec[imuon] = met_per
                        self.out.fillBranch("Muon%s_mt" % branch_label, Mt_vec)
                        self.out.fillBranch("Muon%s_recoil_pt"  % branch_label, Recoil_pt_vec)
                        self.out.fillBranch("Muon%s_recoil_phi" % branch_label, Recoil_phi_vec)
                        if mu["tag"]=="" and var_mu=="":
                            self.out.fillBranch("Muon%s_MET_par" % branch_label, met_par_vec)
                            self.out.fillBranch("Muon%s_MET_per" % branch_label, met_per_vec)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

addVarModule = lambda : additionalVariables()
