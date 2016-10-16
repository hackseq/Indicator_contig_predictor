import argparse
from scipy.stats import chisquare
from pysam import AlignmentFile
import numpy

# Default global variables
g_alpha = 0.05
k_pval = "PVAL"

def getAlignedLength(cigarTups):
	'''
	Returns the length of aligned bases in the reference sequence given a list of CIGAR tuples
	Inputs
	- (list of ( (str) operation, (int) length)) cigarTups: the cigar tuples returned by pysam 
	Outputs
	- int length: length of aligned bases in the reference sequence 
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

def updateDistribution(dists, refName, start, cigarTups):
	'''
	Update the coverage distribution for the given long read
	Inputs
	- ( dict[str] = (numpy.array of ints) ) dists: contains the coverage distributions for each long read
	- (str) refName: name of long read
	- (int) start: position in long read that alignment starts at
	- (list of ( (str) operation, (int) length)) cigarTups: the cigar tuples returned by pysam 
	'''
	if not refName in dists:
		refLength = readLengths[refName]
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
		

def constructDistributions(bamName, readLengths):
	'''
	Given a BAM file, constructs a coverage distribution for each long read
	Inputs
	- (str) bamName: BAM file name
	- (dict[(str) refName] = (int) read length) readLengths: returns the length of the long read given its read name
	Outputs
	- ( dict[(str) refName] = (numpy.array of ints) distribution ) dists: contains the coverage distributions 
          for each long read
	'''
	samfile = AlignmentFile(bamName, 'rb')
	iter = samfile.fetch()
	dists = {}
	for alignment in iter: 
		refName = alignment.reference_name()
		start = alignment.reference_start() 
		cigarTups = alignment.cigartuples()
		updateDistributions(dists, refName, start, cigarTups)
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

def prunePValues(reads):
	'''
	Throws out all long reads in pValues with p-value less than 1.0 - g_alpha
	Inputs
	- (dict[(str) refName] = {(str) k_pval : (int) p-value, (str) k_cov : (int) cov}): 
	'''
	for refName in pValues:
		pVal = pValues[refName][k_pval]
		if pVal < (1.0-g_alpha):
			del 

def unittests():
	test_getAlignedLength()	
	test_updateDistribution()
	test_getPValues()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='''
		Coverage generator
        	''') 
	parser.add_argument('-i', '--input', metavar='BAM', type=str, help=
        	"""
        	provide the input BAM file
        	""")
	parser.add_argument('-a', '--alpha', metavar='ALPHA', type=float, help=
		"""
		specify the alpha value for P-Value threshold.
		Default: 0.05
		""")
	parser.add_argument('-t', '--tests', action='store_true', help=
        	"""
        	perform unit tests
        	""")

	args = parser.parse_args()

	if args.tests:
		unittests()
	if args.alpha:
		g_alpha = args.alpha
