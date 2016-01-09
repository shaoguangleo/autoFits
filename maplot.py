#!/usr/bin/env python
"""
This script will plot
@version:0.9
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

import load_data
import all_class
import uv_grid
import g_ifft2
import matplotlib.pyplot as plt
import numpy as np
import uv_bin

def maplot(uvData, my_units, domap):
    # Plot ,dirty beam,residual map,restored map
    # Prepare uv bin
    [uvbin,uvbin_array,uvb] =uv_bin.uv_bin(uvData,my_units)

    # for debug
    trace =0

    # set paremeter for uvgrid
    # todo
    nmask = 2
    tgtocg = 120
    # default
    convfn = load_data.convfn
    rxft   = load_data.rxft_1024
    ryft   = load_data.ryft_1024

    if my_units.nx == 256:
        convfn = load_data.convfn
        rxft   = load_data.rxft_256
        ryft   = load_data.ryft_256
    if my_units.nx == 1024:
        convfn = load_data.convfn
        rxft   = load_data.rxft_1024
        ryft   = load_data.ryft_1024

    gcf = all_class.gcf()
    gcf.nmask  = nmask
    gcf.tgtocg = tgtocg
    gcf.convfn = convfn
    gcf.rxft = rxft
    gcf.ryft = ryft

    # uvgrid
    # TODO...
    [cntr_ptr_vector,cntr_ptr_vector_array] = uv_grid.uv_grid(uvData, my_units, uvbin, uvb, gcf, domap);

    fidx = 10
    if trace ==1:
        fidx=fidx+1
        plt.figure(fidx)
        plt.imshow(abs(cntr_ptr_vector_array))
        plt.title('maplot(), uvdata')

    #ifft
    [uvbin_array_conj_shift2_ifft2] = g_ifft2.g_ifft2(cntr_ptr_vector_array)

    if trace ==1:
        fidx=fidx+1
        plt.figure(fidx)
        #plt.imshow(uvbin_array_conj_shift2_ifft2./max(uvbin_array_conj_shift2_ifft2(:)))
        plt.imshow(uvbin_array_conj_shift2_ifft2)
        plt.title('uvdata ifft')

#  * Multiply the image throughout by the sensitivity function to remove the
#%  * gridding convolution function.
    rxft_length = len(rxft);
    ryft_length = len(ryft);
    sacle_x = rxft_length/my_units.nx;
    sacle_y = ryft_length/my_units.ny;
    for y in range(my_units.ny):
        for x in range(my_units.nx):
            x_xu = np.ceil(round(x*sacle_x));
            y_xu = np.ceil(round(y*sacle_y));
            uvbin_array_conj_shift2_ifft2_rft[y][x] = ryft(y_xu)*rxft(x_xu)*uvbin_array_conj_shift2_ifft2(y,x);

    if trace ==1:
        fidx=fidx+1;
        plt.figure(fidx);
        #plt.imshow(uvbin_array_conj_shift2_ifft2_rft./max(uvbin_array_conj_shift2_ifft2_rft(:)));
        plt.imshow(uvbin_array_conj_shift2_ifft2_rft);
        plt.title('maplot(), map image');
    # Make sure the image pixel is not complex, if it is complex means program have error
    # uvbin_array_conj_shift2_ifft2_rft_abs = abs(uvbin_array_conj_shift2_ifft2_rft);
    return uvbin_array_conj_shift2_ifft2_rft
