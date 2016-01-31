#!/usr/bin/env python
"""
This script will load uv sel uv
@version:0.9
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

def load_uvsel_uv(uv_filename):
    # Pick up the data info
    # uv data parameters:
    # uu , vv, amp, phs, wt, uvscale, cif, isub, base, ut
    # 1  ,  2,   3,   4,  5,       6,   7,    8,    9, 10
    print 'Now loading uv file...'

    fid = open(uv_filename)
    content = fid.readlines()

    uv_data = []
    #for i in range(len(content)):
    for i in content:
        # This is the data info
        # uv_data.append(content(i).split('=')[1])
        uv_data.append(i.split('=')[1])
        # This is the describe info
        # uv_data.append(content(i).split('=')[0])

    return uv_data
