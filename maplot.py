#!/usr/bin/env python
"""
This script will plot uv data
@version:0.99
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
    # Will return ndarray too
    # Plot ,dirty beam,residual map,restored map
    # Prepare uv bin
    [uvbin,uvbin_array,uvb] =uv_bin.uv_bin(uvData,my_units)

    # for debug
    trace =0

    # set paremeter for uvgrid
    nmask = 2
    tgtocg = 120
    # default
    convfn = load_data.convfn
    rxft   = load_data.rxft_1024
    ryft   = load_data.ryft_1024

    '''
    if my_units.nx == 256:
        convfn = load_data.convfn
        rxft   = load_data.rxft_256
        ryft   = load_data.ryft_256
    '''
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

    if all_class.debug:
        print 'uvbin is '
        print uvbin

    [cntr_ptr_vector,cntr_ptr_vector_array] = uv_grid.uv_grid(uvData, my_units, uvbin, uvb, gcf, domap)
    if all_class.debug:
        print '-'*80
        print len(cntr_ptr_vector)
        print cntr_ptr_vector_array.shape
        temp_rst = open('temp_rst.txt','w')
        temp_rst.write(str(cntr_ptr_vector))
        temp_rst.close()
        print '-'*80
        import time
        time.sleep(5)

    fidx = 10
    if all_class.debug:
        trace = 1
    #TODO Here should check the value cntr_ptr_vector_array, seems different
    if trace ==1:
        fidx=fidx+1
        plt.figure(fidx)
        plt.imshow(abs(cntr_ptr_vector_array))
        plt.title('maplot(), uvdata')
        plt.show()


    #ifft
    uvbin_array_conj_shift2_ifft2 = g_ifft2.g_ifft2(cntr_ptr_vector_array)

    #TODO the image is different with Matlab
    if trace ==0:
        fidx=fidx+1
        plt.figure(fidx)
        #plt.imshow(uvbin_array_conj_shift2_ifft2./max(uvbin_array_conj_shift2_ifft2(:)))
        #plt.imshow(uvbin_array_conj_shift2_ifft2)
        plt.imshow(uvbin_array_conj_shift2_ifft2/uvbin_array_conj_shift2_ifft2.max())
        plt.title('uvdata ifft')
        #plt.show()

#  * Multiply the image throughout by the sensitivity function to remove the
#%  * gridding convolution function.
    rxft_length = len(rxft)
    ryft_length = len(ryft)
    scale_x = rxft_length/my_units.nx
    scale_y = ryft_length/my_units.ny

    uvbin_array_conj_shift2_ifft2_rft = [[0 for row in range(my_units.ny)] for col in range(my_units.nx)]

    for y in range(my_units.ny):
        for x in range(my_units.nx):
            x_xu = np.ceil(round(x*scale_x))
            y_xu = np.ceil(round(y*scale_y))
            uvbin_array_conj_shift2_ifft2_rft[y][x] = ryft[int(y_xu)]*rxft[int(x_xu)]*uvbin_array_conj_shift2_ifft2[y][x]

    if trace ==1:
        fidx=fidx+1
        plt.figure(fidx)
        #plt.imshow(uvbin_array_conj_shift2_ifft2_rft./max(uvbin_array_conj_shift2_ifft2_rft(:)));
        plt.imshow(uvbin_array_conj_shift2_ifft2_rft)
        plt.title('maplot(), map image')
        plt.show()
    # Make sure the image pixel is not complex, if it is complex means program have error
    # uvbin_array_conj_shift2_ifft2_rft_abs = abs(uvbin_array_conj_shift2_ifft2_rft);
    return np.array(uvbin_array_conj_shift2_ifft2_rft)
