# The main function to auto model fit
import load_uvsel_uv
import string # for string.atof
import math # for cos and sin
import comp2uv_multi
import cart2pol
#import copy
import map_size
import all_class

# Default setting #
# uv data for modelfit
uv_filename   = './input/1730-130.u.2009_12_10.uvf.txt'
# fits image data for plot
fits_filename ='./input/1730-130.u.2009_12_10.icn.fits'

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
    '''
    print len(uv_data_phs)
    print len(uv_data_amp)
    print '*'*40
    print (uv_data_phs)
    print '*'*40
    print (uv_data_amp)
    '''
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
