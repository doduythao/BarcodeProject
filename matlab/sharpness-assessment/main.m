fileList = dir('demo_folder\*.png');
for file=fileList'
    im = imread(strcat('demo_folder/', file.name));
    im_gray = rgb2gray(im);
    im_double = double(im_gray);
    [LPC_SI lpc_map] = lpc_si(im_double);
    if (LPC_SI >= 0.92)
        imwrite(im, strcat('keep/', file.name));
    end
end
