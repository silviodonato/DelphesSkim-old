#!/bin/bash

source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc8-opt/setup.sh

PATH=$PATH:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/llvm/8.0.1/bin/
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/llvm/8.0.1/lib64/:.


python /afs/cern.ch/user/m/mthakore/public/DelphesSkim/converter.py DYToLL_madgraphMLM 0
python /afs/cern.ch/user/m/mthakore/public/DelphesSkim/converter.py DYToLL_madgraphMLM 1
python /afs/cern.ch/user/m/mthakore/public/DelphesSkim/converter.py DYToLL_madgraphMLM 2
python /afs/cern.ch/user/m/mthakore/public/DelphesSkim/converter.py DYToLL_madgraphMLM 3
python /afs/cern.ch/user/m/mthakore/public/DelphesSkim/converter.py DYToLL_madgraphMLM 4
python /afs/cern.ch/user/m/mthakore/public/DelphesSkim/converter.py DYToLL_madgraphMLM 5
python /afs/cern.ch/user/m/mthakore/public/DelphesSkim/converter.py DYToLL_madgraphMLM 6
python /afs/cern.ch/user/m/mthakore/public/DelphesSkim/converter.py DYToLL_madgraphMLM 7
python /afs/cern.ch/user/m/mthakore/public/DelphesSkim/converter.py DYToLL_madgraphMLM 8
python /afs/cern.ch/user/m/mthakore/public/DelphesSkim/converter.py DYToLL_madgraphMLM 9
