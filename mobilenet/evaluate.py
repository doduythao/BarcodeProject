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
from evaluator import Evaluator
from model import Model

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
