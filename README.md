# De novo metagenomic marker pipeline

## Roadmap
1. Human Infant Microbiome Dataset ("Babybiome")
  * Kudos to Molly K. Gibson for excellent datasharing
2. BLAST script 
  * Based on magicBLAST, a new RNAseq BLAST mapper
3. Coverage generator
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

