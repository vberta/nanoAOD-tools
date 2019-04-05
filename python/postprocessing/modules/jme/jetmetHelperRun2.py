#!/usr/bin/env python
import os, sys
import subprocess

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *

# JEC for MET
jecTagsMC = {'2016' : 'Summer16_07Aug2017_V11_MC', 
             '2017' : 'Fall17_17Nov2017_V32_MC', 
             '2018' : 'Autumn18_V8_MC'}

jecTagsDATA = { '2016B' : 'Summer16_07Aug2017BCD_V11_DATA', 
                '2016C' : 'Summer16_07Aug2017BCD_V11_DATA', 
                '2016D' : 'Summer16_07Aug2017BCD_V11_DATA', 
                '2016E' : 'Summer16_07Aug2017EF_V11_DATA', 
                '2016F' : 'Summer16_07Aug2017EF_V11_DATA', 
                '2016G' : 'Summer16_07Aug2017GH_V11_DATA', 
                '2016H' : 'Summer16_07Aug2017GH_V11_DATA', 
                '2016H' : 'Summer16_07Aug2017GH_V11_DATA', 
                '2017B' : 'Fall17_17Nov2017B_V32_DATA', 
                '2017C' : 'Fall17_17Nov2017C_V32_DATA', 
                '2017D' : 'Fall17_17Nov2017DE_V32_DATA', 
                '2017E' : 'Fall17_17Nov2017DE_V32_DATA', 
                '2017F' : 'Fall17_17Nov2017F_V32_DATA', 
                '2018A' : 'Autumn18_RunA_V8_DATA',
                '2018B' : 'Autumn18_RunB_V8_DATA',
                '2018C' : 'Autumn18_RunC_V8_DATA',
                '2018D' : 'Autumn18_RunD_V8_DATA',
                } 

jerTags = {'2016' : 'Summer16_25nsV1_MC',
          '2017' : 'Fall17_V3_MC',
          '2018' : 'Fall17_V3_MC'
          }

def createJMECorrector(isMC=True, dataYear=2016, runPeriod="B", jesUncert="Total", redojec=True, saveJets=False, crab=False):
    
    jecTag = jecTagsMC[str(dataYear)] if isMC else jecTagsDATA[str(dataYear) + runPeriod]

    jmeUncert = [x for x in jesUncert.split(",")]

    #untar the zipped jec files when submitting crab jobs
    if crab :
        jesDatadir = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/jme/"
        jesInputFile = jesDatadir + jecTag + ".tar.gz"
        if os.path.isfile(jesInputFile):
            print "Using JEC files from: %s" % jesInputFile
            subprocess.call(['tar', "-xzvf", jesInputFile, "-C", jesDatadir])
        else:
            print "JEC file %s does not exist" % jesInputFile

    jmeCorrections = None
    #jme corrections
    if isMC:
        jmeCorrections = lambda : jetmetUncertaintiesProducer(era=str(dataYear), globalTag=jecTag, jesUncertainties=jmeUncert, \
                                                                  redoJEC=redojec, saveJets = saveJets, jerTag=jerTags[str(dataYear)])
    else:
        if redojec:
            jmeCorrections = lambda : jetRecalib(globalTag=jecTag, saveJets = saveJets)
    return jmeCorrections
