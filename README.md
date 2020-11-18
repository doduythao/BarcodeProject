# BarcodeProject

## Package requirements

python 3.6

    pytorch
    torchvision
    scipy
    pillow==6.1

## Prepare Dataset

Make `data` folder at `<this repo's root>/model/` and `cd` to this `data` folder, then do following tasks:

### Download
    https://uithcm-my.sharepoint.com/:f:/g/personal/13520797_ms_uit_edu_vn/EolYFvBTBTpOpaAFTd6bw-gBHoMzFSfDnboqZ4-9dDdAOg?e=XDqKfC
    curl -L "https://drive.google.com/uc?id=1K12-ySAyNtpJV8f5_3VugeLRfkfKL8iE&export=download" > list.zip

### Unzip and arrange

At the `data` folder, `unzip -q <downloaded zips' files>`
(Copy to merge train folders into only 1.)

    cp -a add_syn_train/img/. syn_train/img/
    cp -a add_syn_train/gt/. syn_train/gt/
    
    cp -a add_syn_train2/img/. syn_train/img/
    cp -a add_syn_train2/txt/. syn_train/gt/
    
    cp -a real_train_aug/img/. syn_train/img/
    cp -a real_train_aug/txt/. syn_train/gt/
    
Now, we have the file tree like this:

    data/
      real/
      syn_train/
      full_train.txt
      real_full.txt
      real_train.txt
      real_val.txt
      syn_train.txt

delete all other directories and zip files.

    rm -r syn_train.zip add_syn_train.zip add_syn_train2.zip real_train_aug.zip real.zip list.zip add_syn_train/  add_syn_train2/ real_train_aug/
    
## Train
Go to each model folder, preview the train.py to learn more about the params to fill.
Run `python train.py` with params.
