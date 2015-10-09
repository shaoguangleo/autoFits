import math

def comp2uv(x_fit,uv_data):
    # model fit
    # radio of radian to millisecond
    rtomas =2.062648062470963551564733573307786131966597008796332528822e+8
    # radio of radian to degree
    # rtod =57.29577951308232087679815481410517033240547246656458
    # x_fit format [Flux, x0, y0, Major, Minor, Phi(deg)]
    # x_fit format [   1,  2,  3,     4,     5,        6]
    # x_fit = [0,0,0,0,0,0]
    flux = 0.0
    x0   = 0.0
    y0   = 0.0
    major= 0.0
    ratio= 0.0
    phi  = 0.0
    if len(x_fit) == 6 :
        flux = x_fit[0]
        x0   = x_fit[1]
        y0   = x_fit[2]
        major= x_fit[3]
        ratio= x_fit[4]
        phi  = x_fit[5]

    x0 /= rtomas
    y0 /= rtomas
    major /= rtomas

#    print 'uv data len is %d' % len(uv_data)
#    print type(uv_data)
#    print uv_data[0]
    #for i in range(uv_data):
    for i in uv_data:
        # Pick up the uv info
        #print i
        #uu = uv_data.split(',')[0]
        #vv = uv_data.split(',')[1]
        uu = float(i.split(',')[0])
        vv = float(i.split(',')[1])

        # Component phase
        cmpphs = 2 * math.pi * (uu * x0 + vv * y0)
        sinphi = math.sin(phi)
        cosphi = math.cos(phi)

        # Calculate the UV radian for ellipse strength
        tempa = (uu * cosphi - vv * sinphi) * ratio
        tempb = (uu * sinphi + vv * cosphi)
        uvrad = math.pi * major * math.sqrt((tempa * tempa + tempb * tempb))
        # Here is default value
        si = 1
        pb = 1
        flux_xu = flux * si * pb

        if uvrad < 1.0e-9:
            uvrad = 1.0e-9

        # There are a lot of calculate model component
        # Here we use the M_GAUS type
        if uvrad < 12.0:
            cmpamp = flux_xu * math.exp(-0.3606737602 * uvrad * uvrad)
        else:
            cmpamp = 0.0

        cmpre = cmpamp * math.cos(cmpphs)
        cmpim = cmpamp * math.sin(cmpphs)

        uv_re_im_fit = []
        uv_re_im_fit.append(cmpre)
        uv_re_im_fit.append(cmpim)
        return uv_re_im_fit
