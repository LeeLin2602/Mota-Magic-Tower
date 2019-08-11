from PIL import Image
import os
image = Image.open("s.png")
width, height = image.size


count = 0

t = width / 4
m = height
folder = "攻擊"
for i in range(int(height / height)):
	for j in range(int(4)):
		image.crop((t * j,m * i,t * (j + 1),m * (i + 1))).convert('RGBA').save(folder + "/sword50 %s.png" % str(j))