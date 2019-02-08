from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
import sys

config = Configuration()

config.section_("General")
config.General.requestName = 'TEST'
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py','../python/postprocessing/wmass/keep_and_drop_MC.txt', '../python/postprocessing/wmass/keep_and_drop_Data.txt']
config.JobType.scriptArgs = ['isMC=1','passall=0']
config.JobType.sendPythonFolder	 = True
config.section_("Data")
config.Data.inputDataset = '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/NANOAODSIM'
config.Data.inputDBS = 'global'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 50
#config.Data.totalUnits = 10
config.Data.outLFNDirBase = '/store/user/%s/NanoAODv3-TEST' % (getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'TEST'
config.section_("Site")
config.Site.storageSite = "T2_IT_Pisa"

if __name__ == '__main__':

    import os

    f = open(sys.argv[1]) 
    content = f.readlines()
    content = [x.strip() for x in content] 
    from CRABAPI.RawCommand import crabCommand

    n = 0
    for dataset in content :        
        config.Data.inputDataset = dataset
        config.General.requestName = dataset.split('/')[1]+'_sub'+str(n)+'_v1'
        config.Data.outputDatasetTag = dataset.split('/')[2]
        print config.General.requestName, '==>', config.Data.outLFNDirBase+'/'+dataset.split('/')[1]+'/'+config.Data.outputDatasetTag
        crabCommand('submit', '--dryrun', config = config)
        n += 1
