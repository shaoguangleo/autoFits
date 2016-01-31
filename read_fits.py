#!/usr/bin/env python
"""
This script will read the fits result file
@version:0.9
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

import numpy as np

def read_fits(fits_file):
    print 'ready read the fits file'
    a = open(fits_file)
    rst = []
    for i in a:
        rst.append([float(i.split('\t')[j]) for j in range(1024)])
    return rst