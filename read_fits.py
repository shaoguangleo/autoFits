#!/usr/bin/env python
"""
This script will read the fits result file
@version:1.0
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

import numpy as np
import pyfits

def read_fits(fits_file):
    print '> Ready read the fits file'
    hdu_list = pyfits.open(fits_file)
    fits_data = hdu_list[0].data
    return fits_data[0][0]
