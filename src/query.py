#!/usr/bin/env python
# encoding: utf-8
'''
Script for running a long read set against BLASTing against multiple SRA ids, 
parsing the data and collecting in format compatible with our classifier

@author:     cjustin
@contact:    cjustin@bcgsc.ca
@editor:     dcgenomics
'''

from optparse import OptionParser
import subprocess
import sys
import os
from joblib import Parallel, delayed

def _runSingle(inputSRA):
     """Run a single sra ids"""
     cmd = "magicblast -paired -splice F -db " + self._reads + " -sra " + inputSRA + " > " + output
#      cmd = "sleep 10 > " + inputSRA + ".bam"
     cmd += " 2> " + inputSRA + ".bam.log ; rm ~/ncbi/public/sra/" + inputSRA + ".sra.cache"
     print(cmd)
     os.system(cmd)
 

class Query:
    
    def __init__(self, reads):
        """Constructor"""
        self._reads = reads
    
    def run(self, inputSRAs, threads):
        """Run multiple SRA ids from a list, splitting into different processes"""       
        filenames = []
        #parse input
        sraFH = open(inputSRAs);
        for files in sraFH:
            file = files.strip()
            filenames.append(file)
        
        Parallel(n_jobs = threads) (delayed(_runSingle)(file) for file in filenames)
    
if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", metavar="INPUT",
                      help="input file of list of SRA IDs")
    parser.add_option("-r", "--reads", dest="reads", metavar="READS", 
                      help="blast DB")
    parser.add_option("-t", "--threads", dest="threads", metavar="THREADS", 
                      help="number of thread to use at a time", default = 1)
                
    (options, args) = parser.parse_args()
           
    if options.input and options.reads:
        runner = Query(options.reads)
        runner.run(options.input, int(options.threads))        
    else:
        print 'ERROR: Missing Required Options. Use -h for help'
