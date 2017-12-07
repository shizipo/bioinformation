#! /usr/bin/env python
#! coding = utf-8
import argparse

parser = argparse.ArgumentParser(description="check begin GATC contig , translate reversed and complected sequences")
parser.add_argument('-i','--infile',help='original fasta file',required=True)
parser.add_argument('-o','--outfile',help='outfile ',required=True)
#parser.add_argument('-s','--softname',help='the name of soft',required=True)

argv = parser.parse_args()


def TransRCsequences(file1,file2):
    f1 = open(r'%s'%file1,'r').read()
    f2 = open(r'%s'%file2,'w')
    dict1 = {}
    key = ''
    list = f1.split(">")[1:]
    dict2 = {'G':'C','C':'G','A':'T','T':'A','g':'c','c':'g','a':'t','t':'a','N':'N','n':'n'}
    for i in list:
        id = i.strip().split("\n")[0]
        sequence = ''.join(i.strip().split("\n")[1:])
        if sequence[:4] == 'GATC':
            for base in sequence[::-1]:
                sequence1 = []
                sequence1.append(dict2[base])
                
            f2.write('>%s\n'%id) 
            f2.write('%s\n'%''.join(sequence1))
        else:
            f2.write('>%s\n'%id)
            f2.write('%s\n'%sequence)

def main():
    file1 = argv.infile
    file2 = argv.outfile
    TransRCsequences(file1,file2)
main()
