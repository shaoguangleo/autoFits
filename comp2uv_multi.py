#!/usr/bin/env python
"""
This script will comp the uv multi data
@version:1.0
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

#import fix
import numpy as np
import comp2uv
from cal_col_row import *

def comp2uv_multi(x_fit_multi,uv_data):
    # Calculate the re and im of visibility base on the x_fit_multi&&uv
    # x_fit format [Flux, x0, y0, Major, Minor, Phi(deg)]
    # x_fit format [   1,  2,  3,     4,     5,        6]
    row, col = cal_col_row(uv_data)
    uv_re_im_fit_multi = np.zeros((row,2))
    #cmp_num = fix.fix(len(x_fit_multi)/6)
    cmp_num = int(np.fix(len(x_fit_multi)/6))

    x_fit = []
    for i in range(cmp_num):
        delta = i * 6
        for j in range(6):
            x_fit.append(x_fit_multi(delta+j))
        #print 'HHHHH'
        print x_fit
        #import time
        #time.sleep(4)
        # Here 0 means flux info, 3 means Major, 4 means Phi
        x_fit[3] = abs(x_fit[3])
        x_fit[0] = abs(x_fit[0])
        x_fit[4] = abs(x_fit[4])

        if i > 0:
            x_fit[4] = 1
            x_fit[5] = 0

#    print 'uv data len is %d' % len(uv_data)
    uv_re_im_fit = comp2uv.comp2uv(x_fit,uv_data)
#    print type(uv_re_im_fit)
#    print type(uv_re_im_fit_multi)
    uv_re_im_fit_multi = np.array(uv_re_im_fit_multi) + uv_re_im_fit
    #print uv_re_im_fit_multi[0]

    return uv_re_im_fit_multi
