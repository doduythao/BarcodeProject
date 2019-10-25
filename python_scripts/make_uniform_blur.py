import matplotlib.pyplot as plt
import cv2 as cv
from scipy import ndimage
import numpy as np
import sys
import os
import random
import multiprocessing

# remember no '/' at the end of each param!
# 1 for original dir, 2 for input of the model, 3 for label of the model
# to avoid confusing, set 2 is just the duplicate set one of each in 1.
# 3 is the filter after for each kernel in set 2.

org_path = sys.argv[1]
# inp_path = sys.argv[2]
out_path = sys.argv[3]

k1 = cv.imread('../matlab/uniform_kernel/kernel_01.png')
k1 = cv.cvtColor(k1, cv.COLOR_BGR2GRAY)
norm_k1 = k1 / 255.0

k2 = cv.imread('../matlab/uniform_kernel/kernel_02.png')
k2 = cv.cvtColor(k2, cv.COLOR_BGR2GRAY)
norm_k2 = k2 / 255.0

k3 = cv.imread('../matlab/uniform_kernel/kernel_03.png')
k3 = cv.cvtColor(k3, cv.COLOR_BGR2GRAY)
norm_k3 = k3 / 255.0

k4 = cv.imread('../matlab/uniform_kernel/kernel_04.png')
k4 = cv.cvtColor(k4, cv.COLOR_BGR2GRAY)
norm_k4 = k4 / 255.0


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
    # norm_image = cv.normalize(img, None, alpha=-0.1, beta=1.8, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
    # b, g, r = cv.split(norm_image)
    # np.savetxt(open("../dataset/norm_f_b.txt", "a"), b)
    # np.savetxt(open("../dataset/norm_f_g.txt", "a"), g)
    # np.savetxt(open("../dataset/norm_f_r.txt", "a"), r)
    # print(norm_image.shape)

    result0 = ndimage.convolve(norm_image[:, :, 0], norm_f) / (np.sum(norm_f))
    # result0 = ndimage.convolve(norm_image[:, :, 0], norm_f) / (1.9*np.sum(norm_f))
    result1 = ndimage.convolve(norm_image[:, :, 1], norm_f) / (np.sum(norm_f))
    # result1 = ndimage.convolve(norm_image[:, :, 1], norm_f) / (1.9*np.sum(norm_f))
    result2 = ndimage.convolve(norm_image[:, :, 2], norm_f) / (np.sum(norm_f))
    # result2 = ndimage.convolve(norm_image[:, :, 2], norm_f) / (1.9*np.sum(norm_f))
    result = np.stack((result0, result1, result2), axis=2).astype(np.float32)

    # cv.imwrite(inp_path + '/' + name_no_ext + '-k' + str(k) + '.png', img)
    cv.imwrite(out_path + '/' + name_no_ext + '-k' + str(k) + '.png', result * 255)


# result_rgb = cv.cvtColor(result, cv.COLOR_BGR2RGB)
# plt.imshow(result_rgb)
# plt.show()


EXT = [".jpg", ".png"]


def main():
    # pool = multiprocessing.Pool()
    # for filename in [f for f in os.listdir(org_path) if f.endswith(tuple(EXT))]:
    #     pool.apply_async(apply_kernel, [filename, 1, norm_k1])
    #     pool.apply_async(apply_kernel, [filename, 2, norm_k2])
    #     pool.apply_async(apply_kernel, [filename, 3, norm_k3])
    #     pool.apply_async(apply_kernel, [filename, 4, norm_k4])
    # pool.close()
    # pool.join()
    for filename in [f for f in os.listdir(org_path) if f.endswith(tuple(EXT))]:
        ran_num = random.randint(0, 2)
        if ran_num == 0:
            apply_kernel(filename, ran_num, norm_k1)
        elif ran_num == 1:
            apply_kernel(filename, ran_num, norm_k2)
        else:
            apply_kernel(filename, ran_num, norm_k3)


if __name__ == '__main__':
    sys.exit(main())
