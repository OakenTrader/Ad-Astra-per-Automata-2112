import numpy as np
import matplotlib.pyplot as plt

# Temp to rgb algorithm from https://gist.github.com/paulkaplan/5184275 converted from javascript

def temp2rgb(K):
    temp = K / 100
    if temp <= 66:
        red = 255
        green = 95.4708025861 * np.log(temp) - 140.1195681661
        if temp <= 19:
            blue = 0
        else:
            blue = 132.5177312231 * np.log(temp - 10) - 305.0447927307
    else:
        red = 387.498727446 * (temp - 60) ** -0.1332047592
        green = 315.1221695283 * (temp - 60) ** -0.0755148492
        blue = 255
    r = min(max(red, 0), 255)
    g = min(max(green, 0), 255)
    b = min(max(blue, 0), 255)
    return [r, g, b]


def str2list(x):
    if type(x) == str:
        r = int(x[1] + x[2], 16)
        g = int(x[3] + x[4], 16)
        b = int(x[5] + x[6], 16)
        return [r, g, b]
    elif type(x) == list:
        return "#{:X}{:X}{:X}".format(int(round(x[0])), int(round(x[1])), int(round(x[2])))
    else:
        print('Type error')

# a = temp2rgb(33000)
# b = str2list(a)
# print(b)

# fig, ax = plt.subplots()
# ax.set_facecolor(b)
# plt.show()

