import numpy as np
import torch
import torch.nn.functional as F

mapping_indexes = {
    0: [0, 0, 0, 0, 0, 0],
    1: [0, 0, 1, 0, 1, 1],
    2: [0, 0, 1, 1, 0, 1],
    3: [0, 0, 1, 1, 1, 0],
    4: [0, 1, 0, 0, 1, 1],
    5: [0, 1, 1, 0, 0, 1],
    6: [0, 1, 1, 1, 0, 0],
    7: [0, 1, 0, 1, 0, 1],
    8: [0, 1, 0, 1, 1, 0],
    9: [0, 1, 1, 0, 1, 0]
}


def get_digit1(digit2_logits, digit3_logits, digit4_logits, digit5_logits, digit6_logits, digit7_logits):
    # cẩn thận chỗ axis của sum. phải test kĩ lại khi ráp vô chạy thật, chỗ stack cũng phải cẩn thận.
    n_digit2_logits = F.softmax(digit2_logits, 1)
    n_digit3_logits = F.softmax(digit3_logits, 1)
    n_digit4_logits = F.softmax(digit4_logits, 1)
    n_digit5_logits = F.softmax(digit5_logits, 1)
    n_digit6_logits = F.softmax(digit6_logits, 1)
    n_digit7_logits = F.softmax(digit7_logits, 1)

    with torch.no_grad():
        b_digit2_logits = torch.stack((n_digit2_logits[:, :10].sum(1), n_digit2_logits[:, 10:].sum(1))).cpu().numpy()
        b_digit3_logits = torch.stack((n_digit3_logits[:, :10].sum(1), n_digit3_logits[:, 10:].sum(1))).cpu().numpy()
        b_digit4_logits = torch.stack((n_digit4_logits[:, :10].sum(1), n_digit4_logits[:, 10:].sum(1))).cpu().numpy()
        b_digit5_logits = torch.stack((n_digit5_logits[:, :10].sum(1), n_digit5_logits[:, 10:].sum(1))).cpu().numpy()
        b_digit6_logits = torch.stack((n_digit6_logits[:, :10].sum(1), n_digit6_logits[:, 10:].sum(1))).cpu().numpy()
        b_digit7_logits = torch.stack((n_digit7_logits[:, :10].sum(1), n_digit7_logits[:, 10:].sum(1))).cpu().numpy()

    batch_size = list(digit2_logits.shape)[0]
    digit1 = np.array([
        [np.prod([b_digit2_logits[mapping_indexes[i][0]][row_i], b_digit3_logits[mapping_indexes[i][1]][row_i],
         b_digit4_logits[mapping_indexes[i][2]][row_i], b_digit5_logits[mapping_indexes[i][3]][row_i],
         b_digit6_logits[mapping_indexes[i][4]][row_i], b_digit7_logits[mapping_indexes[i][5]][row_i]])
         for i in range(len(mapping_indexes))] for row_i in range(batch_size)])

    digit1_tensor = torch.from_numpy(digit1).float().cuda()
    return digit1_tensor
