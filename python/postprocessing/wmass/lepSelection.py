import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class leptonSelection(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("genVtype", "I")
        self.out.branch("Idx_mu_bare", "I")
        self.out.branch("Idx_mu_preFSR", "I")
        self.out.branch("Idx_mu_dress", "I")
        self.out.branch("Idx_nu", "I")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        ############################################## bare and preFSR muon selection from GenPart collection
        genParticles = Collection(event, "GenPart")

        baremuons =[]
        neutrini =[]
        myIdx = -99
        myNuIdx = -99
        
        for i,g in enumerate(genParticles) :
            if not ((g.statusFlags & (1 << 0)) and g.status==1 ): continue
            if abs(g.pdgId)==13: baremuons.append((i,g))# muon is prompt
            if abs(g.pdgId) in [12, 14, 16]: neutrini.append((i,g)) # neutrino is prompt and don't explicitly ask for neutrino flavour
            
        #look at the flavour of the highest pt neutrino to decide if accept or not the event
        neutrini.sort(key = lambda x: x[1].pt, reverse=True )

        evt_flag = -1
        if   len(neutrini)>0 and abs(neutrini[0][1].pdgId)==12: evt_flag = 12 # nu_e
        elif len(neutrini)>0 and abs(neutrini[0][1].pdgId)==14: evt_flag = 14 # nu_mu
        elif len(neutrini)>0 and abs(neutrini[0][1].pdgId)==16: evt_flag = 16 # nu_tau

        # return if there are no neutrini or the highest-pt nu is not of type mu
        if len(neutrini)==0 or abs(neutrini[0][1].pdgId) != 14:            
            self.out.fillBranch("genVtype", evt_flag)
            self.out.fillBranch("Idx_mu_bare", -1)
            self.out.fillBranch("Idx_mu_preFSR", -1)      
            self.out.fillBranch("Idx_mu_dress", -1)
            self.out.fillBranch("Idx_nu", -1)
            return True
        else:
            self.out.fillBranch("genVtype", evt_flag)

        baremuons.sort(key = lambda x: x[1].pt, reverse=True ) #order by pt in decreasing order
        myIdx = baremuons[0][0]
        myNuIdx = neutrini[0][0]

        self.out.fillBranch("Idx_mu_bare",myIdx)
        self.out.fillBranch("Idx_nu", myNuIdx)
        
        muons =[]
        myIdx = -99
        
        for i,g in enumerate(genParticles) :
            if abs(g.pdgId)==13 and g.status==1 and (g.statusFlags & (1 << 8)) and (g.statusFlags & (1 << 0)): muons.append((i,g)) # muon is fromHardProcess

        if len(muons)>0:
            muons.sort(key = lambda x: x[1].pt, reverse=True ) #order by pt in decreasing order
            myIdx = muons[0][0]
            myMuon = genParticles[myIdx]
            
            if myMuon.genPartIdxMother > 0:
                while (genParticles[myMuon.genPartIdxMother].pdgId == myMuon.pdgId): # the muon has a muon as mother
                    if (genParticles[myMuon.genPartIdxMother].statusFlags & (1 << 14)): # muon is LastCopyBeforeFSR
                        myIdx = myMuon.genPartIdxMother
                        break
                    
                    myMuon = genParticles[myMuon.genPartIdxMother]
                    if myMuon.genPartIdxMother < 0:
                        break 
                    
        self.out.fillBranch("Idx_mu_preFSR",myIdx)

        ############################################## dressed muon selection from GenDressedLepton collection
        genDressedLeptons = Collection(event,"GenDressedLepton")

        myIdx = -99
        dressmuons = []
        for i,l in enumerate(genDressedLeptons) :
            if abs(l.pdgId)==13: dressmuons.append((i,l))
        
        if len(dressmuons)>0:
            dressmuons.sort(key = lambda x: x[1].pt, reverse=True ) #order by pt in decreasing order
            myIdx = dressmuons[0][0]

        self.out.fillBranch("Idx_mu_dress",myIdx)

        
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

leptonSelectModule = lambda : leptonSelection() 
 
