#!/usr/bin/env python
# encoding: utf-8
'''
@author:     cjustin
@contact:    cjustin@bcgsc.ca
'''

from optparse import OptionParser

class ReadLengths:
    
    def __init__(self):
        """Constructor"""
        pass
    
    def load(self, fastaIndex):
        self._lengths = {}
        fh = open(fastaIndex)
        for line in fh:
            tempArray = line.split("\t")
            readID = tempArray[0]
            length = tempArray[1]
            self._lengths[readID] = int(length)

    
if __name__ == '__main__':
    
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", metavar="INPUT",
                      help="input file")
                
    (options, args) = parser.parse_args()
    
    rl = ReadLengths()
    rl.load(options.input)
