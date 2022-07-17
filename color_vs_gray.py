from scipy.ndimage import filters
from PIL import Image, ImageChops
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import glob


def load_test_images():
        images = [] 
        gray_images = []

        x_val = 0
        y_val = 1
        for j in range(8):
                for i in range(38):
                        img_name = 'images_2/y: '+ str(y_val) + ' x: ' + str(x_val) + ".png"
                        images.append(cv2.imread(img_name))
                        x_val += 1
                y_val += 1
                x_val = 0
        for image in range(len(images)):
                gray = cv2.cvtColor(images[image], cv2.COLOR_BGR2GRAY)
                gray_images.append(gray)
        return images, gray_images


def get_min_color(images):
    color = []
    cmp_img = []
    min_dif = []

    for pic in range(len(images)):
        img1 = images[pic]
        for image in range(len(images)):
            c = 0
            for y in range(100):
                comp = [ [img1[y, 99, 0], img1[y, 99, 1], img1[y, 99, 2]], [images[image][y, 0, 0], images[image][y, 0, 1], images[image][y, 0, 2]] ]
                color.append(comp)
            for e in range(len(color)):
                c += abs(int(color[e][0][0]) - int(color[e][1][0])) + abs(int(color[e][0][1]) - int(color[e][1][1])) + abs(int(color[e][0][2]) - int(color[e][1][2]))
            cmp_img.append(c/300)
            color.clear()
        min_dif.append(min(cmp_img))
        cmp_img.clear()
    return min_dif


def get_min_gray(gray_images):
    color = []
    cmp_img = []
    min_dif = []

    for pic in range(len(images)):
        img1 = gray_images[pic]
        for image in range(len(images)):
            c = 0
            for y in range(100):
                comp = [ img1[y, 99], gray_images[image] [y, 0] ]
                color.append(comp)
            for e in range(len(color)):
                c = c + abs(int(color[e][0]) - int(color[e][1]))
            cmp_img.append(c/100)
            color.clear()
        min_dif.append(min(cmp_img))
        cmp_img.clear()
    return min_dif



def plot(x, y, title):

    fig, ax = plt.subplots()
    ax.set_xlabel('Image')
    ax.set_ylabel('Minimum Average Pixel Difference')
    ax.set_title(title)
    ax.plot(x, y)
    plt.show()



images, gray_images = load_test_images()
c_min_dif = get_min_color(images)
g_min_dif = get_min_gray(gray_images)
print(len(c_min_dif), len(g_min_dif))
x = []
for it in range(len(c_min_dif)):
    x.append(it) 

#x = np.array[0, len(images)-1]
plot(x, c_min_dif, 'Color Image')
plot(x, g_min_dif, 'Grayscaled Image')
