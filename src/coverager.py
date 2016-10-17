import sys
import argparse
from scipy.stats import chisquare
from pysam import AlignmentFile
import numpy

# Default global variables
g_alpha = 0.05
g_cov = 100
k_pval = "PVAL"
k_cov = "COV"

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

	def getLengths(self):
		return self._lengths 

def getAlignedLength(cigarTups):
	'''
	Returns the length of aligned bases in the reference sequence given a list of CIGAR tuples
	Inputs
	- (list of ( (str) operation, (int) length)) cigarTups: the cigar tuples returned by pysam 
	Outputs
	- (int) length: length of aligned bases in the reference sequence 
	'''
	length = 0
	for tup in cigarTups:
		operation = tup[0]
		if operation in ["M", "D", "=", "X"]:
			opLength = int(tup[1])
			length += opLength
	return length

def test_getAlignedLength():
	cigarTups = [ ('M', 5), ('D', 2), ('=', 10), ('X', 4), ('I', 25) ]
	assert( getAlignedLength(cigarTups) == 21 )
	print "test_getAlignedLength passed!"

def updateDistribution(dists, lengths, refName, start, cigarTups):
	'''
	Update the coverage distribution for the given long read
	Inputs
	- ( dict[str] = (numpy.array of ints) ) dists: contains the coverage distributions for each long read
	- (str) refName: name of long read
	- (int) start: position in long read that alignment starts at
	- (list of ( (str) operation, (int) length)) cigarTups: the cigar tuples returned by pysam 
	'''
	if not refName in dists:
		length = lengths[refName]
		dists[refName] = numpy.zeros(length) 
	length = getAlignedLength(cigarTups)
	for i in range(start, start+length):
		dists[refName][i] += 1

def test_updateDistribution():
	refName = "example"
	dists = { refName : [0,0,0,0,0,0,0] }

	start = 1 
	cigarTups = [('M',5)]
	updateDistribution(dists,refName,start,cigarTups)
	assert( dists == { refName : [0,1,1,1,1,1,0] } )

	start = 2
	cigarTups = [('M',2)]
	updateDistribution(dists,refName,start,cigarTups)
	assert( dists == { refName : [0,1,2,2,1,1,0] } )

	print "test_updateDistribution passed!"
		

def constructDistributions(bamName, lengths):
	'''
	Given a BAM file, constructs a coverage distribution for each long read
	Inputs
	- (str) bamName: BAM file name
	- (dict[(str) refName] = (int) read length) lengths: 
          returns the length of the long read given its read name
	Outputs
	- ( dict[(str) refName] = (numpy.array of ints) distribution ) dists: contains the coverage distributions 
          for each long read
	'''
	samfile = AlignmentFile(bamName, 'rb')
	iter = samfile.fetch()
	dists = {}
	for alignment in iter: 
		refName = alignment.reference_name
		start = alignment.reference_start
		cigarTups = alignment.cigartuples
		updateDistribution(dists, lengths, refName, start, cigarTups)
	return dists

def getPValues(dists):
	'''
	Finds the p-value of how closely the empirical distributions of the coverage distributions match a
	uniform distributions.
	Inputs
	- (dict[(str) refName] = (numpy.array of ints) coverage distribution) dists: contains the coverage 
          distributions for each long read
	Outputs
	- (dict[(str) refName] = (int) p-value) pValues: contains the p-value of being a uniform distribution
          for each long read
	'''
	pValues = {}
	for refName in dists:
		distribution = dists[refName]
		chisq, p = chisquare(distribution)
		pValues[refName] = p
	return pValues	

def test_getPValues():
	refName = "example"

	dists = { refName : [ 5 for i in range(100) ] }
	pValues = getPValues(dists)
	assert( pValues[refName] == 1.0 )

	dists = { refName : [ i for i in range(100) ] }
	pValues = getPValues(dists)
	assert( pValues[refName] < 1.0 )

	print "test_getPValues passed!"

def getCovs(dists):
	'''
	Finds the average coverage of each long read.
	Inputs
	- (dict[(str) refName] = (numpy.array of ints) coverage distribution) covs: contains the coverage 
          distributions for each long read
	Outputs
	- (dict[(str) refName] = (int) p-value) covs: contains the coverage for the given long read
          for each long read
	'''
	covs = {}
	for refName in dists:
		distribution = dists[refName]
		average = numpy.mean(distribution)
		covs[refName] = average
	return covs	

def test_getCovs():
	refName = "example"
	dists = { refName : [ 10 for i in range(100) ] }
	covs = getCovs(dists)
	assert( covs == { refName : 10.0 } )
	print "test_getCovs passed!"

def combineCovsAndPValues(pVals,covs):
	'''
	Combines the pVals and covs into one dict
	Inputs
	- (dict[(str) refName] = (numpy.array of ints) coverage distribution) covs: contains the coverage 
          distributions for each long read
	- (dict[(str) refName] = (numpy.array of ints) coverage distribution) dists: contains the coverage 
          distributions for each long read
	Outputs
	- (dict[(str) refName] = { (str) k_pval : (float) int, (str) k_cov : (float) cov }) reads:
          contains coverages and p-value for each read 
	'''
	reads = {}
	for refName in pVals:
		reads[refName] = { k_pval : pVals[refName], k_cov : covs[refName] }	
	return reads

def test_combineCovsAndPValues():
	refName = "example"
	pVals = { refName : 1.0 }
	covs = { refName : 10 }
	reads = combineCovsAndPValues(pVals,covs)
	assert( reads == { refName : { k_cov : 10, k_pval : 1.0 } } )
	print "test_combineCovsAndPValues passed!"

def prunePValues(reads):
	'''
	Throws out all long reads in pValues with p-value less than 1.0 - g_alpha
	Inputs
	- (dict[(str) refName] = {(str) k_pval : (int) p-value, (str) k_cov : (int) cov}) reads 
          reads, their p-value and coverage
	'''
	for refName in reads:
		pVal = reads[refName][k_pval]
		if pVal < (1.0-g_alpha):
			del reads[refName] 

def pruneCovs(reads):
	'''
	Throws out all long reads in pValues with coverage less than g_cov
	Inputs
	- (dict[(str) refName] = {(str) k_pval : (int) p-value, (str) k_cov : (int) cov}) reads: 
	  reads, their p-value and coverage
	'''
	for refName in reads:
		cov = reads[refName][k_cov]
		if cov < g_cov:
			del reads[refName] 

def writePreservedReads(outputPath, reads):
	'''
	Write the name of the preserved long reads into the file.
	Inputs
	- (str) outputPath: path to the output file
	- (dict[(str) refName] = {(str) k_pval : (int) p-value, (str) k_cov : (int) cov}) reads: 
	  reads, their p-value and coverage
	'''
	with open(outputPath,'w') as output:
		for refName in reads:
			line = "%s\n" % (refName)
			output.write(line)

def unittests():
	test_getAlignedLength()	
	test_updateDistribution()
	test_getPValues()
	test_getCovs()
	test_combineCovsAndPValues()
	print "All tests passed!"

parser = argparse.ArgumentParser(description='''
	Coverage generator
       	''') 
parser.add_argument('-b', '--bam', metavar='BAM', type=str, help=
       	"""
       	Provide the input BAM file
       	""")
parser.add_argument('-f', '--fasta', metavar='FASTA', type=str, help=
	"""
	Provide the FASTA index file 
	""")
parser.add_argument('-o', '--output', metavar='OUTPUT', type=str, help=
	"""
	Provide the output path for preserved long reads.
	""")
parser.add_argument('-a', '--alpha', metavar='ALPHA', type=float, help=
	"""
	Specify the alpha value for P-Value threshold.
	Default: %.2f
	""" % (g_alpha))
parser.add_argument('-c', '--cov', metavar='COV', type=int, help=
	"""
	Specify the coverage threshold.
	Default: %d
	""" % (g_cov))	
parser.add_argument('-t', '--tests', action='store_true', help=
       	"""
       	Perform unit tests
       	""")

args = parser.parse_args()
optsIncomplete = False

if args.tests:
	unittests()
	sys.exit()

if args.alpha:
	g_alpha = args.alpha

if args.cov:
	g_cov = args.cov

if args.fasta:
	fastaName = args.fasta
else:
	print "Please provide the FASTA index path"
	optsIncomplete = True

if args.bam:
	bamName = args.bam
else:
	print "Please provide the input BAM file"
	optsIncomplete = True

if args.output:
	outputPath = args.output
else:
	print "Please provide the output path."
	optsIncomplete = True

if optsIncomplete:
	sys.exit()

readLengths = ReadLengths()
readLengths.load(fastaName)
lengths = readLengths.getLengths()
dists = constructDistributions(bamName,lengths)
pVals = getPValues(dists)
covs = getCovs(dists)
reads = combineCovsAndPVals(pVals,covs)
prunePValues(reads)
pruneCovs(reads)
writePreservedReads(outputPath)
