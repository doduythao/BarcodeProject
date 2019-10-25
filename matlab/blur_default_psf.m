org_dir = 'D:/test1o/11t1';
output_dir  = 'D:/test1o/11t1o';
if( ~exist(output_dir, 'dir') )
    mkdir(output_dir);
end

img_list = dir(fullfile(org_dir,'*.png'));

for i = 1:length(img_list)
    img_name = img_list(i).name;
    full_path = fullfile(org_dir, img_name);
    [ ~, sname, ~] = fileparts(full_path);
    img = imread(full_path);
    PSF = fspecial('motion', 7, 5); % create PSF
    blurred = imfilter(img, PSF, 'circular', 'conv');
    output_name = fullfile(output_dir, img_name);
    imwrite(blurred, output_name);
end