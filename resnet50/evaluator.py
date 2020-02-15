import torch
import torch.utils.data
from torchvision import transforms
from dataset import BarcodeDataset


class Evaluator(object):
    def __init__(self, img_path, txt_path):
        transform = transforms.Compose([
            transforms.Resize([285, 285]),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ])
        self._loader = torch.utils.data.DataLoader(BarcodeDataset(img_path, txt_path, transform), batch_size=128, shuffle=False)

    def evaluate(self, model):
        num_correct, correct_1, correct_2, correct_3, correct_4, correct_5, correct_6, correct_7, correct_8, correct_9, correct_10, correct_11, correct_12, correct_13 = (0,)*14
        num_correct_wthout1 = 0

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
                num_correct_wthout1 += (
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
                
                correct_1 += digit1_prediction.eq(digits_labels[0]).cpu().sum()
                correct_2 += digit2_prediction.eq(digits_labels[1]).cpu().sum()
                correct_3 += digit3_prediction.eq(digits_labels[2]).cpu().sum()
                correct_4 += digit4_prediction.eq(digits_labels[3]).cpu().sum()
                correct_5 += digit5_prediction.eq(digits_labels[4]).cpu().sum()
                correct_6 += digit6_prediction.eq(digits_labels[5]).cpu().sum()
                correct_7 += digit7_prediction.eq(digits_labels[6]).cpu().sum()
                correct_8 += digit8_prediction.eq(digits_labels[7]).cpu().sum()
                correct_9 += digit9_prediction.eq(digits_labels[8]).cpu().sum()
                correct_10 += digit10_prediction.eq(digits_labels[9]).cpu().sum()
                correct_11 += digit11_prediction.eq(digits_labels[10]).cpu().sum()
                correct_12 += digit12_prediction.eq(digits_labels[11]).cpu().sum()
                correct_13 += digit13_prediction.eq(digits_labels[12]).cpu().sum()
                
        dataset_size = len(self._loader.dataset)

        accuracy = num_correct.item() / dataset_size
        
        print('1: ', correct_1.item()/dataset_size, ', ',
              '2: ', correct_2.item()/dataset_size, ', ',
              '3: ', correct_3.item()/dataset_size, ', ',
              '4: ', correct_4.item()/dataset_size, ', ',
              '5: ', correct_5.item()/dataset_size, ', ',
              '6: ', correct_6.item()/dataset_size, ', ',
              '7: ', correct_7.item()/dataset_size, ', ',
              '8: ', correct_8.item()/dataset_size, ', ',
              '9: ', correct_9.item()/dataset_size, ', ',
              '10: ', correct_10.item()/dataset_size, ', ',
              '11: ', correct_11.item()/dataset_size, ', ',
              '12: ', correct_12.item()/dataset_size, ', ',
              '13: ', correct_13.item()/dataset_size
             )
        print('without-1 acc: ', num_correct_wthout1.item()/dataset_size)
        
        return accuracy
