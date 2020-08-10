import numpy as np
import matplotlib.pyplot as plt
import random as rd
import matplotlib.cm as cm
import Bcel_body as cel
import properties_gen as prop

# Build the main picture

cm.register_cmap(name='trans_blue',
                 data={'red': [(0, 0, 0),
                               (0.5, 8 / 256, 8 / 256),
                               (1, 1, 1)],

                       'green': [(0, 0, 0),
                                 (0.5, 48 / 256, 48 / 256),
                                 (1, 1, 1)],

                       'blue': [(0, 0, 0),
                                (0.5, 107 / 256, 107 / 256),
                                (1, 1, 1)],

                       'alpha': [(0, 0, 0),
                                 (50 / 256, 0, 1),
                                 (1, 1, 1),
                                 ]})


def star_plot(size, r):
    possetx, possety = [], []
    N = 1000  # Number of stars
    for i in range(0, N):
        posx = rd.uniform(0, size)
        posy = rd.uniform(0, size)
        d = np.sqrt((posx - size / 2) ** 2 + (posy - size / 2) ** 2)
        if d < r:
            pass
            # print(d)
        elif d >= r:
            possetx.append(posx)
            possety.append(posy)
    for (posx, posy) in zip(possetx, possety):
        var = int(max(rd.gauss(10, 5), 5))
        gridsize = 4 * var
        coord = np.zeros((gridsize, gridsize))
        listcoord = coord.tolist()
        x = np.arange(posx, posx + gridsize, 1)
        y = np.arange(posy, posy + gridsize, 1)
        for indexy in range(0, gridsize):
            for indexx in range(0, gridsize):
                radius = np.sqrt((indexx - gridsize / 2) ** 2 + (indexy - gridsize / 2) ** 2)
                b = prop.normal_pdf(radius, 0, var)
                listcoord[indexy][indexx] = listcoord[indexy][indexx] + b
        halo = np.asarray(listcoord, dtype=np.float32)
        bgstar = plt.pcolormesh(x, y, halo, cmap="trans_blue", vmin=0, vmax=1)
        # plt.colorbar(bgstar, ax=ax)


def full_star_gen(s, ns, designation):
    rd.seed(s)
    size = 2000  # Map size
    xmin, xmax, ymin, ymax = (0, size, 0, size)
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 10)
    ax.set_facecolor("k")
    ax.set_aspect('equal')
    ax.set_xlim(left=xmin, right=xmax)
    ax.set_ylim(bottom=ymin, top=ymax)
    color_s = cel.main_star(designation, ns, size, False)
    star_plot(size, 400)
    plt.axis(False)
    print("render completed")
    picname = "E:\Python projects\Python Resource\spacebot\system_image/star{}.png".format(ns)
    fig.savefig(picname, dpi=200, facecolor="k", bbox_inches='tight', edgecolor="none")
    # plt.show()
    return color_s


def full_planet_gen(s, np, designation):
    rd.seed(s)
    size = 2000  # Map size
    xmin, xmax, ymin, ymax = (0, size, 0, size)
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 10)
    ax.set_facecolor("k")
    ax.set_aspect('equal')
    ax.set_xlim(left=xmin, right=xmax)
    ax.set_ylim(bottom=ymin, top=ymax)
    color_p = cel.planet(designation, np, size)
    star_plot(size,300)
    plt.axis(False)
    print("render completed")
    picname = "E:\Python projects\Python Resource\spacebot\system_image/planet{}.png".format(np)
    fig.savefig(picname, dpi=200, facecolor="k", bbox_inches='tight', edgecolor="none")
    # plt.show()
    return color_p
