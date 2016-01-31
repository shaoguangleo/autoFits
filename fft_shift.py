#!/usr/bin/env python
"""
This script will do the fft shift
@version:0.9
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

import numpy as np

def fft_shift(data_input):
    total_len = np.size(data_input)
    total_row = len(data_input)
    total_column = total_len / total_row

    data_shift_x = fft_shift_x(data_input)
    data_shift_x_y = fft_shift_y(data_shift_x)

def fft_shift_x(data_input):
    total_len = np.size(data_input)
    total_row = len(data_input)
    total_column = total_len / total_row
    ny = total_row
    nx = total_column
    data_shift_x = np.zeros([ny,nx])

    data_shift_x[:][0:nx/2] = data_input[:][nx/2:nx]
    data_shift_x[:][nx/2:nx] = data_input[:][0:nx/2]

def fft_shift_y(data_input):
    total_len = np.size(data_input)
    total_row = len(data_input)
    total_column = total_len / total_row
    ny = total_row
    nx = total_column

    data_shift_y[:][0:nx/2] = data_input[nx/2:nx][:]
    data_shift_y[:][nx/2:nx] = data_input[1:nx/2][:]
