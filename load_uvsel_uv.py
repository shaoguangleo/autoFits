#!/usr/bin/env python
"""
This script will load uv sel uv
@version:1.0
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""
import time
import all_class
import sys

def load_uvsel_uv(uv_filename):
    # Pick up the data info
    # uv data parameters:
    # uu , vv, amp, phs, wt, uvscale, cif, isub, base, ut
    # 1  ,  2,   3,   4,  5,       6,   7,    8,    9, 10
    print '> Now loading uv file...'

    fid = open(uv_filename)
    content = fid.readlines()
    fid.close()

    #uv_data = []
    uv_data = [[0 for i in range(10)] for j in range(len(content))]
    #for i in range(len(content)):
    for i,c in enumerate(content):
        sys.stdout.write('                          %.2f%%\r' %(i*100.0/len(content)))
        for j in range(10):
            #uv_data[i][j] = float(c.split('=')[1].strip().split(',')[j])
            uv_data[i][j] = float(c.split(',')[j])
            if j > 5 and j < 10:
                uv_data[i][j] = int(uv_data[i][j])
        # This is the data info
        # uv_data.append(content(i).split('=')[1])
        #uv_data.append(i.split('=')[1].split(',')[0])
        # This is the describe info
        # uv_data.append(content(i).split('=')[0])
    print '\n'
    if all_class.debug:
        print uv_data
    return uv_data
