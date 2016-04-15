#!/usr/bin/env python
"""
This script will do the fft shift
@version:1.0
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

import numpy as np

def fft_shift(data_input):
    '''
    Args:
        data_input: ndarray type

    Returns:
        ndarray type

    '''
    #total_len = np.size(data_input)
    #total_row = len(data_input)
    #total_column = total_len / total_row
    data_shift_x = fft_shift_x(data_input)
    data_shift_x_y = fft_shift_y(data_shift_x)
    return data_shift_x_y

def fft_shift_x(data_input):
    #total_len = np.size(data_input)
    #total_row = len(data_input)
    #total_column = total_len / total_row
    #ny = total_row
    #nx = total_column
    #data_shift_x = np.zeros([ny,nx])
    ny,nx = data_input.shape
    data_shift_x = [[0 for col in range(nx)] for row in range(ny)]

    data_shift_x[:][0:nx/2-1] = data_input[:][nx/2:nx-1]
    data_shift_x[:][nx/2:nx-1] = data_input[:][0:nx/2-1]

    return  np.array(data_shift_x)

def fft_shift_y(data_input):
    #total_len = np.size(data_input)
    #total_row = len(data_input)
    #total_column = total_len / total_row
    #ny = total_row
    #nx = total_column
    #data_shift_y = np.zeros([nx,ny])
    nx,ny = data_input.shape
    data_shift_y = [[0 for col in range(ny)] for row in range(nx)]

    data_shift_y[0:ny/2-1][:] = data_input[ny/2:ny-1][:]
    data_shift_y[ny/2:ny-1][:] = data_input[0:ny/2-1][:]

    return  np.array(data_shift_y)
