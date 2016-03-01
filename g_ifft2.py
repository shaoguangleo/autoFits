#!/usr/bin/env python
"""
This script equal the g_ifft2
@version:1.0
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

import numpy as np
import fft_shift
import all_class

def g_ifft2(cntr_ptr_vector_array):
    total_len = np.size(cntr_ptr_vector_array)
    total_row = len(cntr_ptr_vector_array)
    total_column = total_len / total_row
    nvgrid = total_row
    nugrid = total_column
    #[ nvgrid, nugrid] = size(cntr_ptr_vector_array);
    ny = nvgrid
    nx = 2*(nugrid-1)
    #uvbin_array_zero = np.zeros((ny,nx))
    uvbin_array_zero = [[0 for col in range(nx)] for row in range(ny)]
    for i in range(ny):
        for j in range(nx):
            uvbin_array_zero[i][j] = complex(0)
    if all_class.debug:
        print nx
        print ny
    #uvbin_array_zero[0:len(uvbin_array_zero),0:nugrid] = cntr_ptr_vector_array
    for i in range(nvgrid):
        for j in range(nugrid):
            uvbin_array_zero[i][j] = cntr_ptr_vector_array[i][j]
    #uvbin_array_zero[:,:513] = cntr_ptr_vector_array

    uvbin_array_conj = uvbin_array_zero
    uvbin_array_conj = np.array(uvbin_array_conj)
    if all_class.debug:
        print 'shape'
        print uvbin_array_conj.shape
    for pos_x in range((nx/2)-1):
        for pos_y in range(-(ny/2), (nx/2)):
            pos_conj_x = -pos_x
            pos_conj_y = -pos_y

            pos_x_idx = pos_x + (nx/2)-1
            pos_y_idx = pos_y + (ny/2)-1
            #print pos_x_idx,
#            print pos_y_idx

            pos_conj_x_idx = pos_conj_x + (nx/2)-1
            pos_conj_y_idx = pos_conj_y + (ny/2)-1
#            print pos_conj_y_idx

            #uvbin_array_conj[pos_y_idx-1][pos_x_idx-1] = np.conj(uvbin_array_conj[pos_conj_y_idx-1][pos_conj_x_idx-1])
            uvbin_array_conj[pos_y_idx][pos_x_idx] = np.conj(uvbin_array_conj[pos_conj_y_idx][pos_conj_x_idx])

    #uvbin_array_conj_ifft2 = ifft2(uvbin_array_conj);
    uvbin_array_conj_ifft2 = np.fft.ifft2(uvbin_array_conj)
    if all_class.debug:
        print 'The shape is'
        print uvbin_array_conj_ifft2.shape
        print uvbin_array_conj_ifft2[0][0]
        print uvbin_array_conj[0][0]
        print uvbin_array_conj[1][1]
        print type(uvbin_array_conj_ifft2)

    uvbin_array_conj_ifft2_shift2 = fft_shift.fft_shift(uvbin_array_conj_ifft2)

    return uvbin_array_conj_ifft2_shift2
