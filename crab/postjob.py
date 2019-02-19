#!/usr/bin/env python
import commands
import time
import re
import os
import string
from os import listdir
from os.path import isfile, join
import sys
import argparse

from CRABClient.UserUtilities import config, getUsernameFromSiteDB

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser("")
parser.add_argument('-tag', '--tag', type=str, default="TEST",      help="")
parser.add_argument('-isMC', '--isMC', type=int, default=1,      help="")
parser.add_argument('-dataYear', '--dataYear',type=int, default=2016, help="")
parser.add_argument('-run', '--run',type=str, default='batch', help="")
parser.add_argument('-pushback', '--pushback',type=int, default=0, help="")
args = parser.parse_args()
tag = args.tag
isMC = args.isMC
dataYear = args.dataYear
run = args.run
pushback = args.pushback
samples = ('mc' if isMC else 'data')+'samples_'+str(dataYear)+'.txt'
print "tag =", bcolors.OKGREEN, tag, bcolors.ENDC, \
    ", isMC =", bcolors.OKGREEN, str(isMC), bcolors.ENDC, \
    ", dataYear =", bcolors.OKGREEN, str(dataYear), bcolors.ENDC, \
    ", pushback =", bcolors.OKGREEN, str(pushback), bcolors.ENDC, \
    " => running on sample file:", bcolors.OKGREEN, samples, bcolors.ENDC

################################################################################

import subprocess

select_first_trial = True
n_max_files = 2

username = getUsernameFromSiteDB()
path = '/home/users/%s/wmass/CMSSW_10_2_9/src/PhysicsTools/NanoAODTools/crab/' % username
fin = open('postcrab_'+samples.rstrip('.txt')+'_'+tag+'.txt', 'r')
content = fin.readlines()
sample_dirs = [x.strip() for x in content]
for sample_dir in sample_dirs:    
    task_name = sample_dir.split('/')[-2]
    sample_name = sample_dir.split('/')[-4]
    script_name = 'haddnano_'+task_name
    fout = open(script_name+'.sh','w')
    fout.write('#!/bin/bash\n\n')
    fout.write('cd '+path+'\n')
    fout.write('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
    fout.write('eval `scramv1 runtime -sh`\n')
    fout.write('\n')    
    pos = sample_dir.find("cms")
    sample_dir_from_cms = sample_dir[pos-1:] 
    outdir_master = ("/gpfs/ddn/cms/user/%s/" % username)+"/NanoAOD-"+tag+"/"
    if not os.path.isdir(outdir_master):
        mkoutdirmastercmd = "mkdir "+outdir_master
        print bcolors.OKBLUE, mkoutdirmastercmd, bcolors.ENDC
        fout.write(mkoutdirmastercmd+'\n')
        if run=='shell': os.system(mkoutdirmastercmd)
    outdir = ""
    if pushback:
        outdir = outdir_master+"/"+task_name+"/"
    else:
        outdir = outdir_master+"/"+sample_name+"/"
    if not os.path.isdir(outdir):
        mkoutdircmd = "mkdir "+outdir
        print bcolors.OKBLUE, mkoutdircmd, bcolors.ENDC
        fout.write(mkoutdircmd+'\n')
        if run=='shell': os.system(mkoutdircmd)                
    crab_trials = os.listdir(sample_dir)
    for crab_trial in crab_trials:
        if select_first_trial and crab_trial!="0000":
            continue
        files = [sample_dir+"/"+crab_trial+"/"+x for x in os.listdir(sample_dir+'/'+crab_trial) if "tree_" in x]
    print "Found", bcolors.OKGREEN, "%s" % len(files), bcolors.ENDC, "files"
    haddargs = outdir+"tree.root "
    for nf,f in enumerate(files):
        if nf<n_max_files:
            haddargs += f+" "
    haddcmd = "python ../scripts/haddnano.py "+haddargs
    print bcolors.OKBLUE, haddcmd, bcolors.ENDC
    if run=='shell': os.system(haddcmd)
    fout.write(haddcmd+'\n')
    if (os.path.isfile(outdir+"tree.root") or run=='batch') and pushback:
        print "File:", bcolors.OKGREEN, outdir+"tree.root", bcolors.ENDC, "found. Move back to SRM"
        pushbackcmd = 'lcg-cp -b -U srmv2 -v file://'+outdir+'tree.root'+' \"srm://stormfe1.pi.infn.it:8444/srm/managerv2?SFN='+sample_dir_from_cms+'/tree.root'+'\"'
        print bcolors.OKBLUE, pushbackcmd, bcolors.ENDC
        fout.write('voms-proxy-init --voms cms\n')
        fout.write(pushbackcmd+'\n')
        if run=='shell': 
            os.system('voms-proxy-init --voms cms')
            os.system(pushbackcmd)
    elif not pushback:
        print "Done!"
    else:
        print "Could not find file "+outdir+"tree.root"
    if (os.path.isfile(sample_dir+"/tree.root") or run=='batch') and pushback:
        print "File:", bcolors.OKGREEN, sample_dir+"/tree.root", bcolors.ENDC, "is in SRM. Remove tmp files" 
        rmcmd = "rm -r "+outdir
        print bcolors.OKBLUE, rmcmd, bcolors.ENDC
        fout.write(rmcmd+'\n')
        if run=='shell': os.system(rmcmd)
    elif not pushback:
        pass
    else:
        print "Could not find file "+sample_dir+"/tree.root"
    fout.close()
    os.system('chmod +x '+script_name+'.sh')
    if run=='batch': 
        submit_to_queue = 'bsub -q local -n 8 -J '+script_name+' -o '+path+'/'+script_name+'.stdout'+' -e '+path+'/'+script_name+'.stderr'+' -cwd `pwd` '+'./'+script_name+'.sh'
        print bcolors.OKBLUE, submit_to_queue, bcolors.ENDC
        os.system(submit_to_queue)
        time.sleep( 1.0 )
        print "@@@@@ END JOB @@@@@"        
