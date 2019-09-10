import numpy as np
import cv2 as cv
import sys
import os

# remember no '/' at the end of each param!
# extract boxes using mask as mask image (black and white image)

img_path = sys.argv[1]
mask_path = sys.argv[2]
dst_path = sys.argv[3]
ext = [".jpg", ".png"]

for filename in [f for f in os.listdir(mask_path) if f.endswith(tuple(ext))]:
    name_no_extension = filename.split('.')[0]
    mask = cv.imread(mask_path + '/' + filename, 0)
    img = cv.imread(img_path + '/' + filename, 1)
    _, thresh = cv.threshold(mask, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, 1, 2)
    height, width, _ = img.shape

    for i in range(len(contours)):
        x, y, w, h = cv.boundingRect(contours[i])
        up = y - int(h * 0.05) if (y - int(h * 0.05)) >= 0 else y
        down = y + int(h * 1.05) if (y + int(h * 1.05)) <= height else y + int(h)
        left = x - int(w * 0.05) if (x - int(w * 0.05)) >= 0 else x
        right = x + int(w * 1.05) if (x + int(w * 1.05)) <= width else x + int(w)

        crop_img = img[up:down, left:right]
        cv.imwrite(dst_path + '/' + name_no_extension + '-' + str(i) + '.png', crop_img)
