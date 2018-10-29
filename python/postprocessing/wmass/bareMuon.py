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
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        genParticles = Collection(event, "GenPart")

        for i,g in enumerate(genParticles) :
            myIdx = -99
            if abs(g.pdgId==13) and g.status==1 and (g.statusFlags & (1 << 0)): 
                myIdx = i
                break
              
        
        self.out.fillBranch("GenPart_bareMuonIdx",myIdx)
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

bareMuonfromW = lambda : bareMuonfromWProducer() 
 
