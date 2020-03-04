# BarcodeProject

## Package requirements

python 3.6

`pytorch
torchvision
scipy
pillow
`

## Prepare Dataset

Make `data` folder at `<this repo's root>/model/` and `cd` to this `data` folder, then do following tasks:

### Download

`wget --content-disposition --no-check-certificate "https://onedrive.live.com/download?cid=768D72B2AD0A3FD8&resid=768D72B2AD0A3FD8%2115080&authkey=ACqCpXOCVuytFu4"`

`wget --content-disposition --no-check-certificate "https://onedrive.live.com/download?cid=768D72B2AD0A3FD8&resid=768D72B2AD0A3FD8%2115082&authkey=AIwYRJ-3FviDGys"`

`wget --content-disposition --no-check-certificate "https://onedrive.live.com/download?cid=768D72B2AD0A3FD8&resid=768D72B2AD0A3FD8%2115089&authkey=AFd-n_yxIL2dSZ4"`

`wget --content-disposition --no-check-certificate "https://onedrive.live.com/download?cid=768D72B2AD0A3FD8&resid=768D72B2AD0A3FD8%2115086&authkey=AF6RnFRgYAmdz70"`

`wget --content-disposition --no-check-certificate "https://onedrive.live.com/download?cid=768D72B2AD0A3FD8&resid=768D72B2AD0A3FD8%2115085&authkey=ALhaV7mtopohBGI"`

`wget --content-disposition --no-check-certificate "https://onedrive.live.com/download?cid=768D72B2AD0A3FD8&resid=768D72B2AD0A3FD8%2115090&authkey=ABJ0T07qfYiT5Xs"`

### Unzip and arrange

At the `data` folder, `unzip -q <downloaded zips' files>`
(Copy to merge train folders into only 1.)
    cp -a add_syn_train/img/. syn_train/img/
    cp -a add_syn_train/gt/. syn_train/gt/
    
    cp -a add_syn_train2/img/. syn_train/img/
    cp -a add_syn_train2/gt/. syn_train/gt/
    
    cp -a real_train_aug/img/. syn_train/img/
    cp -a real_train_aug/txt/. syn_train/gt/
