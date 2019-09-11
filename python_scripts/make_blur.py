import matplotlib.pyplot as plt
import cv2 as cv
import scipy
import matplotlib.image as mpimg

img = cv.imread('../dataset/text_01.png', 0)
norm_image = cv.normalize(img, None, alpha=-0.1, beta=1.8, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)

f = cv.imread('../matlab/uniform_kernel/kernel_01.png')

result = scipy.ndimage.convolve(img, f, mode='nearest')