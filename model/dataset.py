import os
import os.path as path
import numpy as np
import torch
import torch.utils.data as data
from PIL import Image

mapping_indexes = {
    0: [0, 0, 0, 0, 0, 0],
    1: [0, 0, 1, 0, 1, 1],
    2: [0, 0, 1, 1, 0, 1],
    3: [0, 0, 1, 1, 1, 0],
    4: [0, 1, 0, 0, 1, 1],
    5: [0, 1, 1, 0, 0, 1],
    6: [0, 1, 1, 1, 0, 0],
    7: [0, 1, 0, 1, 0, 1],
    8: [0, 1, 0, 1, 1, 0],
    9: [0, 1, 1, 0, 1, 0]
}


def process_label(raw_digits):
    how_encode = mapping_indexes[raw_digits[0]]
    digit2_7s = [raw_digits[i + 1] + 10 if how_encode[i] == 1 else raw_digits[i + 1] for i in range(6)]
    return [raw_digits[0]] + digit2_7s + raw_digits[7:]


class BarcodeDataset(data.Dataset):
    """EAN13 dataset"""

    def __init__(self, image_dir, label_dir, transform=None):
        self.image_dir = image_dir
        self.label_dir = label_dir
        self.transform = transform
        self.file_list = os.listdir(self.image_dir)

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        img_path = self.file_list[idx]
        basename_noext = path.splitext(path.basename(img_path))[0]
        label_path = path.join(self.label_dir, basename_noext + '.txt')
        img_pil = Image.open(path.join(self.image_dir,img_path)).convert('RGB')
        with open(label_path) as f:
            raw_label = f.readline().strip()
        raw_digits = [int(c) for c in list(raw_label)]
        digits = process_label(raw_digits)
        img = self.transform(img_pil)
        return img, digits
