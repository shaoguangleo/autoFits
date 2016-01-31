#!/usr/bin/env python
"""
This script equal the g_ifft2
@version:0.9
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
    uvbin_array_zero = np.zeros((ny,nx))
    if all_class.debug:
        print nvgrid
        print nugrid
    all_class.print_debug()
    #uvbin_array_zero[0:len(uvbin_array_zero),0:nugrid] = cntr_ptr_vector_array
    for i in range(nvgrid):
        for j in range(nugrid):
            uvbin_array_zero[i][j] = cntr_ptr_vector_array[i][j]

    uvbin_array_conj = uvbin_array_zero
    for pos_x in range((nx/2)):
        for pos_y in range(-(ny/2)+1,(nx/2)):
            pos_conj_x = -pos_x
            pos_conj_y = -pos_y

            pos_x_idx = pos_x + (nx/2)+1
            pos_y_idx = pos_y + (ny/2)+1

            pos_conj_x_idx = pos_conj_x + (nx/2)+1
            pos_conj_y_idx = pos_conj_y + (ny/2)+1

            uvbin_array_conj[pos_y_idx-1][pos_x_idx-1] = np.conj(uvbin_array_conj[pos_conj_y_idx-1][pos_conj_x_idx-1])

    #uvbin_array_conj_ifft2 = ifft2(uvbin_array_conj);
    uvbin_array_conj_ifft2 = np.fft.ifft2(uvbin_array_conj)

    [uvbin_array_conj_ifft2_shift2] = fft_shift.fft_shift(uvbin_array_conj_ifft2)

    return uvbin_array_conj_ifft2_shift2
