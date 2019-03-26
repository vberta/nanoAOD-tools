import ROOT
import os
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


def mk_safe(fct, *args):
    try:
        return fct(*args)
    except Exception as e:
        if any('Error in function boost::math::erf_inv' in arg for arg in e.args):
            print 'WARNING: catching exception and returning -1. Exception arguments: %s' % e.args
            return -1.
        else:
            raise e


class muonScaleResProducer(Module):
    def __init__(self, rc_dir, rc_corrections, dataYear):
        self.is_2017 = True if dataYear == 2017 else False
        p_postproc = '%s/src/PhysicsTools/NanoAODTools/python/postprocessing' % os.environ['CMSSW_BASE']
        p_roccor = p_postproc + '/data/' + rc_dir
        if "/RoccoR_cc.so" not in ROOT.gSystem.GetLibraries():
            p_helper = '%s/RoccoR.cc' % p_roccor
            print 'Loading C++ helper from ' + p_helper
            ROOT.gROOT.ProcessLine('.L ' + p_helper)
        self._roccor = ROOT.RoccoR(p_roccor + '/' + rc_corrections)

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Muon_corrected_pt", "F", lenVar="nMuon")
        #if self.is_2017:
        self.out.branch("Muon_correctedUp_pt", "F", lenVar="nMuon")
        self.out.branch("Muon_correctedDown_pt", "F", lenVar="nMuon")
        self.is_mc = bool(inputTree.GetBranch("GenJet_pt"))

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        muons = Collection(event, "Muon")
        if self.is_mc:
            genparticles = Collection(event, "GenPart")
        roccor = self._roccor
        if self.is_mc:
            u1 = random.uniform(0.0, 1.0)
            u2 = random.uniform(0.0, 1.0)
            #pt_corr = list(
            #    mu.pt * mk_safe(
            #        roccor.kScaleAndSmearMC,
            #        mu.charge, mu.pt, mu.eta, mu.phi, mu.nTrackerLayers, u1, u2
            #        ) for mu in muons)
            #if self.is_2017:
            pt_corr=[]
            pt_err=[]
            for mu in muons:
                genIdx = mu.genPartIdx
                if genIdx >= 0 and genIdx < len(genparticles):
                    genMu = genparticles[genIdx]
                    #mcSF =  mk_safe(roccor.kSpreadMC(mu.charge, mu.pt, mu.eta, mu.phi, GenPart_pt[mu.genPartIdx]))
                    pt_corr.append(mu.pt * mk_safe(roccor.kSpreadMC, mu.charge, mu.pt, mu.eta, mu.phi, genMu.pt))
                    pt_err.append(mu.pt*mk_safe(roccor.kSpreadMCerror, mu.charge, mu.pt, mu.eta, mu.phi, genMu.pt))
                else:
                    #mcSF =  mk_safe(roccor.kSmearMC(mu.charge, mu.pt, mu.eta, mu.phi, mu.nTrackerLayers, u1))
                    pt_corr.append(mu.pt*mk_safe(roccor.kSmearMC, mu.charge, mu.pt, mu.eta, mu.phi, mu.nTrackerLayers, u1))
                    pt_err.append(mu.ptErr*mk_safe(roccor.kSmearMCerror, mu.charge, mu.pt, mu.eta, mu.phi, mu.nTrackerLayers, u1))

            #pt_err = list(
            #    mu.pt * mk_safe(
            #        roccor.kScaleAndSmearMCerror,
            #        mu.charge, mu.pt, mu.eta, mu.phi, mu.nTrackerLayers, u1, u2
            #        ) for mu in muons)
        else:
            pt_corr = list(
                mu.pt * mk_safe(
                    roccor.kScaleDT,
                    mu.charge, mu.pt, mu.eta, mu.phi
                    ) for mu in muons)
            #if self.is_2017:
            pt_err = list(
                mu.pt * mk_safe(
                    roccor.kScaleDTerror,
                    mu.charge, mu.pt, mu.eta, mu.phi
                    ) for mu in muons)

        self.out.fillBranch("Muon_corrected_pt", pt_corr)
        #if self.is_2017:
        pt_corr_up = list( max(pt_corr[imu]+pt_err[imu], 0.0) for imu,mu in enumerate(muons) )
        pt_corr_down = list( max(pt_corr[imu]-pt_err[imu], 0.0) for imu,mu in enumerate(muons) )
        self.out.fillBranch("Muon_correctedUp_pt",  pt_corr_up)
        self.out.fillBranch("Muon_correctedDown_pt",  pt_corr_down)

        return True


# the Rochester guys don't supply a unified interface. The 2016 corrections come as many files in a
# directory and the 2017 correction are in a single file.

muonScaleRes2016 = lambda : muonScaleResProducer('roccor.Run2.v3', 'RoccoR2016.txt', 2016)
muonScaleRes2017 = lambda : muonScaleResProducer('roccor.Run2.v3', 'RoccoR2017.txt', 2017)
muonScaleRes2018 = lambda : muonScaleResProducer('roccor.Run2.v3', 'RoccoR2018.txt', 2018)
