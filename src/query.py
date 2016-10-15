#!/usr/bin/env python
# encoding: utf-8
'''
Downloader -- A simple python script for downloading a multifasta file give a NCBI genbank id (GI)

This code serves as an example.

@author:     cjustin
@contact:    cjustin@bcgsc.ca
'''

class Downloader:
    
    def __init__(self):
        """Constructor"""
        pass
    
    def run(self, inputSRAs, reads):
        """Run multiple SRA ids from a list, splitting into different processes"""
        pass
    
    def runSingle(self, inputSRA):
        """Run a single sra ids"""
        pass

    def parseLine(self, line):
        """parse blast output into format needed for classifier"""
        pass
    
    def compileResults(self, outputList):
        """compile counts and results from multiple file"""
        pass
    
if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", metavar="INPUT",
                      help="input file of list of SRA files")
    parser.add_option("-r", "--reads", dest="reads", metavar="READS", 
                      help="reads file")
                
    (options, args) = parser.parse_args()
        
    if options.input and options.reads:
        runner = Query()
        runner.run(options.input, options.reads)        
    else:
        print 'ERROR: Missing Required Options. Use -h for help'
