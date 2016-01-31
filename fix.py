#!/usr/bin/env python
"""
This script equal the fix function
@version:0.9
@contact: sgguo@shao.ac.cn
@author:{Guo Shaoguang<mailto:sgguo@shao.ac.cn>}
"""

import math
def fix(number):
    # Round towards zero
    if number > 0:
        value = math.floor(number)
    elif number < 0:
        value = math.ceil(number)
    else:
        value = 0.0
    return value


if __name__ == '__main__':
    print fix(3.5)
    print fix(5.3)
