import argparse
import os
import time
from datetime import datetime

import numpy as np
import torch
torch.manual_seed(0)

import torch.nn.functional as F
import torch.nn as nn
import torch.optim as optim
import torch.utils.data
from torch.optim.lr_scheduler import StepLR
from torchvision import transforms

from dataset import BarcodeDataset
from evaluator import Evaluator
from model import Model
from model_teacher import TcModel

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--data_dir', default='./data', help='directory to read LMDB files')
parser.add_argument('-l', '--logdir', default='./logs', help='directory to write logs')
parser.add_argument('-r', '--restore_checkpoint', default=None, help='path to restore checkpoint')
parser.add_argument('-rt', '--restore_teacher', default='../resnet50_285/logs/model-1095000.pth', help='teacher path')
parser.add_argument('-bs', '--batch_size', default=32, type=int, help='Default 32')
parser.add_argument('-lr', '--learning_rate', default=1e-2, type=float, help='Default 1e-2')
parser.add_argument('-p', '--patience', default=100, type=int, help='Default 100, set -1 to train infinitely')
parser.add_argument('-ds', '--decay_steps', default=10000, type=int, help='Default 10000')
parser.add_argument('-dr', '--decay_rate', default=0.95, type=float, help='Default 0.95')
parser.add_argument('-tf', '--train_files', default='../model/data/syn_train.txt', help='path to train list file')
parser.add_argument('-vf', '--val_files', default='../model/data/real_full.txt', help='path to val list file')
parser.add_argument('-ba', '--best_acc', default=0.0, type=float, help='Default 0.0')
parser.add_argument('-a', '--alpha', default=0.2, type=float, help='Default 0.2')
parser.add_argument('-t', '--tem', default=10.0, type=float, help='Around 1 - 20')

def loss_fn_kd(outputs, labels, teacher_outputs, alpha, T):
    """
    Compute the knowledge-distillation (KD) loss given outputs, labels.
    "Hyperparameters": temperature and alpha
    NOTE: the KL Divergence for PyTorch comparing the softmaxs of teacher
    and student expects the input tensor to be log probabilities! See Issue #2
    """
    KD_loss = 0
    for i in range(13):
        KD_loss += (nn.KLDivLoss()(F.log_softmax(outputs[i]/T, dim=1),
                                   F.softmax(teacher_outputs[i]/T, dim=1)) * (alpha * T * T) + 
                    F.cross_entropy(outputs[i], labels[i]) * (1. - alpha))
    return KD_loss


def _train(train_img_path, train_txt_path, val_img_path, val_txt_path, path_to_log_dir,
           path_to_restore_checkpoint_file, training_options):
    batch_size = training_options['batch_size']
    initial_learning_rate = training_options['learning_rate']
    initial_patience = training_options['patience']
    num_steps_to_show_loss = 100
    num_steps_to_check = 1000

    step = 0
    patience = initial_patience
    best_accuracy = training_options['best_acc']
    duration = 0.0

    model = Model()
    model.cuda()
    
    teacher = TcModel()
    teacher.cuda()
    teacher.restore(training_options['restore_teacher'])

    transform = transforms.Compose([
                transforms.Resize([285, 285]),
                transforms.ToTensor(),
                transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
            ])
    train_loader = torch.utils.data.DataLoader(BarcodeDataset(training_options['train_files'], train_img_path, train_txt_path, transform),
                                               batch_size=batch_size, shuffle=True,
                                               num_workers=4, pin_memory=True)
    evaluator = Evaluator(training_options['val_files'], val_img_path, val_txt_path)
    optimizer = optim.SGD(model.parameters(), lr=initial_learning_rate, momentum=0.9, weight_decay=0.0005)
    scheduler = StepLR(optimizer, step_size=training_options['decay_steps'], gamma=training_options['decay_rate'])

    if path_to_restore_checkpoint_file is not None:
        assert os.path.isfile(path_to_restore_checkpoint_file), '%s not found' % path_to_restore_checkpoint_file
        step = model.restore(path_to_restore_checkpoint_file)
        scheduler.last_epoch = step
        print('Model restored from file: %s' % path_to_restore_checkpoint_file)

    path_to_losses_npy_file = os.path.join(path_to_log_dir, 'losses.npy')
    if os.path.isfile(path_to_losses_npy_file):
        losses = np.load(path_to_losses_npy_file)
    else:
        losses = np.empty([0], dtype=np.float32)

    while True:
        for batch_idx, (images, digits_labels) in enumerate(train_loader):
            start_time = time.time()
            images, digits_labels = images.cuda(), [digit_label.cuda() for digit_label in digits_labels]
            
            dls = model.train()(images)
            with torch.no_grad():
                tdls = teacher.eval()(images)
            
            loss = loss_fn_kd(dls, digits_labels, tdls, training_options['alpha'], training_options['tem'])
            optimizer.zero_grad()
            loss.backward()

            optimizer.step()
            scheduler.step()
            step += 1
            duration += time.time() - start_time

            if step % num_steps_to_show_loss == 0:
                examples_per_sec = batch_size * num_steps_to_show_loss / duration
                duration = 0.0
                print('=> %s: step %d, loss = %f, learning_rate = %f (%.1f examples/sec)' % (
                    datetime.now(), step, loss.item(), scheduler.get_lr()[0], examples_per_sec))

            if step % num_steps_to_check != 0:
                continue

            losses = np.append(losses, loss.item())
            np.save(path_to_losses_npy_file, losses)

            print('=> Evaluating on validation dataset...')
            accuracy = evaluator.evaluate(model)
            print('==> accuracy = %f, best accuracy %f' % (accuracy, best_accuracy))

            if accuracy > best_accuracy:
                path_to_checkpoint_file = model.store(path_to_log_dir, step=step)
                print('=> Model saved to file: %s' % path_to_checkpoint_file)
                patience = initial_patience
                best_accuracy = accuracy
            else:
                patience -= 1

            print('=> patience = %d' % patience)
            if patience == 0:
                return


def main(args):
    train_img_path ='../model/data/syn_train/img/'
    train_txt_path ='../model/data/syn_train/gt/'
    val_img_path   ='../model/data/real/img/'
    val_txt_path   ='../model/data/real/txt/'
    path_to_log_dir = args.logdir
    path_to_restore_checkpoint_file = args.restore_checkpoint
    training_options = {
        'batch_size': args.batch_size,
        'learning_rate': args.learning_rate,
        'patience': args.patience,
        'decay_steps': args.decay_steps,
        'decay_rate': args.decay_rate,
        'train_files': args.train_files,
        'val_files': args.val_files,
        'best_acc': args.best_acc,
        'restore_teacher': args.restore_teacher,
        'alpha' : args.alpha,
        'tem' :args.tem
    }

    if not os.path.exists(path_to_log_dir):
        os.makedirs(path_to_log_dir)

    print('Start training')
    _train(train_img_path, train_txt_path, val_img_path, val_txt_path, path_to_log_dir,
           path_to_restore_checkpoint_file, training_options)
    print('Done')


if __name__ == '__main__':
    main(parser.parse_args())
