import cv2
import numpy as np

img1 = cv2.imread('images/Cropped_img340.png')
img2 = cv2.imread('images/Cropped_img39.png')
vis = np.concatenate((img1, img2), axis=0)
cv2.imwrite('out.png', vis)
