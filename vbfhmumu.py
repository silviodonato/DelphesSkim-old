import os
prod = "PROD_1_2"
os.mkdir(prod)

import htcondor  # for submitting jobs, querying HTCondor daemons, etc.
import classad   # for interacting with ClassAds, HTCondor's internal data format
from samples import samples

schedd = htcondor.Schedd()          # get the Python representation of the scheduler

nfilesPerJob = 10

os.system("cp converter.py %s"%prod)
os.system("cp variables.py %s"%prod)
os.system("cp skim.sh %s"%prod)

for sampleName in samples:
    for datasetNumber,dataset in enumerate(samples[sampleName]):
        files = os.popen("xrdfs eoscms.cern.ch ls %s"%dataset).read()
        files = files.split("\n")
        files = ["root://eoscms.cern.ch/%s"%f for f in files if len(f)>1 ]
        filesGroups = [files[i:i+nfilesPerJob] for i in range(0,len(files),nfilesPerJob)]
        for fileGroupNumber, fileGroup in enumerate(filesGroups):
            hostname_job = htcondor.Submit({
                "executable": "skim.sh",  # the program to run on the execute node
                "arguments": "%s_%s_%s.root %s"%(sampleName,datasetNumber,fileGroupNumber,','.join(fileGroup)),       # anything the job prints to standard output will end up in this file
                "output": "%s.%s.%s.out"%(sampleName,datasetNumber,fileGroupNumber),        # anything the job prints to standard error will end up in this file
                "error": "%s.%s.%s.err"%(sampleName,datasetNumber,fileGroupNumber),          # this file will contain a record of what happened to the job
                "log": "%s.%s.%s.log"%(sampleName,datasetNumber,fileGroupNumber),          # this file will contain a record of what happened to the job
                "transfer_input_files": "converter.py, variables.py, skim.sh",
                "+JobFlavour": "espresso",          
                "should_transfer_files": "YES",
            #    "request_cpus": "1",            # how many CPU cores we want
            #    "request_memory": "128MB",      # how much memory we want
            #    "request_disk": "128MB",        # how much disk space we want
            })
            subFile = open("%s/%s.%s.%s.sub"%(prod,sampleName,datasetNumber,fileGroupNumber),'w')
            subFile.write("")
            subFile.write(str(hostname_job))
            subFile.write("queue")
            subFile.write("")
            subFile.close()

print('''
You can submit all files with

cd %s
kinit
rm -rf merge.sub
for i in $(ls | grep ".sub");do cat $i >>merge.sub; echo "" >> merge.sub;done
condor_submit merge.sub
'''%prod)

