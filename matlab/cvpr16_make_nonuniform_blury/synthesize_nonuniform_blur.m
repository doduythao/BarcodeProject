function blur_img = synthesize_nonuniform_blur(img, info_data, gyro_data)
    
    img= im2double(img);
    
    bd = 20; %% tmp
    img_pad = padarray(img, [bd, bd], 'replicate', 'both');


    num_row = size(img_pad, 1);
    num_col = size(img_pad, 2);


    time_interval = 0.01;

    % set up start and end time
    st_time = info_data(1, 3) + (-8) * time_interval - info_data(1, 2);
    ed_time = info_data(1, 3) + (-8) * time_interval;


    valid_row = 1:size(gyro_data, 1);%find(gyro_data(:, end) < ed_time + time_interval);


    % interpolate 
    portion = 3;%ceil(1/infoData(1,2));
    intervalAfterTime = time_interval/portion;

    % linear interpolation
    tempInd = 1:portion:1+(length(valid_row)-1)*portion;
    x = tempInd;
    v = gyro_data(valid_row,1:end);
    xq = 1:1+(length(valid_row)-1)*portion;
    vq = interp1(x,v,xq);
    gyroInterData = vq;

    % compute angular velocity 
    avelInter = gyroInterData(2:end,4:6).*repmat((gyroInterData(2:end,end)- ...
        gyroInterData(1:end-1,end)),[1,3]);

    avelInter = cumsum(avelInter)/1;


    % switch the tx ty for headleft
    tmp = gyroInterData(:,1);
    gyroInterData(:,1) = -gyroInterData(:,2);
    gyroInterData(:,2) = tmp;

    % compute velocity 
    comDrift = [0,0.00,0];
    velInter = (gyroInterData(2:end,1:3)-repmat(comDrift,[size(gyroInterData,1)-1,1]))...
        .*repmat((gyroInterData(2:end,end)- gyroInterData(1:end-1,end)),[1,3]);


    velInter = cumsum(velInter*9.8);


    % initial speed
    initialSpeed = [0,0,0];
    velInter = velInter + repmat(initialSpeed,[size(velInter,1),1]);

    % compute the position
    activeRow = intersect(find(gyroInterData(:,end)<ed_time+time_interval),...
        find(gyroInterData(:,end)>=st_time));
    gyroInterData = gyroInterData(activeRow,:);
    activeRow(end)=[];


    rotInter = avelInter(activeRow,:).*repmat((gyroInterData(2:end,end)...
        - gyroInterData(1:end-1,end)),[1,3]);
    rotInter = cumsum(rotInter);



    tranInter = velInter(activeRow,:).*repmat((gyroInterData(2:end,end)...
        - gyroInterData(1:end-1,end)),[1,3]);
    tranInter = cumsum(tranInter)/1;

    pixelPitch = 1e-5;
    poseInter = [tranInter,avelInter(activeRow,:)];
    poseInter = poseInter - repmat(poseInter(1,:),[size(poseInter,1),1]);

    if(1)
        factor = [1,1,1,-1,-1,-1];
    else
        factor = [1,1,1,1,1,1];
    end
    poseInter = poseInter.*repmat(factor,[size(poseInter,1),1]);

    ox = 0;
    oy = 0;
    rotCen = [0,0,0,ox,oy,0];
    poseInterOff = poseInter + repmat(rotCen,[size(poseInter,1),1]);

    fprintf('Generate local PSF...\n');

    data = poseInterOff;
    N_pose = size(data,1);
    weight = 1/N_pose;

    m = num_row;
    n = num_col;
    K = sparse([],[],[],m*n,m*n);

    for j = 1:N_pose
        pose = [data(j,4),data(j,5),data(j,6),data(j,1),data(j,2),data(j,3)];

        K_mat = compute_Kpose_6D(m,n,pose,1);

        K = K + weight * K_mat;
    end

    blur_img = img_pad;
    for c = 1:size(img_pad, 3)  

        img_vector = img_pad(:, :, c);
        img_vector = K * img_vector(:);
        blur_img(:, :, c) = reshape(img_vector, num_row, num_col);

    end

    blur_img = blur_img(1+bd:end-bd, 1+bd:end-bd, :);
    
end