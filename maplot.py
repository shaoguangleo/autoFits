def my_maplot(uvData, my_units, domap):
    # Plot ，dirty beam脏束，residual map残图，restored map即CLEAN图
    # Prepare uv bin
    [uvbin uvbin_array uvb] = my_uvbin(uvData,my_units);

% for debug
trace =0;

% set paremeter for uvgrid
% todo
nmask = 2;
tgtocg = 120;
% default
    my_load_convfn;
    my_load_rxft_1024;
    my_load_ryft_1024;
if my_units.nx == 256
    my_load_convfn;
    my_load_rxft;
    my_load_ryft;
end
if my_units.nx == 1024
    my_load_convfn;
    my_load_rxft_1024;
    my_load_ryft_1024;
end


gcf.nmask  = nmask;
gcf.tgtocg = tgtocg;
gcf.convfn = convfn;
gcf.rxft = rxft;
gcf.ryft = ryft;

% uvgrid
[cntr_ptr_vector cntr_ptr_vector_array] = ...
    my_uvgrid(uvData, my_units, uvbin, uvb, gcf, domap);

fidx = 10;
if trace ==1
    fidx=fidx+1;
    figure(fidx);
    imshow(abs(cntr_ptr_vector_array));
    title('maplot(), uvdata');
end

% 傅里叶反变换
[uvbin_array_conj_shift2_ifft2] = my_ifft2(cntr_ptr_vector_array);

if trace ==1
    fidx=fidx+1;
    figure(fidx);
    imshow(uvbin_array_conj_shift2_ifft2./max(uvbin_array_conj_shift2_ifft2(:)));
    title('uvdata傅里叶反变换');
end

%  * Multiply the image throughout by the sensitivity function to remove the
%  * gridding convolution function.
rxft_length = length(rxft);
ryft_length = length(ryft);
sacle_x = rxft_length/my_units.nx;
sacle_y = ryft_length/my_units.ny;
for y=1:my_units.ny
    for x=1:my_units.nx
        x_xu = ceil(round(x*sacle_x));
        y_xu = ceil(round(y*sacle_y));
%         x_xu = x;
%         y_xu = y;
        uvbin_array_conj_shift2_ifft2_rft(y,x) = ...
            ryft(y_xu)*rxft(x_xu)*uvbin_array_conj_shift2_ifft2(y,x);
    end
end

if trace ==1
    fidx=fidx+1;
    figure(fidx); imshow(uvbin_array_conj_shift2_ifft2_rft./max(uvbin_array_conj_shift2_ifft2_rft(:)));
    title('maplot(), map image');
end
% 确保输出的图像像素不是复数。如果是复数，说明程序有错误。
% uvbin_array_conj_shift2_ifft2_rft_abs = abs(uvbin_array_conj_shift2_ifft2_rft);
