#!/usr/bin/env python
"""
This script will comp the uv multi data
@version:1.0
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""
import numpy as np

def cal_col_row(data_list):
    total_size = np.size(data_list)
    col = np.size(data_list[0])
    row = total_size / col
    return row,col