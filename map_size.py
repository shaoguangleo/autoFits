import all_class

def map_size(nx,xinmap):
    # Setting the size of image
    # here refer from the uv_limits function in  uvinvert.c in difmap
    # Radio radian to millisecond
    rtomas =2.062648062470963551564733573307786131966597008796332528822e+8
    nmask = 0
    my_units = all_class.units()

    # Return the max U and V axis in current map pixel
    xinc = xinmap/rtomas;
    uinc = 1.0/(xinc*nx);
    u_limit = uinc*(nx/4-nmask);

    # Calculate the parameters of U
    my_units.nx = nx;
    my_units.xinc = xinc;
    my_units.uinc = uinc;
    my_units.u_limit = u_limit;

    # Calculate the parameters of V
    my_units.ny = nx;
    my_units.yinc = xinc;
    my_units.vinc = uinc;
    my_units.v_limit = u_limit;

    # Setting the inmap
    my_units.xinmap = xinmap;
    yinmap = xinmap;
    my_units.yinmap = yinmap;

    my_units.binwid=2;

    return my_units
