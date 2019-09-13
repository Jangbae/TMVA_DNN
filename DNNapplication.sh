#!/bin/bash

iFile=$1
oFile=$2
wFile=$3

source /cvmfs/cms.cern.ch/cmsset_default.sh

cd /user_data/jlee/TTTT/test/CMSSW_9_4_6_patch1/src/TTTT/TMVA/

eval `scramv1 runtime -sh`
bash
# source /cvmfs/sft.cern.ch/lcg/contrib/gcc/7.3.0/x86_64-centos7-gcc7-opt/setup.sh
source /cvmfs/sft.cern.ch/lcg/views/LCG_91/x86_64-centos7-gcc62-opt/setup.sh
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.16.00/x86_64-centos7-gcc48-opt/bin/thisroot.sh

python TMVAApplicationPyKeras.py $iFile $oFile $wFile