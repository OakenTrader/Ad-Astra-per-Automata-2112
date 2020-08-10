import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import random as rd
import properties_gen as prop


# Build the main star


def star_color(color):
    cm.register_cmap(name='star',
                     data={'red': [(0, 0, 0),
                                   (0.5, color[0] / 512, color[0] / 512),
                                   (0.9, 1, 1),
                                   (1, 1, 1)],

                           'green': [(0, 0, 0),
                                     (0.5, color[1] / 512, color[1] / 512),
                                     (0.9, 1, 1),
                                     (1, 1, 1)
                                     ],

                           'blue': [(0, 0, 0),
                                    (0.5, color[2] / 512, color[2] / 512),
                                    (0.9, 1, 1),
                                    (1, 1, 1)
                                    ],

                           'alpha': [(0, 0, 0),
                                     (10 / 256, 0, 0),
                                     (100 / 256, 1, 1),
                                     (1, 1, 1),
                                     ]}, lut=256)


def planet_color(color):
    cm.register_cmap(name='planet',
                     data={'red': [(0, 0, 0),
                                   (0.5, color[0] / 512, color[0] / 512),
                                   (1, color[0] / 256, color[0] / 256)],

                           'green': [(0, 0, 0),
                                     (0.5, color[1] / 512, color[1] / 512),
                                     (1, color[1] / 256, color[1] / 256)
                                     ],

                           'blue': [(0, 0, 0),
                                    (0.5, color[2] / 512, color[2] / 512),
                                    (1, color[2] / 256, color[2] / 256)
                                    ],

                           'alpha': [(0, 0, 0),
                                     (10 / 256, 0, 0),
                                     (100 / 256, 1, 1),
                                     (1, 1, 1),
                                     ]}, lut=256)


def main_star_plot(lum, size):
    radius = int(max(rd.gauss(300, 10), 15))
    var = int(max(rd.gauss(50 * radius * np.log10(lum + 3), 10), 15))
    gridsize = 10 * radius
    coord = np.zeros((gridsize, gridsize))
    listcoord = coord.tolist()
    x = np.arange((size - gridsize) / 2, (size + gridsize) / 2, 1)
    y = np.arange((size - gridsize) / 2, (size + gridsize) / 2, 1)
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
    # plt.colorbar(main_star, ax=ax)


def planet_plot(size):
    radius = int(max(rd.gauss(300, 10), 15))
    var = int(max(rd.gauss(150, 10), 15))
    gridsize = 10 * radius
    coord = np.zeros((gridsize, gridsize))
    listcoord = coord.tolist()
    x = np.arange((size - gridsize) / 2, (size + gridsize) / 2, 1)
    y = np.arange((size - gridsize) / 2, (size + gridsize) / 2, 1)
    for indexy in range(0, gridsize):
        for indexx in range(0, gridsize):
            distance = np.sqrt((indexx - gridsize / 2) ** 2 + (indexy - gridsize / 2) ** 2)
            if distance < radius:
                b = 1
            elif distance >= radius:
                b = prop.normal_pdf(distance - radius, 0, var)
            listcoord[indexy][indexx] = listcoord[indexy][indexx] + b
    star = np.asarray(listcoord, dtype=np.float32)
    main_star = plt.pcolormesh(x, y, star, cmap="planet", vmin=0, vmax=1, edgecolor="none", rasterized=True, zorder=2)
    # plt.colorbar(main_star, ax=ax)


def main_star(des, ns, size, planet):
    if not planet:
        designation, relative_mass, relative_luminosity, star_type, relative_radius, temperature, color, distance, spectral_class, abs_mag, app_m, parallax, rotation, eq_coord = prop.prop_gen(
            des, ns)
        star_color(color)
        main_star_plot(relative_luminosity, size)
        relative_mass, relative_luminosity, relative_radius, temperature, distance = prop.Round(
            [relative_mass, relative_luminosity, relative_radius, temperature, distance])
        reach = "After a short-range warp, we have reached the star {} and stabilized our orbit around it.".format(designation)
        bot_work = "Astra Assistant has gathered information of the star."
        placehold = "\r"
        heading = "---- Star information ----"
        repo1 = "Star designation: {}".format(designation)
        repo2 = "Mass: {} Solar mass".format(relative_mass)
        repo3 = "Luminosity: {} Solar luminosity".format(relative_luminosity)
        repo4 = "Type: {}".format(star_type)
        repo5 = "Radius: {} Solar radius".format(relative_radius)
        repo6 = "Surface Temperature: {} Kelvin".format(temperature)
        repo7 = "Spectral class: {}".format(spectral_class)
        repo8 = "Distance from Terris: {} Light years".format(distance)
        repo9 = "Absolute magnitude: {}".format(abs_mag)
        repo10 = "Apparent magnitude measured from Terris: {}".format(app_m)
        repo11 = "Parallax angle measured from Terris: {} Arcseconds".format(parallax)
        repo12 = "Rotation period: {} Terris days".format(rotation)
        repo13 = "Equatorial coordinates observed from Terris: Rise Ascension {} hours, Declination {} degrees".format(
            eq_coord[0], eq_coord[1])
        placehold2 = "\r"
        # choice = "Captain, where would you like to explore next? \nComment the star label (eg. A or B)"
        # choice2 = "or the planet label (eg. a or b) or type NEXT to warp to the next system."
        # print(repo1, repo2, repo3, repo4, repo5, repo6, repo7, repo8, repo9, repo10, repo11, repo12, repo13)
        save_name = "E:\Python projects\Python Resource\spacebot\save_states/states_star{}.txt".format(ns)
        save_star = open(save_name, "w")
        lineset = [reach, bot_work, placehold, heading, repo1, repo2, repo3, repo4, repo5, repo6, repo7, repo8, repo9, repo10, repo11, repo12,
                   repo13, placehold, placehold2]
        for [i, line] in zip(range(0, len(lineset)), lineset):
            save_star.writelines("{}\n".format(line))
        save_star.close()
        return color  # For plotting the system
    else:
        relative_mass = prop.rel_mass()
        star_type = prop.star_types(relative_mass)
        relative_radius = prop.rel_radii(relative_mass, star_type)
        relative_luminosity = prop.rel_luminosity(relative_mass)
        return relative_mass, relative_radius, relative_luminosity


def planet(des, np, size):
    relative_mass, relative_radius, relative_luminosity = main_star(des, 1, size, True)
    planet_designation, planet_type, planet_mass, planet_radius, planet_distance, surface_temp, planet_rotation, planet_orbit, planet_atm, planet_atm_pressure = prop.planet_prop_gen(
        np, des, relative_mass, relative_radius, relative_luminosity)
    color = prop.temp(1, 2, True)
    planet_color(color)
    planet_plot(size)
    planet_radius, planet_mass, surface_temp, planet_rotation, planet_orbit, planet_atm_pressure = prop.Round(
        [planet_radius, planet_mass, surface_temp, planet_rotation, planet_orbit, planet_atm_pressure])
    reach = "After a short-range warp, we have reached the planet {} and stabilized our orbit around it.".format(
        planet_designation)
    bot_work = "Astra Assistant has gathered information of the star."
    placehold = "\r"
    heading = "---- Planet Information ----"
    repo1 = "Planet designation: {}".format(planet_designation)
    repo2 = "Mass: {} Terris mass".format(planet_mass)
    repo4 = "Type: {}".format(planet_type)
    repo5 = "Radius: {} Terris radius".format(planet_radius)
    repo6 = "Surface Temperature: {} Kelvin".format(surface_temp)
    repo12 = "Rotation period: {} Terris days".format(planet_rotation)
    repo13 = "Orbital period: {} Terris years".format(planet_orbit)
    repo14 = "Atmospheric pressure at mean surface level: {} bars".format(planet_atm_pressure)
    if planet_type == "Gas planet":
        repo15 = "Atmosphere composition: \n {} : {}% \n {} : {}% \n {} : {}% \n {} : {}%".format(str(planet_atm[0][0]),
                                                                                              str(planet_atm[0][1]),
                                                                                              str(planet_atm[1][0]),
                                                                                              str(planet_atm[1][1]),
                                                                                              str(planet_atm[2][0]),
                                                                                              str(planet_atm[2][1]),
                                                                                              str(planet_atm[3][0]),
                                                                                              str(planet_atm[3][1]))
    elif planet_type == "Rocky planet":
        repo15 = "Atmosphere composition: \n {} : {}% \n {} : {}% \n {} : {}% \n {} : {}% \n {} : {}% ".format(
            str(planet_atm[0][0]),
            str(planet_atm[0][1]), str(planet_atm[1][0]),
            str(planet_atm[1][1]), str(planet_atm[2][0]), str(planet_atm[2][1]), str(planet_atm[3][0]),
            str(planet_atm[3][1])
            , str(planet_atm[4][0]), str(planet_atm[4][1]))
    else:
        repo15 = "Atmosphere composition: N/A"
    placehold2 = "\r"
    # choice = "Captain, where would you like to explore next? \nComment the star label (eg. A or B)"
    # choice2 = "or the planet label (eg. a or b) or type NEXT to warp to the next system."
    # print( repo1, repo2, repo4, repo5, repo6, repo12, repo13, repo14, repo15, placehold2, choice, choice2)
    save_name = "E:\Python projects\Python Resource\spacebot\save_states/states_planet{}.txt".format(np)
    save_star = open(save_name, "w")
    lineset = [reach, bot_work, placehold, heading, repo1, repo2, repo4, repo5, repo6, repo12, repo13, repo14, repo15, placehold2]
    for [i, line] in zip(range(0, len(lineset)), lineset):
        save_star.writelines("{}\n".format(line))
    save_star.close()
    return color # For plotting the system

# main_star()
# ax.set_aspect("equal")
# plt.axis(False)
# plt.show()
# fig.savefig('celestialbodies.png', bbox_inches="tight", facecolor="k")
