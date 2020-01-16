org_dir = 'C:/Users/thao/11_o';
output_dir  = 'C:/Users/thao/11_o_o';
if( ~exist(output_dir, 'dir') )
    mkdir(output_dir);
end

img_list = dir(fullfile(org_dir,'*.png'));

parfor i = 1:length(img_list)
    img_name = img_list(i).name;
    full_path = fullfile(org_dir, img_name);
    [ ~, sname, ~] = fileparts(full_path);
    img = imread(full_path);
    choice = randi([0 1], 1, 1);
    if choice == 0
        ranlen   = randi([5 10], 1, 1);
        rantheta = randi([0 4], 1, 1);
        PSF = fspecial('motion', ranlen, rantheta); % create PSF
    else
        ranradius = randi([3 5], 1, 1);
        PSF = fspecial('disk', ranradius);
    end
    blurred = imfilter(img, PSF, 'circular', 'conv');
    output_name = fullfile(output_dir, img_name);
    imwrite(blurred, output_name);
end