import barcode
from barcode.writer import ImageWriter
import random
import qrcode
import sys
import os

# absolutely path make sure have / at the end

path_1d = sys.argv[1]
path_2d = sys.argv[2]

if not os.path.exists(path_1d):
    os.makedirs(path_1d)

if not os.path.exists(path_2d):
    os.makedirs(path_2d)

EAN = barcode.get_barcode_class('ean13')

option = [{'background': '#e3e3e3',
           'write_text': False,
           'quiet_zone': 5,
           'module_width': 0.4,
           'module_height': 20.0},
          {'background': 'white',
           'write_text': False,
           'quiet_zone': 5,
           'module_width': 0.4,
           'module_height': 20.0},
          {'background': 'white',
           'write_text': False,
           'quiet_zone': 5,
           'module_width': 0.4,
           'module_height': 15.0},
          {'background': '#e3e3e3',
           'write_text': False,
           'quiet_zone': 5,
           'module_width': 0.4,
           'module_height': 15.0}]

ean13_array = random.sample(range(1000000000000, 9999999999999), 100)

for i in ean13_array:
    ean = EAN(str(i), writer=ImageWriter())
    ean.save(path_1d + str(i), options=random.choice(option))

with open('quotes_for_qr.txt') as f:
    qr_list = list(f)

for i in range(len(qr_list)):
    qr = qrcode.QRCode()
    qr.add_data(qr_list[i])
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(path_2d + str(i) + '.png', 'PNG')
