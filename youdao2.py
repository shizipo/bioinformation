#!/usr/bin/env python
#!-*- encoding = utf-8 -*-
import requests
from bs4 import BeautifulSoup

def GetMeans(path,file_name):
	f = open( r'%s/%s'%(path,file_name),'r')
	f1 = open(r'%s/R_%s'%(path,file_name),'w')
	m = -1
	for line in f.readlines():
		m += 1
		keyword = line.strip().split('\t')[0]
		r = requests.get("http://www.youdao.com/w/eng/%s/#keyfrom=dict2.index.suggest"%keyword)
		demo = r.text
		soup = BeautifulSoup(demo,"html.parser")
		n = 0 
		if soup.find(id="webTransToggle"):
		    link = soup.find(id="webTransToggle")
#			n += 1
#			if n < 2:
#            print("{:^10}\t{:^30}\t{:^10}".format(m,keyword,str(link.span).replace('<span>','').replace('</span>','')))
			f1.write("{:^10}\t{:^30}\t{:^10}\n".format(m,keyword,str(link.span).replace('<span>','').replace('</span>','')))
			break
	f.close()
	f1.close()
def main():
	path = 'C:/Users/新朝/Desktop/NT.result'
	file_name = 'nt5.xls'
	GetMeans(path,file_name)
main()
