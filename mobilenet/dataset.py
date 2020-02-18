import os
import os.path as path
import torch
import torch.utils.data as data
from PIL import Image


class BarcodeDataset(data.Dataset):
    """EAN13 dataset"""

    def __init__(self, file_list_path, image_dir, label_dir, transform=None):
        self.image_dir = image_dir
        self.label_dir = label_dir
        self.transform = transform
        with open(file_list_path) as f:
            content = f.readlines()
        self.file_list = [x.strip() for x in content]

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        img_path = self.file_list[idx]
        basename_noext = path.splitext(img_path)[0]
        label_path = path.join(self.label_dir, basename_noext + '.txt')
        
        img_pil = Image.open(path.join(self.image_dir, img_path)).convert('RGB')
        width, height = img_pil.size
        max_edge = max(width, height)
        new_im = Image.new('RGB', (max_edge, max_edge), (255, 255, 255))
        new_im.paste(img_pil, (int((max_edge-width)/2), int((max_edge-height)/2)))
        
        with open(label_path) as f:
            raw_label = f.readline().strip()
        if len(raw_label)!=13:
            print('SHIT')
        digits = [int(c) for c in list(raw_label)]
        img = self.transform(new_im)
        return img, digits
