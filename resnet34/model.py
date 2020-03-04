import glob
import os

import torch
import torch.nn as nn
import torchvision.models as models


class Model(nn.Module):
    CHECKPOINT_FILENAME_PATTERN = 'model-{}.pth'

    __constants__ = ['resnet',
                     'fc', 'avgpool',
                     '_digit1', '_digit2', '_digit3', '_digit4', '_digit5', '_digit6', '_digit7', '_digit8', '_digit9',
                     '_digit10', '_digit11', '_digit12', '_digit13']

    def __init__(self):
        super(Model, self).__init__()
        resnet = models.resnet34(pretrained=False)
        modules = list(resnet.children())[:-2]
        self.resnet = nn.Sequential(*modules)
        self.avgpool = nn.AvgPool2d(kernel_size=7, stride=1, padding=0)
        self.fc = nn.Sequential(
            nn.Linear(512*3*3, 4096),
            nn.ReLU()
        )
        
        self._digit1 = nn.Sequential(nn.Linear(4096, 10))
        self._digit2 = nn.Sequential(nn.Linear(4096, 10))
        self._digit3 = nn.Sequential(nn.Linear(4096, 10))
        self._digit4 = nn.Sequential(nn.Linear(4096, 10))
        self._digit5 = nn.Sequential(nn.Linear(4096, 10))
        self._digit6 = nn.Sequential(nn.Linear(4096, 10))
        self._digit7 = nn.Sequential(nn.Linear(4096, 10))
        self._digit8 = nn.Sequential(nn.Linear(4096, 10))
        self._digit9 = nn.Sequential(nn.Linear(4096, 10))
        self._digit10 = nn.Sequential(nn.Linear(4096, 10))
        self._digit11 = nn.Sequential(nn.Linear(4096, 10))
        self._digit12 = nn.Sequential(nn.Linear(4096, 10))
        self._digit13 = nn.Sequential(nn.Linear(4096, 10))

    def forward(self, x):
        x = self.resnet(x)
        x = self.avgpool(x)
#         print(x.shape)
        x = x.reshape(x.size(0), -1)
        x = self.fc(x)

        digit1_logits = self._digit1(x)
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

        return digit1_logits, digit2_logits, digit3_logits, digit4_logits, digit5_logits, digit6_logits, digit7_logits,\
               digit8_logits, digit9_logits, digit10_logits, digit11_logits, digit12_logits, digit13_logits

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
