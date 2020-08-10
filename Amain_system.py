import os
import random as rd
import shutil

import matplotlib.pyplot as plt
import numpy as np

import Aspace_gen as sp
import Bcel_body as cel
import properties_gen as prop




def del_old_states(x):
    folder = x
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def star_system_plot(size, num_star, num_planet, cids, cidp):
    xmin, xmax, ymin, ymax = (0, size, 0, size)
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 10)
    ax.set_facecolor("k")
    ax.set_aspect('equal')
    ax.set_xlim(left=xmin, right=xmax)
    ax.set_ylim(bottom=ymin, top=ymax)
    sp.star_plot(2000, 0)
    radiusset = []
    for i in range(0, num_star):
        letter = "ABCDEFG"[i]
        color = cids[i][1]
        print(color)
        cel.star_color(color)
        for k in range(0, len(color)):
            color[k] = color[k] / 256
        radius = int(max(rd.gauss(10, 10), 15))
        radiusset.append(radius)
        var = int(max(rd.gauss(50 * radius, 10), 15))
        gridsize = 10 * radius
        coord = np.zeros((gridsize, gridsize))
        listcoord = coord.tolist()
        posx = rd.uniform(0.4 * size, 0.6 * size)
        posy = rd.uniform(0.4 * size, 0.6 * size)
        x = np.arange(posx, posx + gridsize, 1)
        y = np.arange(posy, posy + gridsize, 1)
        plt.text(x[0] + 2 * radius + 40, y[0] + 2 * radius + 40, "Star {}".format(letter), color=color, fontsize=20)
        for indexy in range(0, gridsize):
            for indexx in range(0, gridsize):
                distance = np.sqrt((indexx - gridsize / 2) ** 2 + (indexy - gridsize / 2) ** 2)
                if distance < radius:
                    b = 1
                elif distance >= radius:
                    b = prop.normal_pdf(distance - radius, 0, var)
                listcoord[indexy][indexx] = listcoord[indexy][indexx] + b
        star = np.asarray(listcoord, dtype=np.float32)
        main_star = plt.pcolormesh(x, y, star, cmap="star", vmin=0, vmax=1, edgecolor="none", rasterized=True, zorder=2)
    for j in range(0, num_planet):
        letter = "abcdefg"[j]
        color = cidp[j][1]
        cel.planet_color(color)
        for k in range(0, len(color)):
            color[k] = color[k] / 256
        radius = int(max(rd.gauss(10, 0.5), 2))
        var = int(max(rd.gauss(50 * radius, 2 * radius), 10))
        posx = rd.uniform(0.2 * size, 0.8 * size)
        posy = rd.uniform(0.2 * size, 0.8 * size)
        gridsize = 70 * radius
        coord = np.zeros((gridsize * 5, gridsize * 5))
        listcoord = coord.tolist()
        x = np.arange(posx, posx + gridsize, 0.2)
        y = np.arange(posy, posy + gridsize, 0.2)
        plt.text(x[0] + 2 * radius + 40, y[0] + 2 * radius + 40, "Planet {}".format(letter), color=color, fontsize=20)
        for indexy in range(0, gridsize):
            for indexx in range(0, gridsize):
                distance = np.sqrt((indexx - gridsize / 2) ** 2 + (indexy - gridsize / 2) ** 2)
                if distance < radius:
                    b = 1
                elif distance >= radius:
                    b = prop.normal_pdf(distance - radius, 0, var)
                listcoord[indexy][indexx] = listcoord[indexy][indexx] + b
        star = np.asarray(listcoord, dtype=np.float32)
        main_star = plt.pcolormesh(x, y, star, cmap="planet", vmin=0, vmax=1, edgecolor="none", rasterized=True,
                                   zorder=2)
    plt.axis(False)
    plt.savefig("E:\Python projects\Python Resource\spacebot\system_image\system.png", facecolor="black", bbox_inches='tight', edgecolor="none")
    max_radius = max(radiusset)
    angular_radius = max_radius * 10 * np.pi / 180000  # Radian
    return angular_radius


def system_report(ang_size, ns, nump):
    date = 1
    heading = "Day {}".format(date)
    reach = "Astra has deactivated the warp drive and reached the targeted star system."
    ang_minute = ang_size * 180 * 60 / np.pi  # Arc minute
    ang_minute = float("{0:.2f}".format(ang_minute))
    angular_size = "The largest star's angular size as measured from Astra: {} arcminutes".format(ang_minute)
    radset = []
    for n in range(1, ns + 1):
        chk = open("E:\Python projects\Python Resource\spacebot\save_states\states_star{}.txt".format(str(n)), "r").readlines()
        for line in chk:
            if "Radius: " in line:
                str_radius = line
                radius = ""
                for v in range(0, len(str_radius)):
                    if str_radius[v] in ["0", "1", "2", '3', '4', '5', '6', '7', '8', '9', '.']:
                        radius = radius + str_radius[v]
                radius = float(radius)
                radset.append(radius)
                break
    maxrad = max(radset)
    d = (maxrad * 6.96E8) / (np.tan(ang_size / 2) * 1.5E11)
    d = float("{0:.2f}".format(d))
    distance = "Distance from the system's center: {} AU".format(d)
    bot_work = "Astra Assistant has gathered information of the system."
    text_holder = "\n \n"
    sys_info = "---- System Information ----"
    design = prop.designation()
    desig = "System designation: {}".format(design)
    comm = "Common name (in Terrisiac): {}".format(prop.common_name())
    num_sta = "Number of stars: {}".format(ns)
    st_list = ""
    for h in range(0, ns):
        st_name = design + "ABCDEFGHI"[h]
        if h != ns - 1:
            st_name += ", "
        st_list += st_name
    star_list = "List of stars: {}".format(st_list)
    num_pla = "Number of planets: {}".format(nump)
    pl_list = ""
    for h in range(0, nump):
        pl_name = design + "abcdefghi"[h]
        if h != nump - 1:
            pl_name += ", "
        pl_list += pl_name
    pla_list = "List of planets: {}".format(pl_list)
    text_holder2 = "\n"
    choice = "Captain, where would you like to explore next? \nComment the star label (eg. A or B)"
    choice2 = "or the planet label (eg. a or b) or type NEXT to warp to the next system."
    save_name = "E:\Python projects\Python Resource\spacebot\save_states/states_system.txt"
    save_star = open(save_name, "w")
    lineset = [heading, reach, angular_size, distance, bot_work, text_holder, sys_info, desig, comm, num_sta, star_list,
               num_pla,
               pla_list, text_holder2, choice, choice2]
    for [i, line] in zip(range(0, len(lineset)), lineset):
        save_star.writelines("{}\n".format(line))
    save_star.close()


def generate_star_system(s):
    del_old_states("save_states")
    del_old_states("system_image")
    system_designation = prop.designation()
    star, planet, new_star, new_planet = [], [], 1, 1
    ns, np = 0, 0
    color_star, color_planet = [], []
    while new_star != 0 and len(star) < 4:
        star.append(1)
        new_star = rd.choices([1, 0], weights=[0.3, 0.7], k=1)[0]
    while new_planet != 0 and len(planet) < 4:
        planet.append(1)
        new_planet = rd.choices([1, 0], weights=[0.3, 0.7], k=1)[0]
    while len(star) != 0:
        ns += 1
        star_seed = s * 1000 + ns
        a = sp.full_star_gen(star_seed, ns, system_designation)
        color_id_star = [ns, a]
        color_star.append(color_id_star)
        del star[0]
    while len(planet) != 0:
        np += 1
        planet_seed = s * 100000 + np
        b = sp.full_planet_gen(planet_seed, np, system_designation)
        color_id_planet = [np, b]
        color_planet.append(color_id_planet)
        del planet[0]
    ang_size = star_system_plot(2000, ns, np, color_star, color_planet)
    system_report(ang_size,ns,np)


# star_system_plot(2000,3,2)


# replace_line("save_states.txt", 1, newseed)

# print(save.read())
