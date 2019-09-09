import numpy as np
import cv2 as cv
import sys
import os
import re

# remember no '/' at each param!
# extract boxes using annotation in yaml opencv format.
# BE CAREFUL with more than 4 vertices coordinators
# YAML file sample:
# %YAML:1.0
# x: !!opencv-matrix
# rows: 4
# cols: 1
# dt: f
# data: [ 205.000000, 204.000000, 462.000000,
#         462.000000]
# y: !!opencv-matrix
# rows: 4
# cols: 1
# dt: f
# data: [ 502.000000, 765.000000, 765.000000,
#         505.000000]

img_path = sys.argv[1]
dst_path = sys.argv[2]
ext = [".jpg", ".png"]

for filename in [f for f in os.listdir(img_path) if f.endswith(tuple(ext))]:
    name_no_extension = filename.split('.')[0]
    yaml_file = open(img_path + '/' + name_no_extension + '_pts.yml', mode='r')
    all_of_it = yaml_file.read()
    all_of_it = all_of_it.replace("\n", " ")
    matchObj = re.findall(r'\[.*?\]', all_of_it)

    x_list = matchObj[0][1:-1].split(',')
    x_list = map(float, x_list)
    x_list = list(map(int, x_list))
    (x1, x2, x3, x4) = x_list
    y_list = matchObj[1][1:-1].split(',')
    y_list = map(float, y_list)
    y_list = list(map(int, y_list))
    (y1, y2, y3, y4) = y_list

    top_left_x = min([x1, x2, x3, x4])
    top_left_y = min([y1, y2, y3, y4])
    bot_right_x = max([x1, x2, x3, x4])
    bot_right_y = max([y1, y2, y3, y4])

    img = cv.imread(img_path + '/' + filename, 1)
    height, width, _ = img.shape

    crop_img = img[top_left_y:bot_right_y + 1, top_left_x:bot_right_x + 1]
    cv.imwrite(dst_path + '/' + filename, crop_img)
