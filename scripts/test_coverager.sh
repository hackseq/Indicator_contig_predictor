#!/bin/bash

dir=/home/devsci2/junk
bamList=bams.txt
coverager=/home/devsci1/src/coverager.py
faidex=${dir}/infant_gut_microbiome_PacBio.fasta.fai

while IFS='' read -r line || [[ -n "$line" ]]; do
	bam=$dir/$line
	output=${line}_preserved.txt
	echo $bam
	python $coverager -f $faidex -b $bam -o $output 
done < "$bamList"
