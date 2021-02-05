import htcondor  # for submitting jobs, querying HTCondor daemons, etc.
import classad   # for interacting with ClassAds, HTCondor's internal data format
import os
from samples import samples

schedd = htcondor.Schedd()          # get the Python representation of the scheduler
nfilesPerJob = 10

for sampleName in samples:
    for datasetNumber,dataset in enumerate(samples[sampleName]):
        files = os.popen("xrdfs eoscms.cern.ch ls %s"%dataset).read()
        files = files.split("\n")
        files = ["root://eoscms.cern.ch/%s"%f for f in files if len(f)>1 ]
        filesGroups = [files[i:i+nfilesPerJob] for i in range(0,len(files),nfilesPerJob)]
        for fileGroupNumber, fileGroup in enumerate(filesGroups):
#            print(files)
            hostname_job = htcondor.Submit({
                "executable": "skim.sh",  # the program to run on the execute node
                "arguments": "%s_%s_%s.root %s"%(sampleName,datasetNumber,fileGroupNumber,','.join(fileGroup)),       # anything the job prints to standard output will end up in this file
                "output": "Files/vbfhmumu.$(ClusterId).%s.%s.%s.out"%(sampleName,datasetNumber,fileGroupNumber),        # anything the job prints to standard error will end up in this file
                "error": "Files/vbfhmumu.$(ClusterId).%s.%s.%s.err"%(sampleName,datasetNumber,fileGroupNumber),          # this file will contain a record of what happened to the job
                "log": "Files/vbfhmumu.$(ClusterId).%s.%s.%s.log"%(sampleName,datasetNumber,fileGroupNumber),          # this file will contain a record of what happened to the job
                "transfer_input_files": "converter.py, variables.py, skim.sh",
                "+JobFlavour": "espresso",          
                "should_transfer_files": "YES",
            #    "request_cpus": "1",            # how many CPU cores we want
            #    "request_memory": "128MB",      # how much memory we want
            #    "request_disk": "128MB",        # how much disk space we want
            })
            print("I'm submitting .... %s %s %s"%(sampleName, dataset, fileGroupNumber))
            print(hostname_job)
            with schedd.transaction() as txn:   # open a transaction, represented by `txn`
                cluster_id = hostname_job.queue(txn)     # queues one job in the current transaction; returns job's ClusterId
            print("Submitted.")

print(cluster_id)

