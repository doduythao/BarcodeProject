import barcode
from barcode.writer import ImageWriter
import random
import qrcode

qr = qrcode.QRCode()
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

ean13_array = random.sample(range(1000000000000, 9999999999999), 10)

for i in ean13_array:
    ean = EAN(str(i), writer=ImageWriter())
    ean.save('dataset/1d/' + str(i), options=random.choice(option))

with open('quotes_for_qr.txt') as f:
    qr_list = list(f)

for i in range(len(qr_list)):
    qr.add_data(qr_list[i])
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('dataset/1d/' + str(i)+'.png', 'PNG')