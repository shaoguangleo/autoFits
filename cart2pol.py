#!/usr/bin/env python
"""
This script will transform cartesian coordinates to polar or cylindrical
@version:1.0
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

import math
#import numpy as np
#Transform Cartesian coordinates to polar or cylindrical
def cart2pol(x,y):
    theta = math.atan2(float(y),float(x))
    r = math.hypot(float(x),float(y))
    return [theta,r]
