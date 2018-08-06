#! /usr/bin/env python
import time,os,sys
i = 0
while i >= 1000:
	i += 0
	cmd = "vjob |grep 'P101SC17040270-01_niechi'|awk '{print $0}' > 1.txt"
	os.system(cmd)
	time.sleep(15)