def get_uv_bin(uvb,uu,vv):
    # If the point is in the unmapped -ve U part of the UV plane,
    # switch to the mapped conjugate-symmetric pixel.
    if uu >= 0:
        uu = -uu
        vv = -vv
    #  Determine the position in the bin array wrt its U=0,V=0 origin.
    #  binpix = uvb->nu * (uvb->nv/2 + floor(vv * uvb->vtopix + 0.5)) +
    #  floor(uu * uvb->utopix + 0.5);
    binpix = uvb.nu * (uvb.nv/2 + floor(vv * uvb.vtopix + 0.5)) + floor(uu * uvb.utopix + 0.5);
    # binpix_matlab = binpix +1;
    return binpix + 1
