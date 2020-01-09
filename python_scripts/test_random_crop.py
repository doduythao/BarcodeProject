import os
import sys
from PIL import Image
import numpy as np

EXT = [".jpg", ".png"]

# remember '/' at the end of each param!
# make sure you know the size of the input. (should be more than cropping size)
CROPPING_SIZE = 256
inp_path = sys.argv[1]
out_path = sys.argv[2]
if not os.path.exists(out_path):
    os.makedirs(out_path)


def crop(im_arr, corner):
    height, width, _ = im_arr.shape
    if corner == 1:
        p_x = 0
        p_y = width - CROPPING_SIZE
    elif corner == 2:
        p_x = height - CROPPING_SIZE
        p_y = 0
    elif corner == 3:
        p_x = 0
        p_y = 0
    elif corner == 4:
        p_x = height - CROPPING_SIZE
        p_y = width - CROPPING_SIZE
    return im_arr[p_x:p_x + CROPPING_SIZE, p_y:p_y + CROPPING_SIZE, :]


def main():
    file_list = [f for f in os.listdir(inp_path) if f.endswith(tuple(EXT))]
    for filename in file_list:
        im = Image.open(inp_path + filename)
        im_arr = np.array(im)
        out_im1 = Image.fromarray(crop(im_arr, 1))
        out_im2 = Image.fromarray(crop(im_arr, 2))
        out_im3 = Image.fromarray(crop(im_arr, 3))
        out_im4 = Image.fromarray(crop(im_arr, 4))
        out_im1.save(out_path + filename.split('.')[0]+"_1.png")
        out_im2.save(out_path + filename.split('.')[0]+"_2.png")
        out_im3.save(out_path + filename.split('.')[0]+"_3.png")
        out_im4.save(out_path + filename.split('.')[0]+"_4.png")


if __name__ == '__main__':
    sys.exit(main())
