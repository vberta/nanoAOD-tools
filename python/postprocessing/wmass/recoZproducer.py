import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.wmass.CSVariables import getCSangles

def format_name(tag_mu="", syst_mu="", tag_met="", syst_met="", ispostfix=True):
    out = "%s%s%s%s" % (("_"+tag_mu) if tag_mu!="" else "",
                        ("_"+syst_mu) if syst_mu!="" else "",
                        ("_"+tag_met)  if tag_met!="" else "",
                        ("_"+syst_met) if syst_met!="" else "")
    if not ispostfix: 
        out = out.lstrip('_')
    return out

class recoZproducer(Module):
    def __init__(self, isMC=True, mudict={}):
        self.mudict = mudict
        self.isMC = isMC
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for key_mu,mu in self.mudict.items() :
            for ivar_mu,var_mu in enumerate(mu["systs"]):
                branch_label = ("GenFromRecoZ" if key_mu=="GEN" else "RecoZ")
                branch_label += format_name(mu["tag"], var_mu, "", "", True)
                self.out.branch("%s_pt" % branch_label, "F")
                self.out.branch("%s_phi" % branch_label, "F")
                self.out.branch("%s_y" % branch_label, "F")
                self.out.branch("%s_mass" % branch_label, "F")
                self.out.branch("%s_CStheta" % branch_label, "F")
                self.out.branch("%s_CSphi" % branch_label, "F")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        muons = Collection(event, "Muon")
        if self.isMC:
            genparticles = Collection(event, "GenPart")
        for key_mu,mu in self.mudict.items() :
            for ivar_mu,var_mu in enumerate(mu["systs"]):
                # fill with real values only if there are two muons
                if event.Vtype in [2,3]:                    
                    # chose plus and negative muon                    
                    muP = ROOT.TLorentzVector()
                    muN = ROOT.TLorentzVector()
                    (idxP, idxN) = (event.Idx_mu1,event.Idx_mu2)
                    if muons[event.Idx_mu1].charge<0: (idxP, idxN) = (event.Idx_mu2,event.Idx_mu1)                     
                    # reco Z, based on Muons objects
                    if key_mu!="GEN":
                        (muP_pt, muN_pt) = ( getattr(muons[idxP], format_name("",var_mu,"","pt", False)), 
                                             getattr(muons[idxN], format_name("",var_mu, "","pt",False)) )
                        muP.SetPtEtaPhiM(muP_pt, muons[idxP].eta, muons[idxP].phi, muons[idxP].mass)
                        muN.SetPtEtaPhiM(muN_pt, muons[idxN].eta, muons[idxN].phi, muons[idxN].mass)
                    # gen Z, based on gen muons
                    else:
                        genIdxP, genIdxN = muons[idxP].genPartIdx, muons[idxN].genPartIdx
                        if genIdxP>=0 and genIdxP<len(genparticles) and genIdxN>=0 and genIdxN<len(genparticles):
                            genMuP,genMuN = genparticles[genIdxP],genparticles[genIdxN]
                            muP.SetPtEtaPhiM(genMuP.pt, genMuP.eta, genMuP.phi, genMuP.mass)
                            muN.SetPtEtaPhiM(genMuN.pt, genMuN.eta, genMuN.phi, genMuN.mass)
                    Z = muP+muN
                    (Z_pt, Z_phi, Z_y, Z_mass) = (Z.Pt(), Z.Phi(), Z.Rapidity(), Z.M())
                    CStheta, CSphi = getCSangles(muP,muN)
                    branch_label = ("GenFromRecoZ" if key_mu=="GEN" else "RecoZ")
                    branch_label += format_name(mu["tag"], var_mu, "", "", ispostfix=True)
                    self.out.fillBranch("%s_pt"  % branch_label, Z_pt)
                    self.out.fillBranch("%s_phi"  % branch_label, Z_phi)
                    self.out.fillBranch("%s_y"  % branch_label, Z_y)
                    self.out.fillBranch("%s_mass"  % branch_label, Z_mass)
                    self.out.fillBranch("%s_CStheta"  % branch_label, CStheta)
                    self.out.fillBranch("%s_CSphi"  % branch_label, CSphi)

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

recoZproducerModule = lambda : recoZproducer()
