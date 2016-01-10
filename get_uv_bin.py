#!/usr/bin/env python
"""
This script will get uv bin data
@version:0.9
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

import numpy as np
def get_uv_bin(uvb,uu,vv):
    # If the point is in the unmapped -ve U part of the UV plane,
    # switch to the mapped conjugate-symmetric pixel.
    if uu >= 0:
        uu = -uu
        vv = -vv
    #  Determine the position in the bin array wrt its U=0,V=0 origin.
    #  binpix = uvb->nu * (uvb->nv/2 + floor(vv * uvb->vtopix + 0.5)) +
    #  floor(uu * uvb->utopix + 0.5);
    binpix = uvb.nu * (uvb.nv/2 + np.floor(vv * uvb.vtopix + 0.5)) + np.floor(uu * uvb.utopix + 0.5);
    # binpix_matlab = binpix +1;
    return binpix + 1
