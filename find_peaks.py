#!/usr/bin/env python
"""
This script will plot
@version:0.9
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

import numpy as np
import matplotlib.pyplot as plt
import split_peak_area


def find_peaks(my_map):
    my_trace = 1
    fidx = 10

    area_pix_sum_min = 10
    First_cntr_ratio = 16
    my_map_max = max(my_map)
    First_cntr = my_map_max/First_cntr_ratio
    contour_min = np.log2(First_cntr)
    contour_max = np.log2(my_map_max)
    contour_bin = range(contour_min,contour_max)
    v = [2**x for x in contour_bin]

    size = np.size(my_map)
    column = np.size(my_map[0])
    row = size / column
    area = np.ones(row,column)
    for i in range(row):
        for j in range(column):
            if my_map[i][j] < First_cntr:
                my_map[i][j] = 0
                area[i][j] = 0

    if my_trace:
        fidx = fidx+1
        plt.figure(fidx)
        plt.contour(my_map,v)
        plt.grid(True)
        plt.title('Astronomical Image')


    print 'Searching local peaks'


    peakInf_leaf_Num = 1
    am = max(my_map)
    # TODO
    # [r c] = find(my_map == am);
    r,c = 512,512
    peakInf_root = {}
    peakInf_root['centerPos'] = [r,c]
    peakInf_root['am'] = [r,c]
    peakInf_root['area'] = np.ones(row,column)
    peakInf_root['peakIdx'] = 1
    peakInf_root['isLeadf'] = -1
    peakInf_root['father'] = []
    peakInf_root['son'] = []


    peakInf_node_all = peakInf_root
    peakInf_leaf_last = peakInf_root
    peakInf_leaf_new = peakInf_root

    newNodeNum = 1
    while newNodeNum > 0:
        peakInf_leaf_last = peakInf_leaf_new
        peakInf_leaf_new = {}
        for peakInf_leaf_last_idx in range(len(peakInf_leaf_last)):
            peakInf_leaf_last_temp = peakInf_leaf_last[peakInf_leaf_last_idx]
            my_map_area = np.dot(my_map,peakInf_leaf_last_temp['area'])
            peakInf_split =split_peak_area.peakInf_split_func(my_map_area,peakInf_leaf_last_temp,contour_bin,area_pix_sum_min)

            if( len(peakInf_split) >1):
                for peakInf_split_idx in range(len(peakInf_split)):
                    peakInf_split_temp = peakInf_split[peakInf_split_idx]
                    peakIdx = len(peakInf_node_all)+1
                    peakInf_split_temp['peakIdx'] = peakIdx
                    peakInf_split_temp['isLeaf'] = 1
                    peakInf_split_temp['father'] = peakInf_leaf_last_temp.peakIdx
                    peakInf_split_temp['son'] = []
                    peakInf_split_temp['x_fit'] = []

                    peakInf_node_all[peakInf_leaf_last_temp['peakIdx']].son(end+1) = peakIdx
                    peakInf_node_all{peakInf_leaf_last_temp.peakIdx}.isLeaf = 0

                    peakInf_leaf_new[end] = peakInf_split_temp
                    peakInf_node_all[end] = peakInf_split_temp
        newNodeNum = length(peakInf_leaf_new);


    # Summary the pixel count, total enegne, average enegne infos.
    for peakIdx=1:length(peakInf_node_all)
        area =  peakInf_node_all{peakIdx}.area;
        my_map_node = my_map.*area;
        energy_sum = sum(my_map_node(:));
        area_pix_sum = sum(area(:));
        energy_per_pix = energy_sum/area_pix_sum;

        peakInf_node_all{peakIdx}.energy_sum = energy_sum;
        peakInf_node_all{peakIdx}.area_pix_sum = area_pix_sum;
        peakInf_node_all{peakIdx}.energy_per_pix = energy_per_pix;

    end

    size = np.size(my_map)
    column = np.size(my_map[0])
    row = size / column

    if my_trace :
        peakImage = np.zeros(row,column)
        for peakIdx in range(len(peakInf_node__all))
            peakImage = peakImage.*(1-peakInf_node_all{peakIdx}.area)+ peakIdx*peakInf_node_all{peakIdx}.area;

        fidx= fidx+1;figure(fidx); imagesc(peakImage); set(gca,'YDir','normal')
        plt.grid(True)
        plt.title(['There are ' + str(len(peakInf_node_all)) + ' local peak area'])

    if my_trace:
        # Display every local peak area
        plot_peak_num = 0
        for peakIdx in range(length(peakInf_node_all):-1:length(peakInf_node_all)-plot_peak_num+1):
            area =  peakInf_node_all{peakIdx}.area
            my_map_node = np.dot(my_map,area)
            fidx= fidx+1
            plt.figure(fidx)
            plt.contour(my_map_node,v)
            plt.grid(True)
            plt.title(['This is the ' + str(peakIdx) + 'th local peak area'])

    # Dividea all node to leaf node and not leaf node
    peakInf_node_isLeaf = {}
    peakInf_node_notLeaf_all = {}
    for peakIdx in range(len(peakInf_node_all)):
        if peakInf_node_all{peakIdx}.isLeaf:
            peakInf_node_isLeaf{end+1} = peakInf_node_all{peakIdx}
        else:
            peakInf_node_notLeaf_all{end+1} = peakInf_node_all{peakIdx}

    # Sort the leaf node by the peak value
    am_all = []
    for peakIdx in range(len(peakInf_node_isLeaf)):
        am_all(peakIdx) = peakInf_node_isLeaf{peakIdx}.am
    [temp sort_idx] = sorted(am_all,'descend')
    peakInf_node_isLeaf_sort_am = {}
    for i in range(len(peakInf_node_isLeaf)):
        peakInf_node_isLeaf_sort_am{i} = peakInf_node_isLeaf{sort_idx(i)}

    # Sort every pixel by the average power
    energy_sum_all = []
    for peakIdx=1 in range(len(peakInf_node_isLeaf)):
        energy_sum_all(peakIdx) = peakInf_node_isLeaf{peakIdx}.energy_sum
    [temp sort_idx] = sorted(energy_sum_all,'descend')
    peakInf_node_isLeaf_sort_energy_sum = {};
    for i in range(len(peakInf_node_isLeaf)):
        peakInf_node_isLeaf_sort_energy_sum{i} = peakInf_node_isLeaf{sort_idx(i)};

    if my_trace:
        #Display every local peak area
        plot_peak_num = 0
        for peakIdx in range(plot_peak_num):
            area =  peakInf_node_isLeaf_sort_energy_sum{peakIdx}.area;
            my_map_node = np.dot(my_map,area)
            fidx= fidx+1
            plt.figure(fidx)
            plt.contour(my_map_node,v)
            plt.grid(True)
            plt.title(['This is the ' + str(peakIdx) +  'th local peak area'])

    return [peakInf_node_isLeaf_sort_am,peakInf_node_isLeaf_sort_energy_sum,peakInf_node_isLeaf,peakInf_node_all]

