import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

def find_last_beforeFSR(genParticles, idx):
    result = idx
    myMuon = genParticles[result]
    if myMuon.genPartIdxMother > 0:
        while (genParticles[myMuon.genPartIdxMother].pdgId == myMuon.pdgId): # the muon has a muon as mother                                                                                               
            if (genParticles[myMuon.genPartIdxMother].statusFlags & (1 << 14)): # muon is LastCopyBeforeFSR                                                                                                 
                result = myMuon.genPartIdxMother
                break
            myMuon = genParticles[myMuon.genPartIdxMother]
            if myMuon.genPartIdxMother < 0:
                break
    return result

class genLeptonSelection(Module):
    def __init__(self, Wtypes=['bare', 'preFSR', 'dress']):
        self.Wtypes = Wtypes
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("genVtype", "I")
        for t in self.Wtypes:
            self.out.branch("Idx_"+t+"_mu1", "I")
            self.out.branch("Idx_"+t+"_mu2", "I")
        self.out.branch("Idx_nu", "I")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        ############################################## bare and preFSR muon selection from GenPart collection
        genParticles = Collection(event, "GenPart")

        neutrini = []
        bare_muons = []        
        preFSR_muons = []
        for i,g in enumerate(genParticles) :
            if not ((g.statusFlags & (1 << 0)) and g.status==1 ): continue
            if abs(g.pdgId)==13: 
                bare_muons.append((i,g)) # muon is prompt
                if (g.statusFlags & (1 << 8)): preFSR_muons.append((i,g))
            if abs(g.pdgId) in [12, 14, 16]: neutrini.append((i,g)) # neutrino is prompt and don't explicitly ask for neutrino flavour
        
        # compute all of them
        results = {}
        for t in ['bare', 'preFSR', 'dress']:
            results[t+'_mu1'] = -1
            results[t+'_mu2'] = -1
        results['nu'] = -1

        # decide the event type
        evt_flag = -1

        # W->mn <=> highest-pt netrino is of type mu
        if len(neutrini)>0:
            neutrini.sort(key = lambda x: x[1].pt, reverse=True )
            if abs(neutrini[0][1].pdgId)==12: evt_flag = 12 # nu_e
            elif abs(neutrini[0][1].pdgId)==14: evt_flag = 14 # nu_mu
            elif abs(neutrini[0][1].pdgId)==16: evt_flag = 16 # nu_tau        
            idx_nu = neutrini[0][0]
            results['nu'] = idx_nu
            if len(bare_muons)<1:
                #print "Warning! The event has a neutrino of type mu, but not a bare muon"
                pass
            else:
                bare_muons.sort(key = lambda x: x[1].pt, reverse=True )                
                idx_mu1 = bare_muons[0][0]
                results['bare_mu1'] = idx_mu1

        # Z->mm <=> two highest-pT bare muons of opposite-sign
        elif len(bare_muons)>1:
            bare_muons_p = [x for x in bare_muons if x[1].pdgId==-13]
            bare_muons_m = [x for x in bare_muons if x[1].pdgId==+13]
            if len(bare_muons_p)>0 and len(bare_muons_m)>0:
                bare_muons_p.sort(key = lambda x: x[1].pt, reverse=True )
                bare_muons_m.sort(key = lambda x: x[1].pt, reverse=True )
                (idx_mu1,idx_mu2) = (bare_muons_p[0][0], bare_muons_m[0][0])
                results['bare_mu1'] = idx_mu1
                results['bare_mu2'] = idx_mu2
                evt_flag = 13
        else:
             evt_flag = -1
            
        # return if not a W->mn or Z->mm event
        if evt_flag not in [13,14]:
            self.out.fillBranch("genVtype", evt_flag)
            for t in self.Wtypes:
                self.out.fillBranch("Idx_"+t+"_mu1", -1)
                self.out.fillBranch("Idx_"+t+"_mu2", -1)
            self.out.fillBranch("Idx_nu", -1)
            return True
        
        # W->mn
        if evt_flag==14:
            if len(preFSR_muons)<1:
                #print "Warning! The event has a neutrino of type mu, but not a muon from hard-process"
                pass
            else:
                idx_mu1 = find_last_beforeFSR(genParticles, preFSR_muons[0][0])
                results['preFSR_mu1'] = idx_mu1
        # Z->mm
        else: 
            if len(preFSR_muons)<2:
                #print "Warning! The event has two bare muons but less than two muons from hard-process"
                pass
            else:
                preFSR_muons_p = [x for x in preFSR_muons if x[1].pdgId==-13]
                preFSR_muons_m = [x for x in preFSR_muons if x[1].pdgId==+13]
                if len(preFSR_muons_p)>0 and len(preFSR_muons_m)>0:
                    preFSR_muons_p.sort(key = lambda x: x[1].pt, reverse=True )
                    preFSR_muons_m.sort(key = lambda x: x[1].pt, reverse=True )
                    idx_mu1 = find_last_beforeFSR(genParticles, preFSR_muons_p[0][0])
                    idx_mu2 = find_last_beforeFSR(genParticles, preFSR_muons_m[0][0])
                    results['preFSR_mu1'] = idx_mu1
                    results['preFSR_mu2'] = idx_mu2            
                    
        ############################################## dressed muon selection from GenDressedLepton collection
        genDressedLeptons = Collection(event,"GenDressedLepton")

        dress_muons = []
        for i,l in enumerate(genDressedLeptons) :
            if abs(l.pdgId)==13: dress_muons.append((i,l))
        
        if evt_flag==14:
            if len(dress_muons)<1:
                #print "Warning! The event has a neutrino of type mu, but not a dressed muon"
                pass
            else:
                dress_muons.sort(key = lambda x: x[1].pt, reverse=True ) #order by pt in decreasing order
                idx_mu1 = dress_muons[0][0]
                results['dress_mu1'] = idx_mu1
        else:
            if len(dress_muons)<2:
                #print "Warning! The event has two bare muons but less than two dressed muons from hard-process"
                pass
            else:
                dress_muons_p = [x for x in dress_muons if x[1].pdgId==-13]
                dress_muons_m = [x for x in dress_muons if x[1].pdgId==+13]
                if len(dress_muons_p)>0 and len(dress_muons_m)>0:
                    dress_muons_p.sort(key = lambda x: x[1].pt, reverse=True )
                    dress_muons_m.sort(key = lambda x: x[1].pt, reverse=True )
                    (idx_mu1,idx_mu2) = (dress_muons_p[0][0], dress_muons_m[0][0])
                    results['dress_mu1'] = idx_mu1
                    results['dress_mu2'] = idx_mu2

        # Fill
        self.out.fillBranch("genVtype", evt_flag)
        for t in self.Wtypes:                    
            self.out.fillBranch("Idx_"+t+"_mu1", results[t+'_mu1'])
            self.out.fillBranch("Idx_"+t+"_mu2", results[t+'_mu2'])
        self.out.fillBranch("Idx_nu", results['nu'])

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

genLeptonSelectModule = lambda : genLeptonSelection() 
 
