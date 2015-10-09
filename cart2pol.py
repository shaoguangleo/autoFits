import math
import numpy
#Transform Cartesian coordinates to polar or cylindrical
def cart2pol(x,y):
    r = math.sqrt(x * x + y * y)
    theta = numpy.arctan(float(x)/float(y))
    return [theta,r]
