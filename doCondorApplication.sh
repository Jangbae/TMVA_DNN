#!/bin/sh

inDir=${1}
outDir=${2}
fileName=${3}
BDT=${4}
CONDORDIR=${5}

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /user_data/jlee/TTTT/CMSSW_9_4_6_patch1/src/TMVA
export SCRAM_ARCH=slc7_amd64_gcc630
eval `scramv1 runtime -sh`

source /cvmfs/sft.cern.ch/lcg/contrib/gcc/7.3.0/x86_64-centos7-gcc7-opt/setup.sh
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.16.00/x86_64-centos7-gcc48-opt/bin/thisroot.sh

root -l -b -q $CONDORDIR/TMVAClassificationApplication.C\(\"$BDT\",\"$inDir/$fileName\",\"$fileName\"\)

cp $fileName $outDir/
rm $fileName 
