
org_dir = 'C:/Users/thao/DATA/org1';
inp_dir = 'C:/Users/thao/DATA/inp1';
if( ~exist(inp_dir, 'dir') )
    mkdir(inp_dir);
end
output_dir  = 'C:/Users/thao/DATA/out1';
if( ~exist(output_dir, 'dir') )
    mkdir(output_dir);
end


gyro_dir = fullfile('dataset', 'gyro');
noise = 0.01;

img_list = dir(fullfile(org_dir,'*.png'));
gyro_list = load_list('list/gyro.txt');

for i = 1:length(img_list)
    
    img_name = img_list(i).name;
    full_path = fullfile(org_dir, img_name);
    [ ~, sname, ~] = fileparts(full_path);
    img = imread(full_path);

    parfor g = 1:length(gyro_list)
        info_filename = fullfile(gyro_dir, gyro_list{g}, 'info.txt');
        gyro_filename = fullfile(gyro_dir, gyro_list{g}, 'gyro.txt');

        % read trajectory and camera info
        info_data = importdata(info_filename);
        gyro_data = importdata(gyro_filename);

        % synthesize non-uniform blur from 6D camera trajectory
        blur_img = synthesize_nonuniform_blur(img, info_data, gyro_data);
        
        % add noise
        blur_img = blur_img + noise * rand(size(blur_img));

        output_name = sprintf('%s-%s.png', sname, gyro_list{g});
        output_path = fullfile(output_dir, output_name);
        input_path = fullfile(inp_dir, output_name);
        % fprintf('Save %s\n', output_path);
        imwrite(blur_img, output_path);
        imwrite(img, input_path);
    end
end