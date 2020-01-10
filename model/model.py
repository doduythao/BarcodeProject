import glob
import os

import torch
import torch.nn as nn


class Model(nn.Module):
    CHECKPOINT_FILENAME_PATTERN = 'model-{}.pth'

    __constants__ = ['_hidden1', '_hidden2', '_hidden3', '_hidden4', '_hidden5',
                     '_hidden6', '_hidden7', '_hidden8', '_hidden9', '_hidden10',
                     '_features', '_classifier',
                     '_digit2', '_digit3', '_digit4', '_digit5', '_digit6', '_digit7', '_digit8', '_digit9', '_digit10',
                     '_digit11', '_digit12', '_digit13']

    def __init__(self, A):
        self.A = A
        super(Model, self).__init__()
        self._hidden1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=48, kernel_size=5, padding=2),
            nn.BatchNorm2d(num_features=48),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=1),
            nn.Dropout(0.2)
        )
        self._hidden2 = nn.Sequential(
            nn.Conv2d(in_channels=48, out_channels=64, kernel_size=5, padding=2),
            nn.BatchNorm2d(num_features=64),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=1, padding=1),
            nn.Dropout(0.2)
        )
        self._hidden3 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=5, padding=2),
            nn.BatchNorm2d(num_features=128),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=1),
            nn.Dropout(0.2)
        )
        self._hidden4 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=160, kernel_size=5, padding=2),
            nn.BatchNorm2d(num_features=160),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=1, padding=1),
            nn.Dropout(0.2)
        )
        self._hidden5 = nn.Sequential(
            nn.Conv2d(in_channels=160, out_channels=192, kernel_size=5, padding=2),
            nn.BatchNorm2d(num_features=192),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=1),
            nn.Dropout(0.2)
        )
        self._hidden6 = nn.Sequential(
            nn.Conv2d(in_channels=192, out_channels=192, kernel_size=5, padding=2),
            nn.BatchNorm2d(num_features=192),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=1, padding=1),
            nn.Dropout(0.2)
        )
        self._hidden7 = nn.Sequential(
            nn.Conv2d(in_channels=192, out_channels=192, kernel_size=5, padding=2),
            nn.BatchNorm2d(num_features=192),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=1),
            nn.Dropout(0.2)
        )
        self._hidden8 = nn.Sequential(
            nn.Conv2d(in_channels=192, out_channels=192, kernel_size=5, padding=2),
            nn.BatchNorm2d(num_features=192),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=1, padding=1),
            nn.Dropout(0.2)
        )
        self._hidden9 = nn.Sequential(
            nn.Linear(192*A*A, 3072),
            nn.ReLU()
        )
        self._hidden10 = nn.Sequential(
            nn.Linear(3072, 3072),
            nn.ReLU()
        )
        self._digit2 = nn.Sequential(nn.Linear(3072, 20))
        self._digit3 = nn.Sequential(nn.Linear(3072, 20))
        self._digit4 = nn.Sequential(nn.Linear(3072, 20))
        self._digit5 = nn.Sequential(nn.Linear(3072, 20))
        self._digit6 = nn.Sequential(nn.Linear(3072, 20))
        self._digit7 = nn.Sequential(nn.Linear(3072, 20))
        self._digit8 = nn.Sequential(nn.Linear(3072, 10))
        self._digit9 = nn.Sequential(nn.Linear(3072, 10))
        self._digit10 = nn.Sequential(nn.Linear(3072, 10))
        self._digit11 = nn.Sequential(nn.Linear(3072, 10))
        self._digit12 = nn.Sequential(nn.Linear(3072, 10))
        self._digit13 = nn.Sequential(nn.Linear(3072, 10))

    def forward(self, x):
        x = self._hidden1(x)
        x = self._hidden2(x)
        x = self._hidden3(x)
        x = self._hidden4(x)
        x = self._hidden5(x)
        x = self._hidden6(x)
        x = self._hidden7(x)
        x = self._hidden8(x)
        x = x.view(x.size(0), 192*self.A*self.A)
        x = self._hidden9(x)
        x = self._hidden10(x)

        digit2_logits = self._digit2(x)
        digit3_logits = self._digit3(x)
        digit4_logits = self._digit4(x)
        digit5_logits = self._digit5(x)
        digit6_logits = self._digit6(x)
        digit7_logits = self._digit7(x)
        digit8_logits = self._digit8(x)
        digit9_logits = self._digit9(x)
        digit10_logits = self._digit10(x)
        digit11_logits = self._digit11(x)
        digit12_logits = self._digit12(x)
        digit13_logits = self._digit13(x)

        return digit2_logits, digit3_logits, digit4_logits, digit5_logits, digit6_logits, digit7_logits, digit8_logits,\
               digit9_logits, digit10_logits, digit11_logits, digit12_logits, digit13_logits

    def store(self, path_to_dir, step, maximum=5):
        path_to_models = glob.glob(os.path.join(path_to_dir, Model.CHECKPOINT_FILENAME_PATTERN.format('*')))
        if len(path_to_models) == maximum:
            min_step = min([int(path_to_model.split('/')[-1][6:-4]) for path_to_model in path_to_models])
            path_to_min_step_model = os.path.join(path_to_dir, Model.CHECKPOINT_FILENAME_PATTERN.format(min_step))
            os.remove(path_to_min_step_model)

        path_to_checkpoint_file = os.path.join(path_to_dir, Model.CHECKPOINT_FILENAME_PATTERN.format(step))
        torch.save(self.state_dict(), path_to_checkpoint_file)
        return path_to_checkpoint_file

    def restore(self, path_to_checkpoint_file):
        self.load_state_dict(torch.load(path_to_checkpoint_file))
        step = int(path_to_checkpoint_file.split('/')[-1][6:-4])
        return step