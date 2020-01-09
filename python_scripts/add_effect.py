import os
import sys
import random
from PIL import Image
import numpy as np
from skimage.util import random_noise
import cv2

EXT = [".jpg", ".png"]

# remember '/' at the end of each param!
inp_path = sys.argv[1]
out_path = sys.argv[2]
if not os.path.exists(out_path):
    os.makedirs(out_path)

effect = sys.argv[3]


# noise, dark: down contrast, light: up brightness, patch:


def apply_effect(im_arr):
    if effect == 'noise':
        v = random.randint(2, 6) / 100
        noise_img = random_noise(im_arr, mode='gaussian', var=v ** 2)
        noise_img = (255 * noise_img).astype(np.uint8)
        return noise_img
    elif effect == 'dark':
        v = random.randint(65, 95) / 100
        adjusted = cv2.convertScaleAbs(im_arr, alpha=v, beta=0)
        return adjusted
    elif effect == 'light':
        v = random.randint(20, 65)
        adjusted = cv2.convertScaleAbs(im_arr, alpha=1, beta=v)
        return adjusted
    elif effect == 'patch':
        new_im = im_arr
        height, width, _ = im_arr.shape
        patch_height = int(height * random.randint(20, 50) / 100)
        patch_width = int(width * random.randint(25, 45) / 100)
        p_x = int(height * random.randint(0, 50) / 100)
        p_y = int(width * random.randint(0, 50) / 100)
        new_im[p_x:p_x + patch_height, p_y:p_y + patch_width, :] = 0
        return new_im


def main():
    file_list = [f for f in os.listdir(inp_path) if f.endswith(tuple(EXT))]
    for filename in file_list:
        im = Image.open(inp_path + filename)
        im_arr = np.array(im)
        out_im = Image.fromarray(apply_effect(im_arr))
        out_im.save(out_path + filename)


if __name__ == '__main__':
    sys.exit(main())
