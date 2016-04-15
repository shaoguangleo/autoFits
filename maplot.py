#!/usr/bin/env python
"""
This script will plot uv data
@version:1.0
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
    #if all_class.debug:
    if not all_class.debug:
        print uvb.nu
        print uvb.nv
    plt.figure()
    plt.plot(uvbin)
    plt.title('UVBIN')
    plt.savefig('uvbin.png')

    plt.figure()
    plt.contour(uvbin_array)
    plt.savefig('uvbin_arr.png')

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

    [cntr_ptr_vector,cntr_ptr_vector_array] = uv_grid.uv_grid(uvData, my_units, uvbin, uvb, gcf, domap)
    if all_class.debug:
        print '-'*80
        print len(cntr_ptr_vector)
        print cntr_ptr_vector_array.shape
        temp_rst = open('temp_rst.txt','w')
        temp_rst.write(str(cntr_ptr_vector))
        temp_rst.close()
        print '-'*80

    fidx = 10
    if all_class.debug:
        trace = 1
    if trace ==1:
        fidx=fidx+1
        plt.figure(fidx)
        plt.imshow(abs(cntr_ptr_vector_array))
        plt.title('maplot(), uvdata')
        #plt.savefig('maplot_uv.png')

    fidx=fidx+1
    plt.figure(fidx)
    plt.imshow(abs(cntr_ptr_vector_array))
    plt.title('maplot(), uvdata')
    plt.savefig('maplot.png')


    #ifft
    uvbin_array_conj_shift2_ifft2 = g_ifft2.g_ifft2(cntr_ptr_vector_array)
    #print cntr_ptr_vector_array
    #print uvbin_array_conj_shift2_ifft2.max()
    #print 'The max'
    #print cntr_ptr_vector_array.max()

    if trace ==0:
    #if trace ==1:
        fidx=fidx+1
        plt.figure(fidx)
        #plt.imshow(uvbin_array_conj_shift2_ifft2./max(uvbin_array_conj_shift2_ifft2(:)))
        #plt.imshow(uvbin_array_conj_shift2_ifft2)
        print 'max'
        print uvbin_array_conj_shift2_ifft2.max()
        print type(uvbin_array_conj_shift2_ifft2)
        #plt.imshow(uvbin_array_conj_shift2_ifft2/uvbin_array_conj_shift2_ifft2.max())
        plt.contour(uvbin_array_conj_shift2_ifft2)
        plt.title('uvdata ifft')
        plt.savefig('uv_data_ifft.png')

#  * Multiply the image throughout by the sensitivity function to remove the
#%  * gridding convolution function.
    rxft_length = len(rxft)
    ryft_length = len(ryft)
    scale_x = rxft_length/my_units.nx
    scale_y = ryft_length/my_units.ny
    if all_class.debug:
        print rxft_length
        print ryft_length
        print scale_x
        print scale_y

    uvbin_array_conj_shift2_ifft2_rft = [[0 for row in range(my_units.ny)] for col in range(my_units.nx)]

    for y in range(my_units.ny):
        for x in range(my_units.nx):
            x_xu = np.ceil(round(x*scale_x))
            y_xu = np.ceil(round(y*scale_y))
            uvbin_array_conj_shift2_ifft2_rft[y][x] = ryft[int(y_xu)]*rxft[int(x_xu)]*uvbin_array_conj_shift2_ifft2[y][x]

    plt.figure()
    plt.contour(uvbin_array_conj_shift2_ifft2_rft)
    plt.title('image_remove_gridding')
    plt.savefig('remove_gridding.png')

    if trace ==0:
        #fidx=fidx+1
        plt.figure()
        #plt.imshow(uvbin_array_conj_shift2_ifft2_rft./max(uvbin_array_conj_shift2_ifft2_rft(:)));
        #plt.imshow(uvbin_array_conj_shift2_ifft2_rft)
        #plt.title('maplot(), map image')
        #plt.savefig('maplot_1.png')
    # Make sure the image pixel is not complex, if it is complex means program have error
    # uvbin_array_conj_shift2_ifft2_rft_abs = abs(uvbin_array_conj_shift2_ifft2_rft);
    # print np.array(uvbin_array_conj_shift2_ifft2_rft)
    return np.array(uvbin_array_conj_shift2_ifft2_rft)
