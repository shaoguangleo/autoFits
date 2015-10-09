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

