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
        num_false   = 0

        with torch.no_grad():
            for batch_idx, (images, digits_labels) in enumerate(self._loader):
                images = images.cuda()
                dls = model.eval()(images)
                dpbs = [F.softmax(dl, 1)[0].cpu().numpy() for dl in dls]
                dmaxidxs = [dpb.argsort()[-2:][::-1] for dpb in dpbs]
                gaps = [dpbs[i][dmaxidxs[i][0]] - dpbs[i][dmaxidxs[i][1]] for i in range(13)]
                chosen_maxidxs = np.argsort(gaps)[:threshold]
                picked_digits = []
                for i in range(13):
                    if i in chosen_maxidxs:
                        picked_digits.append(list(dmaxidxs[i]))
                    else:
                        picked_digits.append(dmaxidxs[i][0])

                all_combinations = make_combination(picked_digits)
                checksum_checked = False
                predicted_sequence = all_combinations[0]
                for combin in all_combinations:
                    if checksum(combin):
                        predicted_sequence = combin
                        checksum_checked = True
                        break

                if checksum_checked:
                    label_digits = [each_digit.numpy()[0] for each_digit in digits_labels]
                    label_sequence = ''.join(map(str, label_digits))
                    if label_sequence == predicted_sequence:
                        num_correct+=1
                    else:
                        num_false+=1
                    
        print('false prediction:', num_false)
        dataset_size = len(self._loader.dataset)
        accuracy = num_correct / dataset_size
        return accuracy


parser = argparse.ArgumentParser()

parser.add_argument('-l', '--logdir', default='./logs', help='directory to write logs')
parser.add_argument('-r', '--restore_checkpoint', default=None,
                    help='path to restore checkpoint, e.g. ./logs/model-100.pth')
parser.add_argument('-vf', '--val_files', default='../model/data/real_val.txt', help='directory to validation list file')
parser.add_argument('-th', '--threshold', default=2, type=int, help='Default 2')

def main(args):
    val_img_path   ='../model/data/real/img/'
    val_txt_path   ='../model/data/real/txt/'
    path_to_log_dir = args.logdir
    path_to_restore_checkpoint_file = args.restore_checkpoint

    model = Model()
    model.cuda()
    model.restore(path_to_restore_checkpoint_file)
    
    print('Start evaluating')
    
    evaluator = Evaluator(args.val_files, val_img_path, val_txt_path)
    start_time = time.time()
    accuracy = evaluator.evaluate(model, args.threshold)
    print('duration: ', time.time() - start_time)
    print('accuracy: ', accuracy)


if __name__ == '__main__':
    main(parser.parse_args())