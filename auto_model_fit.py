#!/usr/bin/env python
"""
This script will plot
@version:0.9
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""
# The main function to auto model fit
import numpy as np
import load_uvsel_uv
import string # for string.atof
import math # for cos and sin
import comp2uv_multi
import cart2pol
#import copy
import map_size
import all_class
import maplot
#import scipy.ndimage.filters as filters
import guass
import matplotlib.pyplot as plt

# Default setting #
# uv data for modelfit
uv_filename   = './input/1730-130.u.2009_12_10.uvf.txt'
# fits image data for plot
fits_filename ='./input/1730-130.u.2009_12_10.icn.fits'

debug = 0 # if debug equal 1, will print verbose informations.
trace = 1

# Loading the visibility data
uv_data = []
uv_data = load_uvsel_uv.load_uvsel_uv(uv_filename)

# Reading the fits file for plot
# fits_data = fitsread(fits_filename)

# Get the uv weight value
weight_idx = 5

# Here to pick up uv data which the weight value is not equal to zero
uv_data_non_zero_wt = []
for i in uv_data:
    if string.atof(i.split(',')[4]) != 0.0 :
        uv_data_non_zero_wt.append(i)

# The following actually is not needed
# We can just put it together with the upline
uv_data_select =[]
for i in uv_data_non_zero_wt:
    uv_data_select.append(i)
print len(uv_data_select)
print len(uv_data_select[0])

# Read the sin and cos of amp
uv_re_im_read = [] # The total matrix
uv_re_im_read_wt = [] # The total matrix with weight
uv_re_im_temp = [] # every value include cos and sin
for i in uv_data_select:
    amp = string.atof(i.split(',')[2])
    ang = string.atof(i.split(',')[3])
    weight = string.atof(i.split(',')[4])
    icos = amp*math.cos(ang)
    isin = amp*math.sin(ang)
    uv_re_im_temp = [] # every value include cos and sin
    uv_re_im_temp.append(icos)
    uv_re_im_temp.append(isin)
    uv_re_im_read.append(uv_re_im_temp)
    uv_re_im_wt_temp = [] # every value include cos and sin
    uv_re_im_wt_temp.append(icos*math.sqrt(weight))
    uv_re_im_wt_temp.append(isin*math.sqrt(weight))
    uv_re_im_read_wt.append(uv_re_im_wt_temp)

for i in range(5):
    print uv_re_im_read[i]
for i in range(5):
    print uv_re_im_read_wt[i]

for cmp_num in range(6):
    x_fit_multi = []
    uv_re_im_fit_multi = []
    uv_re_im_fit_multi = comp2uv_multi.comp2uv_multi(x_fit_multi,uv_data_select)

    # Calculate the real and image part of UV data
    uv_data_re = []
    uv_data_im = []

    for i in range(len(uv_data_select)):
        amp = string.atof(uv_data_select[i].split(',')[2])
        ang = string.atof(uv_data_select[i].split(',')[3])
        weight = string.atof(uv_data_select[i].split(',')[4])
        icos = amp*math.cos(ang)
        isin = amp*math.sin(ang)
        uv_data_re.append(icos - uv_re_im_fit_multi[i][0])
        uv_data_im.append(icos - uv_re_im_fit_multi[i][1])

    uv_data_phs = []
    uv_data_amp = []
    # Here change the cartesian coordinates to polar
    for i in range(len(uv_data_re)):
        temp  = cart2pol.cart2pol(uv_data_re[i],uv_data_im[i])
        uv_data_phs.append(temp[0])
        uv_data_amp.append(temp[1])

    if debug:
        print len(uv_data_phs)
        print len(uv_data_amp)
        print '*'*40
        print (uv_data_phs)
        print '*'*40
        print (uv_data_amp)

    # Calculate the residual
    # And import the new amp&&phs infos
    #uv_data_residual = uv_data_select  => also the same list
    #uv_data_residual = copy.deepcopy(uv_data_select)
    #uv_data_residual = [[0 for col in range(len(uv_data_select[0].split(',')))] for row in range(len(uv_data_select))]
    uv_data_residual = [[0] for row in range(len(uv_data_select))]
    #print uv_data_select[i].split(',')
    for i in range(len(uv_data_select)):
        for j in range(len(uv_data_select[i].split(','))-1):
           #uv_data_residual[i].append(uv_data_select[i].split(',')[j])
           uv_data_residual[i].insert(j,uv_data_select[i].split(',')[j])
        uv_data_residual[i][2] = uv_data_amp[i]
        uv_data_residual[i][3] = uv_data_phs[i]
    print '*'*40
    print uv_data_residual[0]
    print '*'*40

    # Setting the maplot parameters
    nx = 1024
    ny = nx
    xinmap = 0.1
    yinmap = xinmap
    domap = 1
    my_units = all_class.units()
    my_units = map_size.map_size(nx,xinmap)
    print my_units.xinc

    #########
    #TTTTTToooDO
    map_org = maplot.maplot(uv_data_residual,my_units,domap)

    #Setting the filtering intensity based on the beam
    map_re = np.real(map_org)

    #Gussian filtering
    hsize = 20
    sigma = 10

    #filt = filters.gaussian_filter(hsize,sigma)
    filt = guass.fspecial_gauss(hsize,sigma)

    if debug:
        print '-'*80 + 'filt is'
        print filt
        print '-'*80


    map_filt = np.convolve(map_re,filt,'same')
    map_positive = map_filt - min(map_filt)
    map_normal = map_positive/max(map_positive)
    my_map = map_normal

    if trace ==1:
        fidx=fidx+1;
        plt.figure(fidx);
        plt.imshow(my_map./max(my_map(:)));
        plt.title('maplot(), map image');

    '''


    [peakInf_node_isLeaf_sort_am,peakInf_node_isLeaf_sort_energy_sum,peakInf_node_isLeaf,peakInf_node_all] =my_find_peaks(my_map);

    %%
    % Found the highest point in the image
    % [x0_pix, y0_pix] is the axis of highest point, unit:pixel, axis original point locate left-up corner
    %     my_map_max = max(my_map(:));
    %     [c r] = find(my_map>=my_map_max);
    %     y0_pix= c(1);
    %     x0_pix= r(1);
    centerPos = peakInf_node_isLeaf_sort_am{1}.centerPos;
    y0_pix = centerPos(1);
    x0_pix = centerPos(2);
    %%
    % change the axis[x0_mas,y0_mas] unit: mas,axis original point in the image center
    y0_mas = -1*(yinmap*(y0_pix - (ny/2+1)));
    x0_mas = -1*(xinmap*(x0_pix - (nx/2+1)));
    %%
    % using the highest point [x0_mas,y0_mas] to init x_fit_new_cmp
    x_fit_new_cmp = [1,x0_mas,y0_mas,1,1,0];
    x_fit_new_cmp_int = x_fit_new_cmp
    %%
    % save the inter-result to comp_filename
    comp_filename = './2.output/xu_comps.txt';
    headInfo = {};
    headInfo{end+1} = ['uv_filename = ' uv_filename];
    headInfo{end+1} =  datestr(now,0);
    headInfo{end+1} = ' x_fit_new_cmp_int ';
    my_save_comps(x_fit_new_cmp_int,comp_filename,headInfo);

    uv_re_im_fit_multi_wt = my_comp2uv_multi_wt(x_fit_multi,uvData_select);
    residual_xu_wt = uv_re_im_read_wt - my_comp2uv_multi_wt(x_fit_multi,uvData_select);

    % modelfit for new cmp
    x_fit_new_cmp(5)=1;
    x_fit_new_cmp(6)=0;
    x_fit_new_cmp(1)=abs(x_fit_new_cmp(1));
    x_fit_new_cmp(4)=abs(x_fit_new_cmp(4));
    options = optimset('MaxIter',50);
    [x_fit_new_cmp,resnorm,residual,exitflag,output] = ...
        lsqcurvefit(@my_comp2uv_multi_wt,x_fit_new_cmp,uvData_select,residual_xu_wt,[],[],options);
chi_square = resnorm/(size(uvData_select,1)*2-cmp_num*4+2)

    comp_filename = './2.output/xu_comps.txt';
    headInfo = {};
    headInfo{end+1} = ['uv_filename = ' uv_filename];
    headInfo{end+1} =  datestr(now,0);
    headInfo{end+1} = ' x_fit_new_cmp ';
    headInfo{end+1} = sprintf('chi_square = %0.5e',chi_square);
    my_save_comps(x_fit_new_cmp,comp_filename,headInfo);

    x_fit_new_cmp(5)=1;
    x_fit_new_cmp(6)=0;
    x_fit_new_cmp(1)=abs(x_fit_new_cmp(1));
    x_fit_new_cmp(4)=abs(x_fit_new_cmp(4));
    x_fit_multi = [x_fit_multi x_fit_new_cmp ];
    x_fit_new_cmp
    % modelfit for all cmp

    options = optimset('MaxIter',100);
    %optimistic Gussian Model
    [x_fit_multi,resnorm,residual,exitflag,output] = ...
        lsqcurvefit(@my_comp2uv_multi_wt,x_fit_multi,uvData_select,uv_re_im_read_wt,[],[],options);
%    lsqcurvefit(@my_comp2uv_multi_wt,x_fit_multi,uvData_select,uv_re_im_read_wt);

    cmp_num
    x_fit_multi_array = reshape(x_fit_multi,6,cmp_num)'
    chi_square = resnorm/(size(uvData_select,1)*2-cmp_num*4+2)


    headInfo = {};
    headInfo{end+1} = ['uv_filename = ' uv_filename];
    headInfo{end+1} =  datestr(now,0);
    headInfo{end+1} = sprintf('chi_square = %0.5e',chi_square);
    my_save_comps(x_fit_multi_array,comp_filename,headInfo);

    fidx = fidx+1;
    my_color = [ 1.000 0.314 0.510 ];
    my_plot_fits(my_fits,fidx);
    my_plot_comp_all(x_fit_multi_array,my_units,fidx, my_color);
    '''