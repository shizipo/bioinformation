import requests
from bs4 import BeautifulSoup
f = open( r'C:/Users/新朝/Desktop/nt1.xls','r')
f1 = open(r'C:/Users/新朝/Desktop/nt1rl.xls','w')
m = -1
for line in f.readlines():
    m += 1
    keyword = line.strip().split('\t')[0]
    r = requests.get("http://www.youdao.com/w/eng/%s/#keyfrom=dict2.index.suggest"%keyword)
    demo = r.text
    soup = BeautifulSoup(demo,"html.parser")
    n = 0 
    for link in soup.find_all('b'):
        n += 1
        if n < 2:
            f1.write("{:^10}\t{:^30}\t{:^10}\n".format(m,keyword,str(link).replace('<b>','').replace('</b>','')))
        break
f.close()
f1.close()
