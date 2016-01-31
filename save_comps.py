#!/usr/bin/env python
"""
This script will save comps
@version:0.9
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

import  numpy as np

def save_comps(x_fit_multi_array,comp_filename,headInfo):

    size = np.size(x_fit_multi_array)
    column = np.size(x_fit_multi_array[0])
    row = size / column

    fileID = open(comp_filename,'a')
    print fileID
    for i in range(len(headInfo)):
        fileID.writelines('%s ' % headInfo[i])

    fileID.writelines('GuassID,   Flux,   x0,   y0,  Major(mas),  AxialRatio, Phi(deg)')
    comp2txt_array = []
    for i in range(row):
        comp2txt_array[i][0] = i
        for j in range(2,column):
            comp2txt_array[i][j] = x_fit_multi_array[i][j]

    fileID.writelines('%6.5f, %6.5f, %6.5f, %6.5f, %6.5f, %6.5f, %6.5f' % comp2txt_array)
    fileID.close()