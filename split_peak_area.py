#!/usr/bin/env python
"""
This script will plot
@version:0.9
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

import guass
import numpy as np
import pybwlabel

def peakInf_split_func(my_map_area,peakInf_leaf_current,contour_bin, area_pix_sum_min):
    filt = guass.fspecial_gauss(20,10)
    my_map_filt = my_map_area
    #TODO is reallog different with log function
    my_map_log2 = np.log(my_map_filt)/np.log(2)

    peakInf_split_num = 1
    peakInf_split = {}
    peakInf_split = peakInf_leaf_current

    area = peakInf_leaf_current['area']
    area_pix_sum = sum(area)
    if area_pix_sum > area_pix_sum_min:
        for Z_thresh in range(contour_bin[1,end]):
            Z_bigger =(my_map_log2 >= Z_thresh)
            [L,M]=pybwlabel.bwlabel1(Z_bigger,8)

            if M>1:
                peakInf_split_num = M
                for L_labelIdx in range(M):
                    area = (L == L_labelIdx)
                    my_map_area_temp = np.dot(my_map_area,area)
                    am_init(L_labelIdx) = max(my_map_area_temp)

                b = sorted(am_init)
                sort_idx = []
                for i in b:
                    sort_idx.append(am_init.index(i))

                for peakIdx in range(M):
                    L_labelIdx = sort_idx(peakIdx)
                    area = (L ==L_labelIdx)
                    my_map_area_temp = np.dot(my_map_area,area)
                    am = max(my_map_area_temp)

                    # TODO
                    #[r c] = find(my_map_area_temp == am);
                    r,c = 857,354
                    peakInf_split['centerPos'] = [r,c]
                    peakInf_split['am'] = my_map_area_temp(r,c)
                    peakInf_split['area'] = area

                    am_sort(peakIdx) = am