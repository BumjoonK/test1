#! /usr/bin/python3

import sys
import os



#def down(fastq):
    #os.system("/BiO/Install/sratoolkit.2.9.6-ubuntu64/bin/fastq-dump --gzip --split-3 {0} ".format(fastq))

#def gunzip(fastq):
    #os.system("gunzip {0}_1.fastq.gz".format(fastq))
    #os.system("gunzip {0}_2.fastq.gz".format(fastq))

def fastQC(fastq):
   os.system("/BiO/Install/FastQC_0.10.1/fastqc -t 4 --nogroup {0}_1.fastq".format(fastq))
   os.system("/BiO/Install/FastQC_0.10.1/fastqc -t 4 --nogroup {0}_2.fastq".format(fastq))



def trim(fastq):
    os.system("java -jar /BiO/Install/Trimmomatic-0.38/trimmomatic-0.38.jar PE -threads 4 -phred33 {0}_1.fastq {0}_2.fastq {0}_1.trim.fq {0}_1.unpair.fq {0}_2.trim.fq {0}_2.unpair.fq ILLUMINACLIP:/BiO/Install/Trimmomatic-0.38/adapters/TruSeq3-PE-2.fa:2:151:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36".format(fastq))
       
def mapping(fastq):
    os.system("bwa mem -t 4 -R '@RG\\tPL:Illumina\\tID:KBJ\\tSM:{0}\\tLB:HiSeq' /BiO/Access/home/kbioedu07/NCBI.seq/E.coli_2/BW25113.fa {0}_1.trim.fq {0}_2.trim.fq > {0}.sam".format(fastq))

def duprmv(fastq):
#    os.system("mkdir TEMP_PICARD")
    os.system("java -jar /BiO/Install/picard-tools-2.22.3/picard.jar AddOrReplaceReadGroups TMP_DIR=TEMP_PICARD VALIDATION_STRINGENCY=LENIENT SO=coordinate I={0}.sam O={0}_sorted.bam RGID={0} RGLB=HiSeq RGPL=Illumina RGPU=unit1 RGSM={0} CREATE_INDEX=true".format(fastq))    
    os.system("java -jar /BiO/Install/picard-tools-2.22.3/picard.jar MarkDuplicates TMP_DIR=TEMP_PICARD VALIDATION_STRINGENCY=LENIENT I={0}_sorted.bam O={0}_dedup.sam M={0}.duplicate_metrics REMOVE_DUPLICATES=true AS=true".format(fastq))
    os.system("java -jar /BiO/Install/picard-tools-2.22.3/picard.jar SortSam TMP_DIR=TEMP_PICARD VALIDATION_STRINGENCY=LENIENT SO=coordinate I={0}_dedup.sam O={0}_dedup.bam CREATE_INDEX=true".format(fastq))

"""
def bqsr(fastq):
    os.system("java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar BaseRecalibrator -R "reference path" -I {0}_dedup.bam --known-sites /BiO/Education/WGS/REF/dbsnp_138.hg19.vcf --known-sites /BiO/Education/WGS/REF/1000GENOMES-phase_3_indel.vcf -O {0}_recal_pass1.table".format(fastq))
    os.system("java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar ApplyBQSR -R "reference path"  -I {0}_dedup.bam --bqsr-recal-file {0}_recal_pass1.table -O {0}_recal_pass1.bam".format(fastq))
    os.system("java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar BaseRecalibrator -R "reference path" -I {0}_recal_pass1.bam --known-sites /BiO/Education/WGS/REF/dbsnp_138.hg19.vcf --known-sites /BiO/Education/WGS/REF/1000GENOMES-phase_3_indel.vcf -O {0}_recal_pass2.table".format(fastq))
    os.system("java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar ApplyBQSR -R "reference path" -I {0}_recal_pass1.bam -bqsr {0}_recal_pass2.table -O {0}_recal_pass2.bam".format(fastq))
"""

def varcall(fastq):
    os.system("java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar HaplotypeCaller -R /BiO/Access/home/kbioedu07/NCBI.seq/E.coli_2/BW25113.fa -I {0}_dedup.bam -O {0}.rawVariants.g.vcf -ERC GVCF --standard-min-confidence-threshold-for-calling 20".format(fastq))

def gvcf(fastq):
    os.system("java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar GenotypeGVCFs -R /BiO/Access/home/kbioedu07/NCBI.seq/E.coli_2/BW25113.fa -V {0}.rawVariants.g.vcf -O {0}_genotype.vcf".format(fastq))

#def extc(fastq):
#    os.system("java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar SelectVariants -R /BiO/Access/home/kbioedu07/NCBI.seq/E.coli_2/BW25113.fa -V {0}_genotype.vcf --select-type-to-include SNP -O {0}.rawSNPs.vcf".format(fastq))
#    os.system("java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar SelectVariants -R /BiO/Access/home/kbioedu07/NCBI.seq/E.coli_2/BW25113.fa -V {0}_genotype.vcf --select-type-to-include INDEL -O {0}.rawINDELs.vcf".format(fastq))

#def filt(fastq):
#    os.system("java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar VariantFiltration -R /BiO/Access/home/kbioedu07/NCBI.seq/E.coli_2/BW25113.fa -V {0}.rawSNPs.vcf -O {0}.rawSNPs.filtered.vcf --filter-name "." --filter-expression "QD < 2.0 || FS > 60.0 || MQ < 40.0 || HaplotypeScore > 13.0 || MappingQualityRankSum < 12.5 || ReadPosRankSum <-8.0"".format(fastq))
#    os.system("java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar VariantFiltration -R /BiO/Access/home/kbioedu07/NCBI.seq/E.coli_2/BW25113.fa -V {0}.rawINDELs.vcf -O {0}.rawINDELs.filtered.vcf --filter-name "." --filter-expression "QD < 2.0 || FS > 200.0 || ReadPosRnakSum <-20.0"".format(fastq))

fastq =sys.argv[1]
#down(fastq)
#gunzip(fastq)
fastQC(fastq)
trim(fastq)
mapping(fastq)
duprmv(fastq)
#bqsr(fastq)
varcall(fastq)
#gvcf(fastq)
#extc(fastq)
#filt(fastq)
