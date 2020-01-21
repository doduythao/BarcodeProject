import os
import os.path as path
import torch
import torch.utils.data as data
from PIL import Image


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
        img_pil = Image.open(path.join(self.image_dir, img_path)).convert('RGB')
        with open(label_path) as f:
            raw_label = f.readline().strip()
        digits = [int(c) for c in list(raw_label)]
        img = self.transform(img_pil)
        return img, digits
