#!/bin/bash

source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc8-opt/setup.sh

PATH=$PATH:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/llvm/8.0.1/bin/
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/llvm/8.0.1/lib64/:.

echo "Check kinit:", klist
klist

echo "klist -f"
klist -f

echo "token"
token

echo "Check xrootd", root -b -l -q  root://eoscms.cern.ch//store/group/upgrade/delphes_output/YR_Delphes/Delphes342pre14/VBFHToMuMu_M125_14TeV_powheg_pythia8_200PU/VBFHToMuMu_M125_14TeV_powheg_pythia8_1.root -e 'Delphes->Draw("","")'
root -b -l -q  root://eoscms.cern.ch//store/group/upgrade/delphes_output/YR_Delphes/Delphes342pre14/VBFHToMuMu_M125_14TeV_powheg_pythia8_200PU/VBFHToMuMu_M125_14TeV_powheg_pythia8_1.root -e 'Delphes->Draw("","")'

echo python3.8 converter.py $1 $2 
python3.8 converter.py $1 $2
