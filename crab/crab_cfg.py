from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = 'NanoPostWmass'
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py','../python/postprocessing/wmass/keep_and_drop.txt'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
config.Data.inputDataset = '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/emanca-NanoWMass-b0caab6fd5c76dc4ef8a67bbbb0491fc/USER'
config.Data.inputDBS = 'phys03'
#config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 10
#config.Data.totalUnits = 10
config.Data.outLFNDirBase = '/store/user/%s/NanoPostWmass' % (getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'NanoPostWmass'
config.section_("Site")
config.Site.storageSite = "T2_IT_Pisa"

