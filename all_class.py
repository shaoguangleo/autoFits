#!/usr/bin/env python
"""
This script include all the class units need for the program
@version:0.9
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

# Here for the units structure
class units:
    def __init__(self):
        self.nx = 1024
        self.ny = 1024
        self.xinc = 4.8481e-10
        self.yinc = 4.8481e-10
        self.uinc = 2.0143e6
        self.vinc = 2.0143e6
        self.u_limit = 5.1566e8
        self.v_limit = 5.1566e8
        self.xinmap = 0.1
        self.yinmap = 0.1
        self.binwid = 2

class uvb:
    def __init__(self):
        self.utopix = 1e-6
        self.vtopix = 1e-6
        self.nu = 512
        self.nv = 512
        self.nbin = 262144

class gcf:
    def __init__(self):
        self.nmask =2
        self.tgtocg = 120
        self.convfn = [0 for i in range(302)]
        self.rxft_1024 = [0 for i in range(1024)]
        self.ryft_1024 = [0 for i in range(1024)]
        self.rxft_256 = [0 for i in range(256)]
        self.ryft_256 = [0 for i in range(256)]
        self.rxft = [0 for i in range(1024)]
        self.ryft = [0 for i in range(1024)]

class vis:
    def __init__(self):
        self.amp = 0.0
        self.phs = 0.0
        self.modamp = 0.0
        self.modphs = 0.0

# 1 will print verbose information and 0 for quite
debug = 0

def print_debug():
    print '*'*40
    print "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
    print '*'*40
