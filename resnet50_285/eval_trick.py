import argparse
import os
import time
from datetime import datetime

import numpy as np
import torch

import torch.nn.functional
import torch.optim as optim
import torch.utils.data
from torch.optim.lr_scheduler import StepLR
from torchvision import transforms

from dataset import BarcodeDataset
from model import Model


class Evaluator(object):
    def __init__(self, file_list_path, img_path, txt_path):
        transform = transforms.Compose([
            transforms.Resize([285, 285]),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ])
        self._loader = torch.utils.data.DataLoader(BarcodeDataset(file_list_path, img_path, txt_path, transform), batch_size=1, shuffle=False)

    def evaluate(self, model):
        num_correct = 0

        with torch.no_grad():
            for batch_idx, (images, digits_labels) in enumerate(self._loader):
                images, digits_labels = images.cuda(), [digit_labels.cuda() for digit_labels in digits_labels]
                digit1_logits, digit2_logits, digit3_logits, digit4_logits, digit5_logits, digit6_logits, digit7_logits, \
                digit8_logits, digit9_logits, digit10_logits, digit11_logits, digit12_logits, digit13_logits = \
                    model.eval()(images)
                
                digit1_prediction = digit1_logits.max(1)[1]
                digit2_prediction = digit2_logits.max(1)[1]
                digit3_prediction = digit3_logits.max(1)[1]
                digit4_prediction = digit4_logits.max(1)[1]
                digit5_prediction = digit5_logits.max(1)[1]
                digit6_prediction = digit6_logits.max(1)[1]
                digit7_prediction = digit7_logits.max(1)[1]
                digit8_prediction = digit8_logits.max(1)[1]
                digit9_prediction = digit9_logits.max(1)[1]
                digit10_prediction = digit10_logits.max(1)[1]
                digit11_prediction = digit11_logits.max(1)[1]
                digit12_prediction = digit12_logits.max(1)[1]
                digit13_prediction = digit13_logits.max(1)[1]

                num_correct += (digit1_prediction.eq(digits_labels[0]) &
                                digit2_prediction.eq(digits_labels[1]) &
                                digit3_prediction.eq(digits_labels[2]) &
                                digit4_prediction.eq(digits_labels[3]) &
                                digit5_prediction.eq(digits_labels[4]) &
                                digit6_prediction.eq(digits_labels[5]) &
                                digit7_prediction.eq(digits_labels[6]) &
                                digit8_prediction.eq(digits_labels[7]) &
                                digit9_prediction.eq(digits_labels[8]) &
                                digit10_prediction.eq(digits_labels[9]) &
                                digit11_prediction.eq(digits_labels[10]) &
                                digit12_prediction.eq(digits_labels[11]) &
                                digit13_prediction.eq(digits_labels[12])).cpu().sum()
                
        dataset_size = len(self._loader.dataset)
        accuracy = num_correct.item() / dataset_size
        return accuracy


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--data_dir', default='./data', help='directory to read LMDB files')
parser.add_argument('-l', '--logdir', default='./logs', help='directory to write logs')
parser.add_argument('-r', '--restore_checkpoint', default=None,
                    help='path to restore checkpoint, e.g. ./logs/model-100.pth')
parser.add_argument('-bs', '--batch_size', default=32, type=int, help='Default 32')
parser.add_argument('-lr', '--learning_rate', default=1e-2, type=float, help='Default 1e-2')
parser.add_argument('-p', '--patience', default=100, type=int, help='Default 100, set -1 to train infinitely')
parser.add_argument('-ds', '--decay_steps', default=10000, type=int, help='Default 10000')
parser.add_argument('-dr', '--decay_rate', default=0.9, type=float, help='Default 0.9')


def main(args):
    val_img_path   ='../model/data/syn_train/img/'
    val_txt_path   ='../model/data/syn_train/gt/'
    path_to_log_dir = args.logdir
    path_to_restore_checkpoint_file = args.restore_checkpoint
    training_options = {
        'batch_size': args.batch_size,
        'learning_rate': args.learning_rate,
        'patience': args.patience,
        'decay_steps': args.decay_steps,
        'decay_rate': args.decay_rate
    }

    model = Model()
    model.cuda()
    model.restore(path_to_restore_checkpoint_file)
    
    print('Start evaluating')
    
    evaluator = Evaluator(val_img_path, val_txt_path)
    accuracy = evaluator.evaluate(model)
    print('accuracy: ', accuracy)


if __name__ == '__main__':
    main(parser.parse_args())
