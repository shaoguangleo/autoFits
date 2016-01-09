#!/usr/bin/env python
"""
This script will plot
@version:0.9
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

import numpy as np


def find_peaks(my_map):
    my_trace = 1;
    fidx = 10;

    area_pix_sum_min = 10;
    First_cntr_ratio = 16;
    my_map_max = max(my_map(:));
    First_cntr = my_map_max/First_cntr_ratio;
    contour_min = np.log2(First_cntr);
    contour_max = np.log2(my_map_max);
    contour_bin = contour_min:1:contour_max;
    v = 2.^(contour_bin);

    area = ones(size(my_map));
    for i=1:size(my_map,1)
        for j=1:size(my_map,2)
            if my_map(i,j) < First_cntr
                my_map(i,j) = 0;   area(i,j) = 0;
            end
        end
    end
    if my_trace
        fidx = fidx+1;figure(fidx);
        contour(my_map,v);grid on;
        title('天文图像');
    end


    print 'Searching local peaks'


    peakInf_leaf_Num = 1;
    am = max(my_map(:));
    [r c] = find(my_map == am);
    peakInf_root{peakInf_leaf_Num}.centerPos = [r(1), c(1)];
    peakInf_root{peakInf_leaf_Num}.am = my_map(r(1), c(1));
    % peakInf_root{peakInf_leaf_Num}.area = area;
    peakInf_root{peakInf_leaf_Num}.area = ones(size(my_map));
    peakInf_root{peakInf_leaf_Num}.peakIdx = 1;
    peakInf_root{peakInf_leaf_Num}.isLeaf = -1;
    peakInf_root{peakInf_leaf_Num}.father = [];
    peakInf_root{peakInf_leaf_Num}.son = [];

    peakInf_node_all = peakInf_root;
    peakInf_leaf_last = peakInf_root;
    peakInf_leaf_new = peakInf_root;

    newNodeNum = 1;
    while newNodeNum > 0
        peakInf_leaf_last = peakInf_leaf_new;
        peakInf_leaf_new = {};
        for peakInf_leaf_last_idx = 1:length(peakInf_leaf_last)
            peakInf_leaf_last_temp = peakInf_leaf_last{peakInf_leaf_last_idx};
            my_map_area = my_map.* peakInf_leaf_last_temp.area;
            peakInf_split = ...
                my_split_peak_area(my_map_area,peakInf_leaf_last_temp,contour_bin,area_pix_sum_min);
            if( length(peakInf_split) >1)
                for peakInf_split_idx = 1:length(peakInf_split)
                    peakInf_split_temp = peakInf_split{peakInf_split_idx};
                    % 新增节点的序号
                    peakIdx = length(peakInf_node_all)+1;
                    peakInf_split_temp.peakIdx = peakIdx;
                    % 新增节点和父节点的相互关系。
                    peakInf_split_temp.isLeaf = 1;
                    peakInf_split_temp.father = peakInf_leaf_last_temp.peakIdx;
                    peakInf_split_temp.son = [];
                    peakInf_split_temp.x_fit = [];
                    peakInf_node_all{peakInf_leaf_last_temp.peakIdx}.son(end+1) = peakIdx;
                    peakInf_node_all{peakInf_leaf_last_temp.peakIdx}.isLeaf = 0;

                    peakInf_leaf_new{end+1} = peakInf_split_temp;
                    peakInf_node_all{end+1} = peakInf_split_temp;
                end
            end
        end
        newNodeNum = length(peakInf_leaf_new);
    end



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



    if my_trace
        % 在同一幅图像中显示所有局部峰值区域。
        peakImage = zeros(size(my_map));
        for peakIdx=1:length(peakInf_node_all)
            peakImage = peakImage.*(1-peakInf_node_all{peakIdx}.area)+ peakIdx*peakInf_node_all{peakIdx}.area;
        end
        fidx= fidx+1;figure(fidx); imagesc(peakImage); set(gca,'YDir','normal');grid on;
        title(['共 ' num2str(length(peakInf_node_all)) ' 个局部峰值区域']);
    end
    if my_trace
        % 独立显示各个局部峰值区域。
        plot_peak_num = 0;
        for peakIdx=length(peakInf_node_all):-1:length(peakInf_node_all)-plot_peak_num+1
            area =  peakInf_node_all{peakIdx}.area;
            my_map_node = my_map.*area;
            fidx= fidx+1;figure(fidx);
            contour(my_map_node,v);grid on;
            title(['第 ' num2str(peakIdx) ' 个局部峰值区域']);
        end
    end


    % 把所有节点分为 叶子节点 和 非叶子节点 两类。
    peakInf_node_isLeaf = {};
    peakInf_node_notLeaf_all = {};
    for peakIdx=1:length(peakInf_node_all)
        if peakInf_node_all{peakIdx}.isLeaf
            peakInf_node_isLeaf{end+1} = peakInf_node_all{peakIdx};
        else
            peakInf_node_notLeaf_all{end+1} = peakInf_node_all{peakIdx};
        end
    end


    % 对 叶子节点 进行排序
    % 按照 峰值 从大到小 排列
    am_all = [];
    for peakIdx=1:length(peakInf_node_isLeaf)
        am_all(peakIdx) = peakInf_node_isLeaf{peakIdx}.am;
    end
    [temp sort_idx] = sort(am_all,'descend');
    peakInf_node_isLeaf_sort_am = {};
    for i=1:length(peakInf_node_isLeaf)
        peakInf_node_isLeaf_sort_am{i} = peakInf_node_isLeaf{sort_idx(i)};
    end

    % 按照 每像素平均能量 从大到小 排列
    energy_sum_all = [];
    for peakIdx=1:length(peakInf_node_isLeaf)
        energy_sum_all(peakIdx) = peakInf_node_isLeaf{peakIdx}.energy_sum;
    end
    [temp sort_idx] = sort(energy_sum_all,'descend');
    peakInf_node_isLeaf_sort_energy_sum = {};
    for i=1:length(peakInf_node_isLeaf)
        peakInf_node_isLeaf_sort_energy_sum{i} = peakInf_node_isLeaf{sort_idx(i)};
    end

    if my_trace
        % 独立显示各个局部峰值区域。
        plot_peak_num = 0;
        for peakIdx=1:plot_peak_num
            area =  peakInf_node_isLeaf_sort_energy_sum{peakIdx}.area;
            my_map_node = my_map.*area;
            fidx= fidx+1;figure(fidx);
            contour(my_map_node,v);grid on;
            title(['第 ' num2str(peakIdx) ' 个局部峰值区域']);
        end
    end

    return [peakInf_node_isLeaf_sort_am,peakInf_node_isLeaf_sort_energy_sum,peakInf_node_isLeaf,peakInf_node_all]

