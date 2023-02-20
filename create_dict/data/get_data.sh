#!/bin/bash

if [ ! -f 38-All.vcf.gz ]; then
	echo 'DBsnp file is not found, downloading ...'
	wget ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b147_GRCh38p2/VCF/00-All.vcf.gz
	wget ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b147_GRCh38p2/VCF/00-All.vcf.gz.tbi
	mv 00-All.vcf.gz 38-All.vcf.gz
	mv 00-All.vcf.gz.tbi 38-All.vcf.gz.tbi
	echo 'DBsnp downloading is finished.'
else
	echo 'DBsnp file is found!'

if command -v bwa >/dev/null 2>&1; then
	echo >&2 "I require BWA but it's not installed. Install."
	wget -O bwa-0.7.15.tar.bz2 https://sourceforge.net/projects/bio-bwa/files/bwa-0.7.15.tar.bz2/download 
	tar -zxvf bwa-0.7.15.tar.bz2
	cd bwa-0.7.15
	make install
	PATH=$PATH:~/opt/bin:$(pwd)
	cd ..

if [ ! -f hg38_23chrom.fa ]; then
    echo "File refence genome not found!"
    echo "Downloading refence genome ..."
	wget http://hgdownload.cse.ucsc.edu/goldenPath/hg38/bigZips/hg38.chromFa.tar.gz
	tar -zxvf hg38.chromFa.tar.gz
	rm -rf hg38.chromFa.tar.gz
	
	cd chroms
	echo -n > hg38_23chrom.fa
	
	for i in {1..22}
	do
	   echo chr$i.fa
	   cat chr$i.fa >> hg38_23chrom.fa
	   rm -rf chr$i.fa
	done
	for i in X Y M
	do
	   echo chr$i.fa
	   cat chr$i.fa >> hg38_23chrom.fa
	   rm -rf chr$i.fa
	done
	rm -rf chr*
	echo "Indexing refence genome ..."
	bwa index hg38_23chrom.fa
	echo "Indexing refence genome is finished"
	cd ..
else
	echo 'Reference genome is found!'

if [ ! -f snp_new.txt ]; then
    echo "File snp_new not found!"
	echo "Downloading Atlas BioMed data base ..."
	psql "dbname='snp_new' user='imgeneticist' host='192.168.22.101' password='SVzH9KK9UxDwNwCGNg4R8j'"
	\copy (SELECT * from snp_names) TO snp_name.csv CSV DELIMITER ','
	echo "Finished downloading Atlas BioMed data base."
else
	echo 'Atlas BioMed data base is found!'
fi



