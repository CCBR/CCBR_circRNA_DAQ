import pysam
import pprint
import sys
import argparse
import os
from itertools import groupby

def split_text(s):
    for k, g in groupby(s, str.isalpha):
        yield ''.join(g)

def get_alt_cigars(c):
	alt_cigars=[]
	x=list(split_text(c))
	if x[1]=="H":
		alt_cigars.append("".join(x[2:]))
	if x[-1]=="H":
		alt_cigars.append("".join(x[:-2]))
	if x[1]=="H" and x[-1]=="H":
		alt_cigars.append("".join(x[2:-2]))
	return alt_cigars

pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser(description='Filter readid filtered BAM file for BSJ alignments')
parser.add_argument('--inputBAM', dest='inputBAM', type=str, required=True,
                    help='input BAM file')
parser.add_argument('--outputBAM', dest='outputBAM', type=str, required=True,
                    help='filtered output BAM file')
parser.add_argument('--readids', dest='readids', type=str, required=True,
                    help='file with readids to keep (tab-delimited with columns:readid,chrom,strand,site1,site2,cigarlist)')
args = parser.parse_args()
rids=dict()
inBAM = pysam.AlignmentFile(args.inputBAM, "rb")
outBAM = pysam.AlignmentFile(args.outputBAM, "wb", template=inBAM)

# multiple alignments of a read are grouped together by 
# HI i Query hit index ... eg. HI:i:1, HI:i:2 etc. --> See https://samtools.github.io/hts-specs/SAMtags.pdf
# each HI represents a different alignent for the pair and 
# generally contains 3 lines in the alignment file eg:
# SRR1731877.10077876	163	chr16	16699505	1	30S53M	=	16699513	53	CTACCGTTTCCTGTGATAAGTGCTACTTCTTGAGGCTCTGTTCCATCTTTGTCCCTTTCCAGAGATTTAATCTCTCTCTCTCT	;DDDDHBFHHDG@AAFHHGEHHIIIIIIIIIBDGIEH3DDHGC4?09?BBB0999B?8)./>FH>GHG>==CE@@A>>AE?;;	NH:i:4	HI:i:1	AS:i:97	nM:i:0	NM:i:0	SA:Z:chr16,16700448,+,30M53H,1,0;
# SRR1731877.10077876	83	chr16	16699513	1	45M	=	16699505	-53	TGTTCCATCTTTGTCCCTTTCCAGAGATTTAATCTCTCTCTCTCT	DGD>B@?;B@GFC88ECADCFHEE@C<@C:2A<A+C?DBB:D?;?	NH:i:4	HI:i:1	AS:i:97	nM:i:0	NM:i:0
# SRR1731877.10077876	2209	chr16	16700448	1	30M53H	=	16699513	0	CTACCGTTTCCTGTGATAAGTGCTACTTCT	;DDDDHBFHHDG@AAFHHGEHHIIIIIIII	NH:i:4	HI:i:1	AS:i:29	nM:i:0	NM:i:0	SA:Z:chr16,16699505,+,30S53M,1,0;
# 2 of these lines represent the split alignment of 1 mate and the 3rd line is the alignment of the 2nd mate
# rids is dict with readids as keys
# each readid may have multiple HI values, each of which is a dict
# each HI value has 3 lists a) sites b) cigars c) alignments ... each of these lists have 3 elements each

count=0
for read in inBAM.fetch():
	count+=1
	qn=read.query_name
	if not qn in rids:
		rids[qn]=dict()
	hi=read.get_tag("HI")
	if not hi in rids[qn]:
		rids[qn][hi]=dict()
		rids[qn][hi]['alignments']=list()
		rids[qn][hi]['sites']=list()
		rids[qn][hi]['cigars']=list()
	rids[qn][hi]['alignments'].append(read)
	site=read.get_reference_positions()[1]
	cigar=read.cigarstring
	cigar=cigar.replace("S","H") # convert soft-clips to hard-clips ... readids file has all hard-clips ... required for comparison
	rids[qn][hi]['sites'].append(site)
	rids[qn][hi]['cigars'].append(cigar)
	rids[qn][hi]['cigars'].sort()	
	#print(site)
	#print(cigar)
	#print(len(rids[qn]))
	#if count==25:
	#	pp.pprint(rids)
	#	for rid in rids:
	#		print(rid,len(rids[rid]))
	#	exit()
inBAM.close()

#print(rids["SRR1731877.10077876"].keys())
#exit()

readidfile = open(args.readids,'r')
readids = readidfile.readlines()
readidfile.close()

#print(rids.keys())



for line in readids:
	line=line.strip().split("\t")
	# print(line)
## SRR1731877.10077876	chr16	-	16699504	16700478	30H53M,45M,30M53H
## columns:readid,chrom,strand,site1,site2,cigarlist
## this is generated by junctions2readids.py from the .junction file from STAR2p
	readid=line[0]
	chrom=line[1]
	strand=line[2]
	site1=line[3]
	site2=line[4]
	cigars=line[5].split(",")
	cigars.sort()
## as we are searching for the alignment which represents this occurance 
## (which of the multiple HI values should we report in the output BAM) 
## of this readid in the readids file,
## TEST #1
## We first compare site (or coordinate)
## If strand is -ve, then site1 is expected to be in the reported alignment
## but if the strand is +ve, the site2 is expected to be in the 'sites' list 
## note: we have to add 1 to switch from 0-based to 1-based
	if strand=="-":
		site=int(site1)+1
	else:
		site=int(site2)+1
## readid will always be part of rids... but just in case
	if not readid in rids:
		continue
	for hi in rids[readid].keys():
		# print(readid,hi,site)
		# print(site,"===>>",rids[readid][hi]['sites'])
		# print(site in rids[readid][hi]['sites'])
		# print(cigars,"====>>",rids[readid][hi]['cigars'])
		# print(rids[readid][hi]['cigars'] == cigars)
		if site in rids[readid][hi]['sites']:
## TEST #2
## we know that site is present in sites of this alignment
## next we ensure that all 3 alignments of this HI value are on the same chromosome/reference
			references=[]
			for read in rids[readid][hi]['alignments']:
				references.append(read.reference_name)
			if len(list(set(references)))!=1: # same HI but different aligning to different chromosomes
				continue
			rids[readid][hi]['alignments']=list(set(rids[readid][hi]['alignments']))
## TEST #3.1
## we know that site is in 'sites' and all 3 alignment from the HI value are on the same chromosome
## next we check if the CIGAR scores of the 3 alignments are the same as the CIGAR scores from the readids file
			if rids[readid][hi]['cigars'] == cigars: # lists are sorted before comparison
				for read in rids[readid][hi]['alignments']:
					outBAM.write(read)	
			else:
## TEST #3.2
## some alignments are missed because of extra soft clipping in one of the 3 reported alignments in a single HI value
## eg.
# SRR1731877.16929220	83	chr7	99416198	255	5S48M1S	=	99416198	-48	GGAAGTCCACCACCAGAAAACCCGCTACATCTTCGACCTCTTTTACAAGCGGAC	FEHC>HHE@GC=GCIIJIGDIJJIJJIJJJJJJIHGJJIIIHHGHHFFFFFCC@	NH:i:1	HI:i:1	AS:i:95	nM:i:0	NM:i:0
# SRR1731877.16929220	163	chr7	99416198	255	42S48M1S	=	99416198	48	CAGAAAACCCGCTACATCTGCGACCTCTTTTACAAGCGGAAATCCACCACCAGAAAACCCGCTACATCTTCGACCTCTTTTACAAGCGGAC	@@BFFFFFHHHHHJJJJJJHIJJJJJJJJJJIJJJIIIIGJJCFHHGJHGEHEFFFFEDCDDDDDDDDDDEDDDDDDDDDDDDCDDDDDDD	NH:i:1	HI:i:1	AS:i:95	nM:i:0	NM:i:0	SA:Z:chr7,99416206,+,42M49H,255,1;
# SRR1731877.16929220	2209	chr7	99416206	255	42M49H	=	99416198	0	CAGAAAACCCGCTACATCTGCGACCTCTTTTACAAGCGGAAA	@@BFFFFFHHHHHJJJJJJHIJJJJJJJJJJIJJJIIIIGJJ	NH:i:1	HI:i:1	AS:i:39	nM:i:1	NM:i:1	SA:Z:chr7,99416198,+,42S48M1S,255,0;
# the readids file contains
# SRR1731877.16929220	chr7	-	99416197	99416248	42H48M,48M1H,42M49H
# cigars from readids file --> 42H48M,48M1H,42M49H
# cigars from bam file --> 42H48M,5H48M1H,42M49H
# this is fix to include these alignments in the output BAM
# recompare cigars after removing softclippings at the ends of the CIGAR of non-matching cigar string
				aminusb=list(set(rids[readid][hi]['cigars'])-set(cigars))
				if len(aminusb)==1:
					restcigars=list(set(rids[readid][hi]['cigars'])-set(aminusb))
					altcigars=get_alt_cigars(aminusb[0])
					for ac in altcigars:
						newcigars=[]
						newcigars.extend(restcigars)
						newcigars.append(ac)
						newcigars.sort()
						if newcigars == cigars:
							for read in rids[readid][hi]['alignments']:
								outBAM.write(read)
							break
## TEST #3.3
## similar to 3.2 some alignments are missed because of extra soft clipping in 2 of the 3 reported alignments in a single HI value
# this is fix for that scenario
				if len(aminusb)==2:
					commoncigar=list(set(rids[readid][hi]['cigars'])-set(aminusb))
					altcigars1=get_alt_cigars(aminusb[0])
					altcigars2=get_alt_cigars(aminusb[1])
					found=0
					for ac1 in altcigars1:
						if found!=0:
							break
						tmpcigars=[]
						tmpcigars.extend(commoncigar)
						tmpcigars.append(ac1)
						for ac2 in altcigars2:
							newcigars=[]
							newcigars.extend(tmpcigars)
							newcigars.append(ac2)	
							newcigars.sort()
							if newcigars == cigars:
								for read in rids[readid][hi]['alignments']:
									outBAM.write(read)
								found=1
								break
outBAM.close()