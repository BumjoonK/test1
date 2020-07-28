#! /usr/bin/env python
# -*- coding: utf-8 -*-

#Step 0 퀄리티가 낮은 데이터르 제거하기 위하여 QC를 통해 good reads 들을 추출한다.
#Step 1 레퍼런스 서열에 시퀀스 read 맵핑을 수행
#Step 2 시퀀싱 과정중 PCR에서 이상적으로 증폭된 duplicated reads를 제거

print("Raw data download")
/BiO/Install/sratoolkit.2.9.6-ubuntu64/bin/fastq-dump --gzip --split-3 SRR1002940

#sratoolkit는 NCBI에서 data download, forwoard와 reverse sequence 생성

print("Fastq data format")

less -S SRR1002940.r1.temp.fq

#-S 옵션은 결과를 clear하게 보여준다. line1: @로 시작, read에 대한 기본정보를 포함하며 line2는 nucleotide sequence line4는 quality를 나타낸다.

print("Step0. Short reads의 QC 및 전처리")

/BiO/Install/FastQC_0.10.1/fastqc -t 4 --nogroup SRR1002940.r1.trim.fq

#quality score는 error rate 0.1% 이하로 나오도록 정리해야하며 phred scoring scheme을 사용한다.

print("Short reads의 QC 및 전처리")

java -jar /BiO/Install/Trimmomatic-0.38/trimmomatic-0.38.jar PE -threads 4 -phred33 SRR1002940.r1.temp.fq SRR1002940.r2.temp.fq SRR1002940.r1.trim.fq SRR1002940.r1.unpair.fq SRR1002940.r2.trim.fq SRR1002940.r2.unpair.fq ILLUMINACLIP:/BiO/Install/Trimmomatic-0.38/adapters/TruSeq3-PE-2.fa:2:151:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36

#Trimmomatic은 illumina의 시권싱 장비에서 생성된 데이터의 trimming 작업을 수행, threads는 사용되는CPU 개수 phred는 qc 점수style, fq 파일은 input, trim.fq가 생성 파일 unpair.fq가 오류나는 파일(pair가 되지 않는)
#TruSeq-PE-2.fa adapter fasta 파일, 2:151:10 미스매치 2개 허용 만들어지는 read length 최대값 151 adapter score 10, LEADING:3, TRAILING:3 read 전후의 quality가 3보다 낮을 경우 제거, SLIDINGWINDOW:4:15 window 4bp만큼 시퀀스를 슬라이딩하며(4개를 연속적으로 읽으면서) 구간내의 평균 qualiy 15보다 낮을 경우 제거, MINLEN:36 36 bp보다 short할 경우 제거

#Step 1 레퍼런스 서열에 시퀀스 read 맵핑을 수행
-R '@RG\tPL:Illumina\tID:YUHL\tSM:SRR1002940\tLB:Hiseq'/BiO/Education/WGS/REF/hg19.fa SRR1002940.r1.trim.fq SRR1002940.r2.trim.fq > SRR1002940.sam

#-R:읽을 그룹들을 작성하는 옵션 \t 는 그냥 출력 포멧
#BWA(Burrows-Wheeler Aligner)는 short reads들을 레퍼런스 서열에 맵핑 시키는 툴, mapping output은 SAM파일로 형성 read, mapping 정보
#whole genome 분석보다는 다른 경우 많이 사용

#Step2 Mark Duplicates(PICARD) 시퀀싱 과정중 PCR에서 이상적으로 증폭된 duplicated reads를 제거

#1.Duplication tagging

mkdir TEMP_PICARD

java -jar /BiO/Install/picard-tools-2.22.3/picard.jar AddOrReplaceReadGroups TMP_DIR=TEMP_PICARD VALIDATION_STRINGENCY=LENIENT SO=coordinate I=SRR1002940.sam O=SRR1002940_sorted.bam RGID=SRR1002940 RGLB=HiSeq RGPL=Illumina RGPU=unit1 RGSM=SRR1002940 CREATE_INDEX=true

#STRINGENCY LENIENT 설정은validation을 관대하게 허락함, SO=sorting order, I=input O=output sam 파일은 용량이 커서 바이너리 파일 BAM으로 교체, RGID=read group id, RGLB=read group library, SM=sample indexing해주는 이유는 bai라는 indexing 파일이 존재한다.

#2. Remove duplicates(제거하기 전에 순서를 맞춰야함)

java -jar /BiO/Install/picard-tools-2.22.3/picard.jar MarkDuplicates TMP_DIR=TEMP_PICARD VALIDATION_STRINGENCY=LENIENT I=SRR1002940_sorted.bam O=SRR1002940_dedup.sam M=SRR1002940.duplicate_metrics REMOVE_DUPLICATES=ture AS=true

#M=matrix 이 파일에 로그를 남기게 됨, 복제된 것을 인식하다가 remove_duplicate=true로 삭제, AS=true로 다시 sorting #2의 input파일은 #1의 output파일

#3.Sorting

java -jar /BiO/Install/picard-tools-2.22.3/picard.jar SortSam TMP_DIR=TEMP_PICARD VALIDATION_STRINGENCY=LENIENT SO=coordinate I=SRR1002940_dedup.sam O=SRR1002940_dedup.bam CREATE_INDEX=true

#dedup.bam이 제일 중요한 모든걸 확인하는 경로
#삭제된 SAM 파일 보기 위해 samtools view SRR1002940_sorted.bam > test.sam       

#Step 3.변이의 정확도를 높이기 위해 base recalibration의 보정 작업을 수행
#Step3-1. Base Quality Score Recalibration-first pass(GATK)->2 steps region을 찾고 apply함

#Step 3-1 1) 시퀀싱 데이터에서 covariation 패턴 분석

java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar BaseRecalibrator -R /BiO/Education/WGS/REF/hg19.fa -I SRR1002940_dedup.bam --known-sites /BiO/Education/WGS/REF/dbsnp_138.hg19.vcf --known-sites /BiO/Education/WGS/REF/1000GENOMES-phase_3_indel.vcf -O SRR1002940_recal_pass1.bam

#Step 3-1 2) 시퀀싱 데이터에 recalibration을 적용
java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar ApplyBQSR -R /BiO/Education/WGS/REF/hg19.fa -I SRR1002940_dedup.bam --bqsr-recal-file SRR1002940_recal_pass1.table -O SRR1002940_recal_pass1.bam


#Step 3-2 1) 시퀀싱 데이터에서 covariation의 패턴 분석  

java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar BaseRecalibrator -R /BiO/Education/WGS/REF/hg19.fa -I SRR1002940_recal_pass1.bam --known-sites /BiO/Education/WGS/REF/dbsnp_138.hg19.vcf -O SRR1002940_recal_pass2.table

#Step 3-2 2) 시퀀싱 데이터에 recalibration을 적용

java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar ApplyBQSR -R /BiO/Education/WGS/REF/hg19.fa -I SRR1002940_recal_pass1.bam -bqsr SRR1002940_recal_pass2.table -O SRR1002940_recal_pass2.bam

#2번 반복을 통해 오류(sample의 del이 snp나 insert로 착각되는 경우) 잡음

#Step 4-1 Calling variants for all samples with HaplotypeCaller(GATK)
#Variant calling은 HaplotypeCaller를 이용하여 SNPs과 Indels 등 두 가지 유형의 변이를 발굴한 후, 출력 결과로 vcf(Variant Call Format)

java -Xmx9g -jar /BiO/Install/gatk -4.1.7.0 local.jar HaplotypeCaller -R /BiO/Education/WGS/REF/hg19.fa -I SRR1002940_recal_pass2.bam -O SRR1002940.rawVariants.g.vcf -ERC GVCF --standard-min-confidence-threshold-for-calling 20


#-ERC GVCF 여러가지 파일들을 merge가 가능함, group calling var1과 sample 1~n 병합

#Step4-3. Applying GenotypeGVCFs(GATK)

java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar GenotypeGVCFs -R /BiO/Education/WGS/REF/hg19.fa -V SRR1002940.rawVariants.g.vcf -O SRR1002940_genotype.vcf
#V=VCF(variant file을 넣는다)
#deletion은 "*"으로 표시 이 과정의 결과에서는 높은 확률 되는 중으로 표시 아직 확정은 아니다.

#Step5-1. Extracting the SNPs and Indels with SelectVariants

#5-1 1) SNPs 추출
java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar SelectVariants -R /BiO/Education/WGS/REF/hg19.fa -V SRR1002940_genotype.vcf --select-type-to-include SNP -O SRR1002940.rawSNPs.vcf

#5-1 2) Indels 추출
java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar SelectVariants -R /BiO/Education/WGS/REF/hg19.fa -V SRR1002940_genotype.vcf --select-type-to-include INDEL -O SRR1002940.rawINDELs.vcf

#Step 5-2. Applying hard-filtering on the SNPs and Indels with VariantFiltration

#5-2 1) SNPs 필터링

java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar VariantFiltration -R /BiO/Education/WGS/REF/hg19.fa -V SRR1002940.rawSNPs.vcf -O SRR1002940.rawSNPs.filtered.vcf --filter-name "." --filter-expression "QD < 2.0 || FS > 60.0 || MQ < 40.0 || HaplotypeScore > 13.0 || MappingQualityRankSum < -12.5 || ReadPosRankSum < -8.0"

#5-2 2) Indels 필터링

java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar VariantFiltration -R /BiO/Education/WGS/REF/hg19.fa -V SRR1002940.rawINDELs.vcf -O SRR1002940.rawINDELs.filtered.vcf --filter-name "." --filter-expression "QD < 2.0 || FS > 200.0 || ReadPosRankSum < -20.0"

#QD:Quality/Depth; FS: strand bias 검출 위해 Fisher's exact test 사용; MQ: Median QualityRankSum: alternative base가 ref base보다 low MQ를 가진 read가 통ㄱㅖ적으로 유의하게 많으면 mismapped로 간주 ReadPosRnaKSum:alternative base가 read의 시작이나 마지막에 통ㄱㅖ적으로 유의하게 bias시 artifact로 간주
#indel의 양이 방대하기 ㄸㅐ문에 효율을 위해 옵션의 수가 적다 이 후 validation 이 후 다시 설정

#Step5-3. Merge the file for SNPs and Indels with MergeVCFs

#option1 SortVcf
java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar SortVcf -I SRR1002940.rawSNPs.filtered.vcf -I SRR1002940.rawINDELs.filtered.vcf -O SRR1002940.Filtered.variant.vcf

#option2 MergeVcfs
java -Xmx8g -jar /BiO/Install/gatk-4.1.7.0/gatk-package-4.1.7.0-local.jar MergeVcfs -I SRR1002940.rawSNPs.filtered.vcf -I SRR1002940.rawINDELs.filtered.vcf -O SRR1002940.Filtered2.variant.vcf

#둘 중에 비교해서 더 잘나온거 사용

#STEP 6-1. Annotation using Annovar- Variant annotation은 발굴한 변이들에 대한 특성을 확인하는 단ㄱㅖ로 Variant Annotation tool을 이용하여 변이들에 annotation을 추가한다.

egrep "^#|PASS" SRR1002940.Filtered.variant.vcf > SRR1002940.Filtered.variant.PASS.vcf
#egrep "^" cmd 중요하다 연습하기, vcf 파일은 #로 구분, 이 중 PASS인 애들만 선별하는 명령어 ">"로 그 뒤에 나오는 변수명의 파일을 생성

perl /BiO/Install/annovar/table_annovar.pl SRR1002940.Filtered.variant.PASS.vcf /BiO/Education/WGS/humandb/ -buildver hg19 -out SRR1002940 -remove -protocol refGene,cytoBand,avsnp138,clinvar_20190305 -operation g,r,f,f -nastring . -vcfinput

#pl=perl 파일, annova는 input 때  -I는 따로 ㅆㅡ지않음 이후 annova를 수행하기 위해 db의 path 입력 후 버젼입력(-buildver hg19) output은 "out" 변수명에 prefix만 입력해도됨, remove PICARD처럼 쓰고지우다가 최종파일만 남김 마지막에 protocol에서 database의 옵션을 말해줌 ","로 이어짐  operation g,r,f,f는 고정 g-gene(refGene) r-region(cytoBand) f-file(avsnp138, clinvar_20190305, -vcfinput = input file은 vcf로
#하나씩 따로 할 수 있는 경우 annovar_table.pl 을 사용

#SNPeff 다운로드
wget http://sourceforge.net/projects/snpEff/files/snpEff_latest_core.zip

#UNZIP
unzip snpEff_latest_core.zip

java -jar snpEff/snpEff.jar databases | grep hg19
#java를 통해 snpEff.jar에 본인의 연구종의 database가 있는지 확인

java -jar /BiO/Access/home/kbioedu07/snpEff/snpEff.jar -v hg19 SRR1002940.Filtered.variant.PASS.vcf > SRR1002940.snpEff.vcf
#자신의 path를 통해 snpEff 실행, 유전적 변이에 대한 annotation을 수행하는 프로그램으로 염기서열 변경에 의한 아미노산 서열의 변화와 같은 변이의 구조적 영향을 예측하는데 사용된다.

java -jar /BiO/Access/home/hykim/YUHS/DATA2/snpEff/snpEff.jar -v hg19 SRR1002940.Filtered.variant.PASS.vcf > SRR1002940.snpEff.vcf
#tmp 파일의 권한이 루트로 접근해서 파일의 쓰기 권한이 없기 때문에 강사님의 파일에 존재하는 snpEff를 사용했다.

#SnpSift Annotate(dbSNP) 한번에 annotate되지 않기 때문에 하나씩 annote, 알려진 snp가 ID에 rs number가 붙음
java -jar /BiO/Access/home/hykim/YUHS/DATA2/snpEff/SnpSift.jar annotate /BiO/Education/WGS/REF/dbsnp_138.hg19.vcf SRR1002940.snpEff.vcf > SRR1002940.snpEff.dbSNP138.vcf

#dbSNP138(hg19) 다운로드
#> wget ftp://gsapubftpanonymous@ftp.broadinstitute.org/bundle/hg19/dbsnp_138.hg19.vcf.gz
#> gunzip dbsnp_138.hg19.vcf.gz
#> java -Xmx8g -jar /home/program/gatk-4.0.11.0/tk-package-4.0.11.0-local.jar IndexFeatureFile -F /home/hykim/REF/dbsnp_138.hg19.vcf
#tar -zxvf annovar.latest.tar.gz
#Additional databases(ANNOVAR main package
#Region-based /BiO/Install/annovar/annotate_variation.pl -buildver hg19 -downdb cytoBand humandb/
#Gene-based /BiO/Install/annovar/annotate_variation.pl -buildver hg19 -downdb -webfrom annovar dbnsfp30a humand/
#Filter-based  /BiO/Install/annovar/annotate_variation.pl -buildver hg19 -downdb -webfrom annovar clinvar_20200316 humandb/
# /BiO/Install/annovar/annotate_variation.pl -buildver hg19 -downdb -webfrom annovar avsnp138 humandb/
#http://annovar.openbioinformatics.org/en.latest/user-guide/startup/

# 최상위 디렉토리로 이동 후 find ./ -name annotate* 로 디렉토리 이름찾기
