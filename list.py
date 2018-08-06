f = open(r'C:\Users\新朝\Desktop\1.txt','r')
for i in f.readlines():
	laneID = int(i.strip().split()[0])
	insertsize = i.strip().split()[1]
	name_lib = i.strip().split()[2]
	print('%s-%s_L%d\t%s'%(name_lib.split('-')[0],name_lib.split('-')[1],laneID,insertsize[:-2]))
