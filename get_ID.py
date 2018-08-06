f = open(r'C:\Users\新朝\Desktop\1.txt','r')
j = []
for i in f.readlines():
        h = i.strip().split()[0]
        print (h,end=' '),
