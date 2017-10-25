#!/usr/bin/env python
# -*- coding utf-8 -*-
import os
import sys
import re
import argparse


parser = argparse.ArgumentParser(description="python survey.py --step 01234 --name Buleberry --list Buleberry.list --pwd /PROJ/GR/DENOVO/Buleberry/Buleberry/ --cvg_hight 3")
parser.add_argument("--step",type=str,help="1:survey;2:assemble;3:contig_coverage;[required]")
parser.add_argument("--name",type=str,help="the name of species[required]")
parser.add_argument("--max_len",type=int,default=150,help="the max len of the reads ,the default is 150[Optional]")
parser.add_argument("--surv_kmer",type=int,default=17,help="the kmer of survey,default 17")
parser.add_argument("--cvg_hight",type=int,default=0,help="if not 0, output Kmers that cvg ge cvg_Hight,default 0")
parser.add_argument("--ass_kmer",type=int,default=41,help="the kmer of assemble,default 41")
parser.add_argument("--list",type=str,help="the list of rmdup clean data path[required]")
parser.add_argument("--info_lib",type=str,help="the stat file of QC result[optional]")
parser.add_argument("--size_flow",type=str,help="the genome size by flow cytometer experiment[optional]")
parser.add_argument("--pwd",type=str,help="the path of current directory [required]")
parser.add_argument("--cfg",type=str,help="the config file for assemble(only required in step2)")

args = parser.parse_args()
c_path = args.pwd
s_k = args.surv_kmer
ch = args.cvg_hight
ls = args.list
max_len = args.max_len
name = args.name
a_k = args.ass_kmer


if '0' in args.step:
	mypath = c_path + '/' + ls
	f1 = open(mypath,'r')
	os.mkdir(c_path + '/00NT')
	os.chdir(c_path + '/00NT')
	fd = os.open("NT.list",os.O_RDWR|os.O_APPEND|os.O_CREAT)
	count = 0
	name_file1 = ''
	for lines in f1:
		file1 = os.path.basename(lines.strip())		
		count += 1
		if count % 2 == 1:
			name_file1 = file1.strip().split('.')[0]
	                os.write(fd,'%s\t'%lines.strip())
	        else:
	    	        os.write(fd,'%s\t%s\n'%(lines.strip(),name_file1))
	fd2 = os.open("sh4NT.sh",os.O_RDWR|os.O_CREAT)
	os.write(fd2,"perl /PROJ/DENOVO/pipeline/02.survey/survey/bin/shell4blast_nt.pl -f %s/00NT/NT.lst -o ./"%c_path)
	os.close(fd)
	os.close(fd2)

if '1' in args.step:
	os.mkdir(c_path + '/01Survey')
	os.chdir(c_path + '/01Survey')
	sd = os.open("sh4kmerfreq.sh",os.O_RDWR|os.O_CREAT)
	s1 = '''perl /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/sh4cfg.pl %(pwd)s/%(ls)s %(max_len)d
/PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/SoapKF pregraph -p 22 -s kmer.cfg -K %(s_k)d -o %(name)s -h %(cvg_hight)d > pregraph.log
perl /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/sh4draw.pl %(name)s.%(s_k)d.merFreq
/PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/Genomeye -k %(s_k)d %(name)s.%(s_k)d.merFreq > %(name)s.%(s_k)d.merFreq.result
perl /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/sh4geninfo.pl %(name)s.%(s_k)d.merFreq %(name)s.%(s_k)d.merFreq.result
perl /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/caluate_gce.H.pl %(name)s.%(s_k)d.merFreq %(s_k)d > gce.result'''%{'pwd':c_path,'ls':ls,'max_len':max_len,'s_k':s_k,'name':name,'cvg_hight':ch}
	os.write(sd,s1)
	os.close(sd)
if '2' in args.step:
	os.mkdir(c_path + '/02Assemble')
	if args.cfg:
		cfg = args.cfg
	elif '1' in args.step:
		cfg = c_path + '/01Survey/kmer.cfg'
	else:
		pass
	mylen = a_k + 2 
	os.chdir(c_path + '/02Assemble')
	td1 = os.open("sh4ass.sh",os.O_RDWR|os.O_CREAT)
        t1 = '''/PUBLIC/software/DENOVO/pipeline/02.survey/soapDenovoHnew2/grapeHK63 pregraph -s %(cfg)s -K %(a_k)d -R -d 1 -p 26 -o %(a_k)d.%(name)s > %(a_k)d.%(name)s.stp1.log
/PUBLIC/software/DENOVO/pipeline/02.survey/soapDenovoHnew2/grapeHK63 contig -D 1 -M 1 -R -g %(a_k)d.%(name)s > %(a_k)d.%(name)s.stp2.log
/PUBLIC/software/DENOVO/pipeline/02.survey/soapDenovoHnew2/grapeHK63 map -s %(cfg)s -K %(a_k)d -p 26 -g %(a_k)d.%(name)s > %(a_k)d.%(name)s.stp3.log
/PUBLIC/software/DENOVO/pipeline/02.survey/soapDenovoHnew2/grapeHK63 scaff -F 1 -g %(a_k)d.%(name)s -L %(len)d > %(a_k)d.%(name)s.stp4.log
/PUBLIC/software/public/System/Perl-5.18.2/bin/perl /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/stat_coverageV1.7.pl -l 100 -i %(a_k)d.%(name)s.contig >> %(name)s.orign.contig.xls
/PUBLIC/software/public/System/Perl-5.18.2/bin/perl /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/stat_coverageV1.7.pl -l 100 -i %(a_k)d.%(name)s.scafSeq >> %(name)s.scafSeq.xls
#perl /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/cutoff_100.pl %(a_k)d.%(name)s.contig > %(a_k)d.%(name)s.contig.cutoff_100
#perl /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/cutoff_100.pl %(a_k)d.%(name)s.scafSeq > %(a_k)d.%(name)s.scafSeq.cutoff_100
/PUBLIC/software/public/System/Perl-5.18.2/bin/perl /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/my_drawcov.pl %(dir)s/02Assemble/%(a_k)d.%(name)s.bubOnGraph'''%{'cfg':cfg,'a_k':a_k,'name':name,'len':mylen,'dir':c_path}
        os.write(td1,t1)
        td2 = os.open("delete_survey.sh",os.O_RDWR|os.O_CREAT)
        os.write(td2,'rm -r %(dir)s/02Assemble/*.ins %(dir)s/02Assemble/*.41merFreq %(dir)s/02Assemble/*.Arc %(dir)s/02Assemble/*.arc_multi %(dir)s/02Assemble/*.bubOnGraph %(dir)s/02Assemble/*.ContigIndex %(dir)s/02Assemble/*.ctgAlongGap %(dir)s/02Assemble/*.edge* %(dir)s/02Assemble/*.filtBubble %(dir)s/02Assemble/*.gapSeq %(dir)s/02Assemble/*.indexTrack %(dir)s/02Assemble/*.links %(dir)s/02Assemble/*.markOnEdge %(dir)s/02Assemble/*.newContigIndex %(dir)s/02Assemble/*.path %(dir)s/02Assemble/*.peGrads %(dir)s/02Assemble/*.pre* %(dir)s/02Assemble/*.read* %(dir)s/02Assemble/*.red_gap %(dir)s/02Assemble/*.repStruct %(dir)s/02Assemble/*.scaf %(dir)s/02Assemble/*.scaf_* %(dir)s/02Assemble/*.scafSeq_ite %(dir)s/02Assemble/*.split.* %(dir)s/02Assemble/*.Tipinfo_* %(dir)s/02Assemble/*.updated.edge %(dir)s/02Assemble/*.vertex %(dir)s/02Assemble/dot* %(dir)s/02Assemble/freq.stat %(dir)s/02Assemble/gapseqB'%{'dir':c_path})
        os.close(td1)
        os.close(td2)
if '3' in args.step:
	os.mkdir(c_path + '/03Coverage_contig')
	mylen2 = 500
	if '2' not in args.step:
		print('Warning:Please run step2 before step3')
	else:
		os.chdir(c_path + '/03Coverage_contig')
		foud = os.open("ctg4contig.sh",os.O_RDWR|os.O_CREAT)
		fou1 = '''perl /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/ctg_cvg_flt.pl %(dir)s/02Assemble/%(a_k)d.%(name)s.contig $len > %(a_k)d.%(name)s.contig.flt
perl /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/ctg_cvg_stat.pl %(a_k)d.%(name)s.contig.flt %(a_k)d > %(a_k)d.%(name)s.contig.stat
perl /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/ctg_cvg_draw.pl %(a_k)d.%(name)s.contig.stat 100 %(name)s.num.png %(name)s.len.png
perl /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/GCcontent.pl %(dir)s/02Assemble/%(a_k)d.%(name)s.contig %(name)s -c 500 -y 800
perl /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/draw_gedepth_R.pl %(name)s.pos %(name)s.gc.png --gc_range 0:100 --dep_cut 400
perl /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/draw_gedepth_R_scatter.pl %(name)s.pos %(name)s.gc.density.png --gc_range 0:100 --dep_cut 400
/PUBLIC/software/public/System/Perl-5.18.2/bin/perl /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/sh4base_stat.pl %(dir)s/02Assemble/%(a_k)d.%(name)s.contig > %(a_k)d.%(name)s.gc.stat
perl /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/caculate.pl %(dir)s/02Assemble/%(a_k)d.%(name)s.stp2.log %(dir)s/01Survey/Result.xls Result.xls %(max)d'''%{'dir':c_path,'a_k':a_k,'name':name,'max':max_len}
		os.write(foud,fou1)
		os.close(foud)
if '4' in args.step:
	if '123' in args.step or os.path.exists(c_path + '/01Survey') and os.path.exists(c_path + '/03Coverage_contig'):
		os.chdir(c_path)
		fived1 = os.open("sh4report.sh",os.O_RDWR|os.O_CREAT)
		os.write(fived1,"python /PUBLIC/software/DENOVO/pipeline/02.survey/survey/bin/Survey_Report.py ")
		os.close(fived1)
	else:
		print("Warning:Please run step123 before step4")
