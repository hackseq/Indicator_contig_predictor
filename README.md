# De novo metagenomic marker pipeline

## Pipeline
1. Human Infant Microbiome Dataset ("Babybiome")
  * Kudos to Molly K. Gibson for excellent datasharing
  [(Gibson MK, Wang B, Ahmadi S, et al. Developmental dynamics of the preterm infant gut microbiota and antibiotic resistome. Nature microbiology. 2016;1:16024.)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5031140/)
2. /src/query.py
  * Based on magicBLAST, a new RNAseq BLAST mapper
3. /src/coverager.py & /scripts/test_coverager.sh
  * Generation of BAMs with magicBLAST mapping to long reads (direct streaming from SRA)
  * Building a histogram of read coverage
   * Thresholding for uniform deep and broad coverage of long reads with short reads (indicator contigs) 
   * Using chi-squared test to check for uniformity
   * Generating probability of long read in short read set
4. Gen. Classifier 
  * Separation by physiological features
   * Male-Female
   * Delivery mode
5. Probability of gene co-occurrence?

