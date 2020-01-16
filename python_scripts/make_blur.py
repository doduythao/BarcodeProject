import matplotlib.pyplot as plt
import cv2 as cv
from scipy import ndimage
import numpy as np
import sys
import os
import random

# remember no '/' at the end of each param!
# 1 for original dir, 2 for input of the model, 3 for label of the model
# to avoid confusing, set 2 is just the duplicate set one of each in 1.
# 3 is the filter after for each kernel in set 2.

org_path = sys.argv[1]
out_path = sys.argv[2]

k1 = cv.imread('kernel/kernel_01.png')
k1 = cv.cvtColor(k1, cv.COLOR_BGR2GRAY)
norm_k1 = k1 / 255.0

k2 = cv.imread('kernel/kernel_02.png')
k2 = cv.cvtColor(k2, cv.COLOR_BGR2GRAY)
norm_k2 = k2 / 255.0


def apply_kernel(file_name, k, norm_f):
    """
    apply kernel base on
    :param norm_f: the kernel, should match with k.
    :param file_name: only based file name, no path.
    :param k: should only in 1-4.
    :return: no need to return, just finish its job
    """
    name_no_ext = file_name.split('.')[0]
    img = cv.imread(org_path + '/' + file_name)
    norm_image = img / 255.0

    result0 = ndimage.convolve(norm_image[:, :, 0], norm_f) / (np.sum(norm_f))
    # result0 = ndimage.convolve(norm_image[:, :, 0], norm_f) / (1.9*np.sum(norm_f))
    result1 = ndimage.convolve(norm_image[:, :, 1], norm_f) / (np.sum(norm_f))
    # result1 = ndimage.convolve(norm_image[:, :, 1], norm_f) / (1.9*np.sum(norm_f))
    result2 = ndimage.convolve(norm_image[:, :, 2], norm_f) / (np.sum(norm_f))
    # result2 = ndimage.convolve(norm_image[:, :, 2], norm_f) / (1.9*np.sum(norm_f))
    result = np.stack((result0, result1, result2), axis=2).astype(np.float32)

    # cv.imwrite(inp_path + '/' + name_no_ext + '-k' + str(k) + '.png', img)
    cv.imwrite(out_path + '/' + file_name, result * 255)


EXT = [".jpg", ".png"]


def main():
    for filename in [f for f in os.listdir(org_path) if f.endswith(tuple(EXT))]:
        ran_num = random.randint(0, 1)
        if ran_num == 0:
            apply_kernel(filename, ran_num, norm_k1)
        else:
            apply_kernel(filename, ran_num, norm_k2)
        


if __name__ == '__main__':
    sys.exit(main())