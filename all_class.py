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
