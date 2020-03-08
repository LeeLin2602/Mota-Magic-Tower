from PIL import Image
import os
image = Image.open("blue_god.png")
width, height = image.size


count = 0

t = width / 3
m = height / 1
folder = ""
for i in range(int(height / m)):
	for j in range(int(4)):
		image.crop((t * j,m * i,t * (j + 1),m * (i + 1))).convert('RGBA').save(folder + "blue_god%s %s.png" % (str(i),str(j)))