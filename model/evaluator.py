import torch
import torch.utils.data
from torchvision import transforms
from dataset import Dataset
from util import get_digit1


class Evaluator(object):
    def __init__(self, path_to_lmdb_dir):
        transform = transforms.Compose([
            transforms.CenterCrop([54, 54]),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ])
        self._loader = torch.utils.data.DataLoader(Dataset(path_to_lmdb_dir, transform), batch_size=128, shuffle=False)

    def evaluate(self, model):
        num_correct = 0

        with torch.no_grad():
            for batch_idx, (images, digits_labels) in enumerate(self._loader):
                images, digits_labels = images.cuda(), [digit_labels.cuda() for digit_labels in digits_labels]
                digit2_logits, digit3_logits, digit4_logits, digit5_logits, digit6_logits, digit7_logits, \
                digit8_logits, digit9_logits, digit10_logits, digit11_logits, digit12_logits, digit13_logits = \
                    model.eval()(
                        images)

                digit1_logits = get_digit1(digit2_logits, digit3_logits, digit4_logits, digit5_logits, digit6_logits,
                                           digit7_logits)

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

        accuracy = num_correct.item() / len(self._loader.dataset)
        return accuracy
