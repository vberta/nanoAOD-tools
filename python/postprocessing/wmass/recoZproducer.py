import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.wmass.CSVariables import getCSangles

class recoZproducer(Module):
    def __init__(self, dataYear=2016):
        self.mudict = {
            "pf"     : { "tag" : "",             "var"  : [""] },
            "roccor" : { "tag" : "_corrected",   "var"  : [""] },
            }
        if dataYear==2017:
            self.mudict["roccor"]["var"] = ["", "_sys_uncertUp",  "_sys_uncertDown"]
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for key_mu,mu in self.mudict.items() :
            for ivar_mu,var_mu in enumerate(mu["var"]):
                branch_label = "%s%s" % (mu["tag"], var_mu)
                self.out.branch("recoZ%s_pt" % branch_label, "F")
                self.out.branch("recoZ%s_phi" % branch_label, "F")
                self.out.branch("recoZ%s_y" % branch_label, "F")
                self.out.branch("recoZ%s_mass" % branch_label, "F")
                self.out.branch("recoZ%s_CStheta" % branch_label, "F")
                self.out.branch("recoZ%s_CSphi" % branch_label, "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        muons = Collection(event, "Muon")
        for keymu,mu in self.mudict.items() :
            for ivar_mu,var_mu in enumerate(mu["var"]):
                branch_label = "%s%s" % (mu["tag"], var_mu)
                
                # fill with real values only if there are two muons
                if event.Vtype in [2,3]:                    
                    # chose plus and negative muon
                    (idxP, idxM) = (event.Muon_idx1,event.Muon_idx2)
                    if muons[event.Muon_idx1].charge<0: (idxP, idxM) = (event.Muon_idx2,event.Muon_idx1) 

                    if var_mu=="":
                        (muP_pt, muN_pt) = (getattr(muons[idxP], "pt"+mu["tag"]), getattr(muons[idxM], "pt"+mu["tag"]))
                    else:
                        if "Up" in var_mu:
                            (muP_pt, muN_pt) = (max(getattr(muons[idxP], "pt"+mu["tag"]) + getattr(muons[idxP], "pt"+var_mu.rstrip("Up")), 0.0), 
                                                max(getattr(muons[idxM], "pt"+mu["tag"]) + getattr(muons[idxM], "pt"+var_mu.rstrip("Up")), 0.0))
                        elif "Down" in var_mu:
                            (muP_pt, muN_pt) = (max(getattr(muons[idxP], "pt"+mu["tag"]) - getattr(muons[idxP], "pt"+var_mu.rstrip("Down")), 0.0), 
                                                max(getattr(muons[idxM], "pt"+mu["tag"]) - getattr(muons[idxM], "pt"+var_mu.rstrip("Down")), 0.0))
                        else:
                            print "Malformatted systematic in muon rocccor"
                    muP = ROOT.TLorentzVector()
                    muN = ROOT.TLorentzVector()
                    muP.SetPtEtaPhiM(muP_pt, muons[idxP].eta, muons[idxP].phi, muons[idxP].mass)
                    muN.SetPtEtaPhiM(muN_pt, muons[idxM].eta, muons[idxM].phi, muons[idxM].mass)
                    Z = muP+muN
                    (Z_pt, Z_phi, Z_y, Z_mass) = (Z.Pt(), Z.Phi(), Z.Rapidity(), Z.M())
                    CStheta, CSphi = getCSangles(muP,muN)
                else:
                    (Z_pt, Z_phi, Z_y, Z_mass, CStheta, CSphi) = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
                    
                self.out.fillBranch("recoZ%s_pt"  % branch_label, Z_pt)
                self.out.fillBranch("recoZ%s_phi"  % branch_label, Z_phi)
                self.out.fillBranch("recoZ%s_y"  % branch_label, Z_y)
                self.out.fillBranch("recoZ%s_mass"  % branch_label, Z_mass)
                self.out.fillBranch("recoZ%s_CStheta"  % branch_label, CStheta)
                self.out.fillBranch("recoZ%s_CSphi"  % branch_label, CSphi)

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

recoZproducerModule = lambda : recoZproducer()
