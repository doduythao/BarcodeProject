import argparse
import numpy as np
import torch
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data
from torch.optim.lr_scheduler import StepLR
from torchvision import transforms
from dataset import BarcodeDataset
from model import Model
import time

def checksum(sequence):
    total = 0
    for i in range(13):
        if i%2 == 0:
            total += int(sequence[i])
        else:
            total += int(sequence[i])*3
    return total%10==0

def make_combination(input_array):
    abin = ['']
    for i in range(13):
        if isinstance(input_array[i], list):
            abin = [j+str(input_array[i][0]) for j in abin] + [j+str(input_array[i][1]) for j in abin]
        else:
            abin = [j+str(input_array[i]) for j in abin]
    return abin

class Evaluator(object):
    def __init__(self, file_list_path, img_path, txt_path):
        transform = transforms.Compose([
            transforms.Resize([285, 285]),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ])
        self._loader = torch.utils.data.DataLoader(BarcodeDataset(file_list_path, img_path, txt_path, transform), batch_size=1, shuffle=False)

    def evaluate(self, model, threshold):
        num_correct = 0

        with torch.no_grad():
            for batch_idx, (images, digits_labels) in enumerate(self._loader):
                digit1_logits, digit2_logits, digit3_logits, digit4_logits, digit5_logits, digit6_logits, digit7_logits, \
                digit8_logits, digit9_logits, digit10_logits, digit11_logits, digit12_logits, digit13_logits = \
                    model.eval()(images)
                
                digit1_prob = F.softmax(digit1_logits, 1)[0].numpy()
                digit2_prob = F.softmax(digit2_logits, 1)[0].numpy()
                digit3_prob = F.softmax(digit3_logits, 1)[0].numpy()
                digit4_prob = F.softmax(digit4_logits, 1)[0].numpy()
                digit5_prob = F.softmax(digit5_logits, 1)[0].numpy()
                digit6_prob = F.softmax(digit6_logits, 1)[0].numpy()
                digit7_prob = F.softmax(digit7_logits, 1)[0].numpy()
                digit8_prob = F.softmax(digit8_logits, 1)[0].numpy()
                digit9_prob = F.softmax(digit9_logits, 1)[0].numpy()
                digit10_prob = F.softmax(digit10_logits, 1)[0].numpy()
                digit11_prob = F.softmax(digit11_logits, 1)[0].numpy()
                digit12_prob = F.softmax(digit12_logits, 1)[0].numpy()
                digit13_prob = F.softmax(digit13_logits, 1)[0].numpy()
                
                digit1_2max_idx = digit1_prob.argsort()[-2:][::-1]
                digit2_2max_idx = digit2_prob.argsort()[-2:][::-1]
                digit3_2max_idx = digit3_prob.argsort()[-2:][::-1]
                digit4_2max_idx = digit4_prob.argsort()[-2:][::-1]
                digit5_2max_idx = digit5_prob.argsort()[-2:][::-1]
                digit6_2max_idx = digit6_prob.argsort()[-2:][::-1]
                digit7_2max_idx = digit7_prob.argsort()[-2:][::-1]
                digit8_2max_idx = digit8_prob.argsort()[-2:][::-1]
                digit9_2max_idx = digit9_prob.argsort()[-2:][::-1]
                digit10_2max_idx = digit10_prob.argsort()[-2:][::-1]
                digit11_2max_idx = digit11_prob.argsort()[-2:][::-1]
                digit12_2max_idx = digit12_prob.argsort()[-2:][::-1]
                digit13_2max_idx = digit13_prob.argsort()[-2:][::-1]
                
                digits_2max_idx = [digit1_2max_idx, digit2_2max_idx, digit3_2max_idx, digit4_2max_idx, digit5_2max_idx, digit6_2max_idx, digit7_2max_idx, digit8_2max_idx, digit9_2max_idx, digit10_2max_idx, digit11_2max_idx, digit12_2max_idx, digit13_2max_idx]
                
                gaps = [digit1_prob[digit1_2max_idx[0]]  -digit1_prob[digit1_2max_idx[1]],
                        digit2_prob[digit2_2max_idx[0]]  -digit2_prob[digit2_2max_idx[1]],
                        digit3_prob[digit3_2max_idx[0]]  -digit3_prob[digit3_2max_idx[1]],
                        digit4_prob[digit4_2max_idx[0]]  -digit4_prob[digit4_2max_idx[1]],
                        digit5_prob[digit5_2max_idx[0]]  -digit5_prob[digit5_2max_idx[1]],
                        digit6_prob[digit6_2max_idx[0]]  -digit6_prob[digit6_2max_idx[1]],
                        digit7_prob[digit7_2max_idx[0]]  -digit7_prob[digit7_2max_idx[1]],
                        digit8_prob[digit8_2max_idx[0]]  -digit8_prob[digit8_2max_idx[1]],
                        digit9_prob[digit9_2max_idx[0]]  -digit9_prob[digit9_2max_idx[1]],
                        digit10_prob[digit10_2max_idx[0]]-digit10_prob[digit10_2max_idx[1]],
                        digit11_prob[digit11_2max_idx[0]]-digit11_prob[digit11_2max_idx[1]],
                        digit12_prob[digit12_2max_idx[0]]-digit12_prob[digit12_2max_idx[1]],
                        digit13_prob[digit13_2max_idx[0]]-digit13_prob[digit13_2max_idx[1]]]
                picked_digits = []
                for i in range(13):
                    if gaps[i]<=threshold:
                        picked_digits.append(list(digits_2max_idx[i]))
                    else:
                        picked_digits.append(digits_2max_idx[i][0])
                all_combinations = make_combination(picked_digits)
                predicted_sequence = all_combinations[0]
                for combin in all_combinations:
                    if checksum(combin):
                        predicted_sequence = combin
                        break
                label_digits = [each_digit.numpy()[0] for each_digit in digits_labels]
                label_sequence = ''.join(map(str, label_digits))
                if label_sequence == predicted_sequence:
                    num_correct+=1

        dataset_size = len(self._loader.dataset)
        accuracy = num_correct / dataset_size
        return accuracy


parser = argparse.ArgumentParser()

parser.add_argument('-l', '--logdir', default='./logs', help='directory to write logs')
parser.add_argument('-r', '--restore_checkpoint', default=None,
                    help='path to restore checkpoint, e.g. ./logs/model-100.pth')
parser.add_argument('-vf', '--val_files', default='../model/data/real_val.txt', help='directory to validation list file')
parser.add_argument('-th', '--threshold', default=0.75, type=float, help='Default 0.75')

def main(args):
    val_img_path   ='../model/data/real/img/'
    val_txt_path   ='../model/data/real/txt/'
    path_to_log_dir = args.logdir
    path_to_restore_checkpoint_file = args.restore_checkpoint

    model = Model()
    model.restore(path_to_restore_checkpoint_file)
    
    print('Start evaluating')
    
    evaluator = Evaluator(args.val_files, val_img_path, val_txt_path)
    start_time = time.time()
    accuracy = evaluator.evaluate(model, args.threshold)
    print('duration: ', time.time() - start_time)
    print('accuracy: ', accuracy)


if __name__ == '__main__':
    main(parser.parse_args())