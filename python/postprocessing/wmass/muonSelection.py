import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class bareMuonfromWProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("GenPart_bareMuonIdx", "I");
        self.out.branch("GenDressedLepton_dressMuonIdx", "I");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        ############################################## bare muon selection from GenPart collection
        genParticles = Collection(event, "GenPart")
        
        for i,g in enumerate(genParticles) :
            myIdx = -99
            if abs(g.pdgId==13) and g.status==1 and (g.statusFlags & (1 << 0)): 
                myIdx = i
                break
                
        self.out.fillBranch("GenPart_bareMuonIdx",myIdx)

        ############################################## bare muon selection from GenDressedLepton collection
        genDressedLeptons = Collection(event,"GenDressedLepton")

        myIdx = -99
        muons = []
        for i,l in enumerate(genDressedLeptons) :
            if abs(l.pdgId==13): muons.append(l)
        
        if len(muons)>0:
            myIdx = [i[0] for i in sorted(enumerate(muons), key=lambda x:x[1].pt, reverse = True)][0]

        self.out.fillBranch("GenDressedLepton_dressMuonIdx",myIdx)

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

bareMuonfromW = lambda : bareMuonfromWProducer() 
 
