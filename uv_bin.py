#!/usr/bin/env python
"""
This script will plot
@version:0.9
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

import all_class
import string
from all_class import units as my_units
from get_uv_bin import *
import numpy as np

def uv_bin(uv_data,my_units):
    #binwid meaning?
    uvb = all_class.uvb()
    uvb.utopix =  1.0 / my_units.uinc / my_units.binwid;
    uvb.vtopix =  1.0 / my_units.vinc / my_units.binwid;
    uvb.nu=my_units.nx/4;
    uvb.nv=my_units.nx/2;
    uvb.nbin=uvb.nu*uvb.nv;

    uvbin = [0 for row in range(uvb.nbin)]

    for i in range(len(uv_data)):
        #uu = string.atof(uv_data[i].split(',')[0])
        #vv = string.atof(uv_data[i].split(',')[1])
        uu = string.atof(uv_data[i][0])
        vv = string.atof(uv_data[i][1])
        #if string.atof(uv_data[i].split(',')[4]) > 0:
        if string.atof(uv_data[i][4]) > 0:
            binpix = get_uv_bin(uvb,uu,vv)
            uvbin[int(binpix)] = uvbin[int(binpix)] +1;

            # If the visibility is in the U=0 bin then its conjugate mirrored
            # point will also be in the bin array, on the other side of V=0.
            # Count it as well.
            if(round(abs(uu) * uvb.utopix)==0):
                binpix = get_uv_bin(uvb,uu,-vv);
                uvbin[int(binpix)] = uvbin[int(binpix)] +1;

    # Add a uniform bin entry to account for the optional zero-spacing flux
    # or for natural weighting.
    # bc = get_uv_bin(uvb, 0.0f, 0.0f);
    binpix = get_uv_bin(uvb,0.0,0.0)
    uvbin[int(binpix)] = uvbin[int(binpix)] +1

    # uvbin_array = reshape(uvbin,uvb.nu,uvb.nv)';
    uvbin_array = np.reshape(uvbin,(uvb.nu,uvb.nv))
    uvbin_array = np.transpose(uvbin_array)

    return [uvbin, uvbin_array, uvb]
