import itchat
import math
import PIL.Image as Image
import os

itchat.auto_login()
friends = itchat.get_friends(update=True)[0:]
user = friends[0]["UserName"]

num = 0
for i in friends:
    img = itchat.get_head_img(userName=i["UserName"])
    fileImage = open('C:/Users/Administrator/Desktop/weichat' + "/" + str(num) + ".jpg",'wb')
    fileImage.write(img)
    fileImage.close()
    num += 1

ls = os.listdir('C:/Users/Administrator/Desktop/weichat')
each_size = int(math.sqrt(float(1280*1280)/len(ls)))
lines = int(1280/each_size)
image = Image.new('RGBA', (1280, 1280))
x = 0
y = 0
for i in range(0,len(ls)+1):
    try:
        img = Image.open('C:/Users/Administrator/Desktop/weichat' + "/" + str(i) + ".jpg")
    except IOError:
        print("Error")
    else:
        img = img.resize((each_size, each_size), Image.ANTIALIAS)
        image.paste(img, (x * each_size, y * each_size))
        x += 1
        if x == lines:
            x = 0
            y += 1
image.save('C:/Users/Administrator/Desktop/weichat' + "/" + "all.png")
itchat.send_image('C:/Users/Administrator/Desktop/weichat' + "/" + "all.png", 'filehelper')