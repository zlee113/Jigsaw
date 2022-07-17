import cv2
import numpy as np
import os

img = cv2.imread("jigsaw.png", cv2.IMREAD_COLOR)

path = '/nis_home/zclee/zcleeTestbox/MLTesting/jigsaw/indexed_images'

x_min = 0
x_max = 100
y_min = 126
y_max = 226

x_value = 0
y_value = 0



for j in range(8):
	for i in range(38):
		cropped_image = img[y_min:y_max, x_min:x_max]
		img_name = 'y: '+ str(y_value) + ' x: ' + str(x_value) + ".png"
		cv2.imwrite(os.path.join(path, img_name), cropped_image)
		x_min = x_min + 100
		x_max = x_max + 100
		x_value += 1

	y_min = y_min + 100
	y_max = y_max + 100
	y_value += 1
	x_value = 0
	x_min = 0
	x_max = 100

