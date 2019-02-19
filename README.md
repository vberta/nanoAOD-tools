# nanoAOD-tools
Tools for working with NanoAOD (requiring only python + root, not CMSSW)

## Checkout instructions

You need to setup python 2.7 and a recent ROOT version first.

    cmsrel CMSSW_10_2_9
    cd CMSSW_10_2_9/src/
    cmsenv	   
    voms-proxy-init --voms cms
    source /cvmfs/cms.cern.ch/crab3/crab.sh
    git clone https://github.com/emanca/nanoAOD-tools.git PhysicsTools/NanoAODTools
    cd PhysicsTools/NanoAODTools
    git checkout origin/wmass
    scram b -j 8

## Run local tests

The basic syntax of the command is the following:

    cd python/wmass/
    python postproc.py --isMC 1 --passall 0 --dataYear 2016 --runPeriod B --jesUncert Total --redojec 1 --maxEvents 1000

Here is a summary of its features:
* the `--isMC` option is `1` when running on MC and `0` otherwise.
* the `--passall` option set to `1` makes the postprocessor run on every event. It is `0` by default.
* the `--dataYear` option refers to the run era. Currently accepted values are `2016` and `2017`.

## Run on crab