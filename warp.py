import numpy as np
import matplotlib.pyplot as plt
import random as rd

def warp():
    fig, ax = plt.subplots()
    ax.set_xlim(left=-1, right=1)
    ax.set_ylim(bottom=-1, top=1)
    ax.set_aspect('equal')
    fig.set_facecolor('k')
    fig.set_size_inches(10, 10)
    number = 800
    x = np.random.rand(number) * 2 - 1
    y = np.random.rand(number) * 2 - 1
    posset = []
    warpposset = []
    for n in range(0, number):
        position = [x[n], y[n]]
        posset.append(position)
    for pos in posset:
        angle = "empty"
        if pos[0] >= 0:
            angle = np.arctan(pos[1] / pos[0])
        elif pos[0] < 0:
            angle = np.arctan(pos[1] / pos[0]) + np.pi
        radius = np.sqrt(pos[0] ** 2 + pos[1] ** 2)
        radius += 0.4 * radius ** 2  # Set warped radius
        warpx = radius * np.cos(angle)
        warpy = radius * np.sin(angle)
        warppos = [warpx, warpy]
        warpposset.append(warppos)
    for m in range(0, number):
        xpos = [posset[m][0], warpposset[m][0]]
        ypos = [posset[m][1], warpposset[m][1]]
        ax.plot(xpos, ypos, color="#ECFAFF")
    plt.axis(False)
    fig.savefig("warp.png", dpi=200, facecolor="k", bbox_inches='tight', edgecolor="none")
