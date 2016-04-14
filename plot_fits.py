#!/usr/bin/env python
"""
This script will plot fits file
@version:1.0
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_fits(my_fits,fidx):
    print '> Plotting fits file'
    First_cntr_ratio = 1024
    my_fits_max = my_fits.max()
    #my_fits_max = 100.0
    First_cntr = my_fits_max/First_cntr_ratio

    contour_min = np.log2(First_cntr)
    contour_max = np.log2(my_fits_max)
    contour_bin = [i for i in range(int(contour_min),int(contour_max))]
    v = [np.power(2,i) for i in contour_bin]


    plt.figure(fidx)
    plt.hold(True)
    #plt.contour(my_fits,v)
    plt.contour(my_fits,112)
    plt.axis('equal')
    plt.grid
    plt.title('Clean Map')
    plt.savefig('clean_map.png')
    #plt.show()
