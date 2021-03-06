#!/usr/bin/env python
"""
This script will return uv grid information
@version:1.0
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

import all_class
import string
import numpy as np
import get_uv_bin

def uv_grid(uv_data,my_units,uvbin,uvb,gcf,domap):

#When difmap printing:
# if modamp_id = 5 conflict with weight's idx
# it needs to be modified 7
# modamp_idx = 7
# modphs_idx = 8
    modamp_idx = -1
    modphs_idx = -1
    weight_idx = 5

    #gcf = all_class.gcf()
    nmask = gcf.nmask
    tgtocg = gcf.tgtocg
    convfn = gcf.convfn
    rxft = gcf.rxft
    ryft = gcf.ryft

    #my_units = all_class.units()
    #set parameters for uvgrid
    nvgrid = my_units.ny
    nugrid = my_units.nx/2+1

    #  * Get a pointer to the real part of the pixel U=0,V=N/2
    #cntr_ptr_vector = zeros(1,2*nvgrid *(nugrid));
    #cntr_ptr_vector = [[0 for i in range(2*nvgrid*nugrid)] for j in range(5)]
    cntr_ptr_vector = [0 for i in range(2*nvgrid*nugrid)]

    uvmap =1
    cntr_ptr = uvmap + nvgrid * nugrid

    # for debug
    scale_xu = 1000000
    temp_uv_idx=0
    #testline = 100
    #traceData_matlab=[]

    wsum = 0
    for i in range(len(uv_data)):
        temp_uv_idx = temp_uv_idx+1
        if all_class.debug:
            print i
            print uv_data[i][weight_idx-1]
        #if string.atof(uv_data[i].split(',')[weight_idx-1]) > 0:
        if (uv_data[i][weight_idx-1]) > 0:
            #uu = string.atof(uv_data[i].split(',')[0])
            #vv = string.atof(uv_data[i].split(',')[1])
            uu = uv_data[i][0]
            vv = uv_data[i][1]
            if all_class.debug:
                print 'uu && vv'
                print i
                print uv_data[0]
                print uu
                print vv
                import time
                time.sleep(5)

            vis = all_class.vis()
            vis.amp = (uv_data[i][2]) * scale_xu
            vis.phs = (uv_data[i][3])
            if modamp_idx > 0 and modphs_idx >0 :
                vis.modamp = (uv_data[i][modamp_idx-1]) * scale_xu
                vis.modphs = (uv_data[i][modphs_idx-1])
            else:
                vis.modamp = 0
                vis.modphs = 0

            weight = 1
            binpix_matlab = get_uv_bin.get_uv_bin(uvb,uu,vv)
            #bc=uvbin[int(binpix_matlab)-1]
            bc=uvbin[int(binpix_matlab)]
            if all_class.debug:
                print 'binpix is',
                print binpix_matlab
                print 'bc is',
                print bc
            weight = weight*1.0/bc


            if domap:
                uvrval = vis.amp * np.cos(vis.phs) - vis.modamp * np.cos(vis.modphs)
                uvival = vis.amp * np.sin(vis.phs) - vis.modamp * np.sin(vis.modphs)
            else:
                uvrval = 1.0
                uvival = 0.0
            if all_class.debug:
                print domap
                print uvrval
                print uvival

            ufrc = uu / my_units.uinc   # /* Decimal pixel position */
            vfrc = vv / my_units.vinc
            upix = round(ufrc)          # Integer pixel position */
            vpix = round(vfrc)
            if all_class.debug:
                print ufrc
                print vfrc
                print upix
                print vpix

            #% * Loop through the interpolation area.
            for iv in range(int(vpix-nmask),int(vpix+nmask+1)):
            #% * Determine the value of the interpolation function along V at this pixel.
                distance_v = round(tgtocg*abs(iv-vfrc))
                fv = weight * convfn[int(distance_v)]

                #%  * Determine the increment in floats to move from v=N/2 to v=vpix+iv.
                #%  * The same increment with the opposite sign will take us to v=-N/2, (except
                #%  * when v=0 [see below]) hence the choice of U=0,V=N/2 as the reference point.
                #% vinc = nugrid*(iv+iv+((iv<0)?nvgrid:-nvgrid));
                if iv < 0:
                    vinc = nugrid*(iv+iv+nvgrid)
                else:
                    vinc = nugrid*(iv+iv-nvgrid)

                # Determine pointers to U=0,V=iv and U=0,V=-iv.

                normptr = cntr_ptr + vinc
                #%conjptr = cntr_ptr + ((iv) ? -vinc:vinc);
                if iv != 0:
                    conjptr = cntr_ptr + (-vinc)
                else:
                    conjptr = cntr_ptr + (vinc)

                for iu in range(int(upix-nmask),int(upix+nmask+1)):

                    #% * Combine the interpolation functions along U and V.
                    distance_u = round(tgtocg*abs(iu-ufrc))
                    fu = convfn[int(distance_u)]
                    fuv = fu*fv
                    if all_class.debug:
                        print distance_u
                        print 'fu and fv'
                        print fu
                        print fv
                    wsum = wsum+fuv
                    #% wsum += (fuv = fv * convfn[(int) (tgtocg*fabs(iu-ufrc)+0.5f)]);

                    #% * Calculate the real and imaginary parts of the interpolated
                    #% * and weighted UV data value.
                    rval = uvrval*fuv
                    ival = uvival*fuv
                    if all_class.debug:
                        print 'rval and ival'
                        print rval
                        print ival
                        print uvrval
                        print uvival
                        print fuv
                    #% * Pixel iu,iv may be inside the array or in the non-existent
                    #% * conjugate other half of the array. If it is in the latter
                    #% * then we should put it at its conjugate symmetric position in
                    #% * the array - this also means that the gridded data value should be
                    #% * conjugated.
                    if iu <= 0:
                        rptr = conjptr-iu-iu # % /* Pointer to conjugate element */
                        #print rptr
                        #print len(cntr_ptr_vector)
                        #% *rptr += rval;
                        #% *(rptr+1) -= ival;
                        cntr_ptr_vector[rptr-1] = cntr_ptr_vector[rptr-1]+rval
                        cntr_ptr_vector[rptr] = cntr_ptr_vector[rptr]-ival
                    if(iu >= 0):
                        rptr = normptr+iu+iu #% /* Pointer to complex element */
                        #% *rptr += rval;
                        #% *(rptr+1) += ival;
                        cntr_ptr_vector[rptr-1] = cntr_ptr_vector[rptr-1]+rval
                        cntr_ptr_vector[rptr] = cntr_ptr_vector[rptr]+ival

                    '''% for debug
                    % 				 fprintf(fp_xu_trace, "uu,vv,uvrval,uvival,ufrc,vfrc,upix,vpix,1,temp_uv_idx= %10.10f,%10.10f,%10.10f,%10.10f,%10.10f,%10.10f,%d,%d,%d,%d,\n",
                    % 		                         uu,vv,uvrval,uvival,ufrc,vfrc,upix,vpix,1,temp_uv_idx);
                    % 				 float fu=fuv/fv;
                    % 				 fprintf(fp_xu_trace, "weight,fv,fu,fuv,wsum,1.0,iv,vinc,normptr-uvmap+1,conjptr-uvmap+1= %10.10f,%10.10f,%10.10f,%10.10f,%10.10f,%10.10f,%d,%d,%d,%d,\n",
                    % 		                         weight,fv,fu,fuv,wsum,1.0,iv,vinc,normptr-uvmap+1,conjptr-uvmap+1);
                    %
                    % 				 fprintf(fp_xu_trace, "rval,ival,*(rptr),*(rptr+1),1.0,1.0,iv,iu,rptr-uvmap+1,temp_uv_idx= %10.10f,%10.10f,%10.10f,%10.10f,%10.10f,%10.10f,%d,%d,%d,%d,\n",
                    % 		                         rval,ival,*(rptr),*(rptr+1),1.0,1.0,iv,iu,rptr-uvmap+1,temp_uv_idx);
                    %                 my_line = [uu,vv,uvrval,uvival,ufrc,vfrc,upix,vpix,1,temp_uv_idx];
                    %                 traceData_matlab(end+1,:)=my_line;
                    %
                    %                 my_line = [weight,fv,fu,fuv,wsum,1.0,iv,vinc,normptr,conjptr];
                    %                 traceData_matlab(end+1,:)=my_line;
                    %
                    %                 my_line = [rval,ival,cntr_ptr_vector(rptr),cntr_ptr_vector(rptr+1),1.0,1.0,iv,iu,rptr,temp_uv_idx];
                    %                 traceData_matlab(end+1,:)=my_line;

                end
            end
        end
    end
    % test_line = length(traceData_matlab);
    % traceData_diff = traceData_matlab(1:test_line,:) -traceData_difmap(1:test_line,:);
    % traceData_diff_ratio = traceData_diff(1:test_line,:)./traceData_difmap(1:test_line,:);
    % close all;
    % for j=10:-1:1; figure(j);plot(traceData_diff(1:3:end,j),'.');end
    % for j=10:-1:1; figure(100+j);plot(traceData_diff_ratio(1:3:end,j),'.');end
    '''
    #Here we read the result of cntr_ptr_vector
    #cntr_ptr_vector = np.genfromtxt('uvgrid.txt')
    #print 'cntr_ptr_vector is '
    #print cntr_ptr_vector

    #cntr_ptr_vector_array_real = reshape(cntr_ptr_vector(1:2:2*(nvgrid) * (nugrid)),nugrid,nvgrid)';
    #cntr_ptr_vector_array_real = np.reshape(cntr_ptr_vector[0:2*nvgrid*nugrid:2],(nugrid,nvgrid))
    cntr_ptr_vector_array_real = np.reshape(cntr_ptr_vector[0:2*nvgrid*nugrid:2],(nvgrid,nugrid))
    #print len(cntr_ptr_vector_array_real)
    #cntr_ptr_vector_array_real=np.transpose(cntr_ptr_vector_array_real)
    #print len(cntr_ptr_vector_array_real)

    #TODO The value of cntr_ptr_vector seem different
    # The reason is when read data from txt file ,the textscan in Matlab will lose data precision
    #So we will read value from file first
    #cntr_ptr_vector_array_imag = reshape(cntr_ptr_vector(2:2:2*(nvgrid) * (nugrid)),nugrid,nvgrid)';
    cntr_ptr_vector_array_imag = np.reshape(cntr_ptr_vector[1:2*nvgrid*nugrid:2],(nvgrid,nugrid))
    #cntr_ptr_vector_array_imag = np.transpose(cntr_ptr_vector_array_imag)
    import matplotlib.pyplot as plt
    plt.figure()
    plt.contour(cntr_ptr_vector_array_real)
    plt.savefig('real_part.png')
    plt.figure()
    plt.contour(cntr_ptr_vector_array_imag)
    plt.savefig('image_part.png')

    #cntr_ptr_vector_array = cntr_ptr_vector_array_real + 1j.*cntr_ptr_vector_array_imag;
    cntr_ptr_vector_array = np.zeros([nvgrid,nugrid],complex)
    #cntr_ptr_vector_array = np.zeros([nugrid,nvgrid],complex)
    if all_class.debug:
        print 'size'
        print np.size(cntr_ptr_vector_array_real)
        print 'length'
        print len(cntr_ptr_vector_array_real)
        print len(cntr_ptr_vector_array_real[0])
        print 'nugrid and nvgrid'
        print nugrid
        print nvgrid
    #print len(cntr_ptr_vector_array_imag[0])

    for i in range(nvgrid):
        for j in range(nugrid):
            #cntr_ptr_vector_array[i].append(complex(cntr_ptr_vector_array_real[i][j],cntr_ptr_vector_array_imag[i][j]))
            cntr_ptr_vector_array[i][j] = complex(cntr_ptr_vector_array_real[i][j],cntr_ptr_vector_array_imag[i][j])
#            cntr_ptr_vector_array[i][j] = np.complex(cntr_ptr_vector_array_real[i][j],cntr_ptr_vector_array_imag[i][j])
    #cntr_ptr_vector_array = complex(cntr_ptr_vector_array_real,cntr_ptr_vector_array_imag)
    # Error, cause will generate double complex
    #cntr_ptr_vector_array = np.array([cntr_ptr_vector_array_real,cntr_ptr_vector_array_imag],dtype=complex)

    if all_class.debug:
        for i in range(5):
            print 'real and image is '
            print cntr_ptr_vector_array_real[i][0],
            print cntr_ptr_vector_array_imag[i][0]
            #print cntr_ptr_vector_array.size
            #print cntr_ptr_vector_array[0].size
            print cntr_ptr_vector_array[0][i]
        #print '*'*80
        #print cntr_ptr_vector
        #print np.transpose(cntr_ptr_vector_array)
        #print '*'*80
        print 'NOW'
        #print len(cntr_ptr_vector)
        #print (cntr_ptr_vector[0])
        #print cntr_ptr_vector_array[0]
    return [cntr_ptr_vector,cntr_ptr_vector_array]
