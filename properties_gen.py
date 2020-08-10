import random as rd
import numpy as np
import color_temp as ct


def Round(x):
    y = []
    for a in x:
        a = float("{0:.2f}".format(a))
        y.append(a)
    return y


def normal_pdf(x, mean, var):  # Normal Prob distribution function
    return np.exp(-(x - mean) ** 2 / (2 * var))


def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


# System properties
def designation():
    cstr, nstr = "", ""
    charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numset = '0123456789'
    char_chance = rd.gauss(0.8, 0.2)
    num_chance = rd.gauss(1.0, 0.1)
    while char_chance > 0:
        char = rd.choices(charset)[0]
        cstr += char
        char_chance -= 0.2
    while num_chance > 0:
        num = rd.choices(numset)[0]
        nstr += num
        num_chance -= 0.1
    des = "{}-{}".format(cstr, nstr)
    return des


def common_name():
    cstr = ""
    cap_charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cap = rd.choices(cap_charset)[0]
    charset = 'qwertyuiopasdfghjklzxcvbnm'
    char_chance = rd.gauss(0.8, 0.2)
    while char_chance > 0:
        char = rd.choices(charset)[0]
        cstr += char
        char_chance -= 0.2
    name = "{}{}".format(cap, cstr)
    return name


# Star properties ---- Relative to Solar properties

# mass
def designation_star(des, ns):
    # Add uppercase character to designation
    code = "ABCDEFG"[ns - 1]
    des += code
    return des


def rel_mass():
    low_mass = max(rd.gauss(5, 7), 0.08 + rd.gauss(0, 0.003))
    high_mass = max(rd.gauss(20, 7), 0.08)
    relative_mass = rd.choices([low_mass, high_mass], weights=[1, 0.3], k=1)[0]
    return relative_mass


# Luminosity
def rel_luminosity(relative_mass):
    relative_luminosity = "empty"
    if relative_mass < 0.4:
        relative_luminosity = 0.23 * relative_mass ** 2.3 + rd.gauss(0, 0.01 * relative_mass ** 2.3)
    elif 0.4 <= relative_mass < 2:
        relative_luminosity = relative_mass ** 4 + rd.gauss(0, 0.05 * relative_mass ** 4)
    elif 2 <= relative_mass < 55:
        relative_luminosity = 1.4 * relative_mass ** 3.5 + rd.gauss(0, 0.07 * relative_mass ** 3.5)
    elif relative_mass >= 55:
        relative_luminosity = 320000 * relative_mass + rd.gauss(0, 16000 * relative_mass)
    return relative_luminosity


# Type
def star_types(relative_mass):
    star_type = "empty"
    types = ["Red dwarf", "Main sequence", "Blue giant", "Red giant", "Blue supergiant", "Red supergiant", "Hypergiant",
             "White dwarf", "Brown dwarf",
             "Neutron star", "Black hole"]
    if relative_mass < 0.08:
        star_type = "Brown dwarf"
    if 0.08 <= relative_mass < 0.8:
        star_type = rd.choices(["Red dwarf", "White dwarf"], weights=[1, 0.3], k=1)[0]
    elif 0.8 <= relative_mass < 1.4:
        star_type = rd.choices(["Main sequence", "White dwarf", "Red giant"], weights=[1, 0.05, 0.1], k=1)[0]
    elif 1.4 <= relative_mass < 3:
        star_type = rd.choices(["Main sequence", "Neutron star", "Red giant"], weights=[1, 0.03, 0.2], k=1)[0]
    elif 3 <= relative_mass < 10:
        star_type = rd.choices(["Main sequence", "Black hole", "Red giant"], weights=[1, 0.03, 0.2], k=1)[0]
    elif 10 <= relative_mass < 30:
        star_type = rd.choices(["Main sequence", "Black hole", "Red giant", "Blue supergiant", "Red supergiant"],
                               weights=[1, 0.1, 0.4, 0.1, 0.1], k=1)[0]
    elif relative_mass >= 30:
        star_type = rd.choices(["Main sequence", "Black hole", "Blue supergiant", "Red supergiant"
                                   , "Hypergiant"], weights=[1, 0.7, 0.8, 0.7, 0.3], k=1)[0]
    return star_type


# Radius
def rel_radii(relative_mass, star_type):
    relative_radius = "empty"
    print(star_type)
    if star_type == "Brown dwarf":
        relative_radius = relative_mass + rd.gauss(0, 0.05 * relative_mass)
    if star_type == "Red dwarf":
        relative_radius = relative_mass + rd.gauss(0,
                                                   0.05 * relative_mass)  # Mass radius relation taken from wiki table
    elif star_type == "Main sequence":
        relative_radius = (relative_mass / 1.09) ** (1 / 1.28)  # Mass radius relation taken from wiki table
    elif star_type == "Red giant":
        relative_radius = max(9.05 + rd.gauss(0, 0.2), rd.gauss(30, 20) + rd.gauss(30, 10))
    elif star_type == "Blue supergiant":
        r1 = max(15 + rd.gauss(0, 0.3), rd.gauss(40, 20) + rd.gauss(10, 5))
        r2 = max(15 + rd.gauss(0, 0.3), rd.gauss(200, 50) + rd.gauss(50, 20))
        relative_radius = rd.choices([r1, r2], weights=[0.4, 0.6], k=1)[0]
    elif star_type == "Red supergiant":
        relative_radius = max(250 + rd.gauss(0, 10), rd.gauss(500, 100) + rd.gauss(100, 50))
    elif star_type == "Hypergiant":
        r1 = max(60 + rd.gauss(0, 5), rd.gauss(120, 20) + rd.gauss(40, 40))
        r2 = max(500 + rd.gauss(0, 10), rd.gauss(800, 100) + rd.gauss(200, 100))
        relative_radius = max(250 + rd.gauss(0, 10), rd.gauss(500, 100) + rd.gauss(100, 50))
    elif star_type == "White dwarf":
        relative_radius = 0.01 * (relative_mass + rd.gauss(0, 0.05)) ** (-1 / 3)  # Relationship taken from internet
    elif star_type == "Neutron star":
        relative_radius = 0.00000953333 / (relative_mass + rd.gauss(0, 0.05))  # Relationship taken from internet
    elif star_type == "Black hole":
        relative_radius = 0.00000404 * (relative_mass + rd.gauss(0, 0.05))  # Schwarzchild radius
    return relative_radius


# Temperature
def temp(relative_luminosity, relative_radius, planet):
    if not planet:
        temperature = (relative_luminosity * 3.83 * 10 ** 26 / (4 * np.pi * (relative_radius * 6.96 * 10 ** 8) ** 2
                                                                * 5.67 * 10 ** (-8))) ** 0.25
        temperature += rd.gauss(0, 0.05) * temperature
        color = ct.temp2rgb(temperature)
        return temperature, color
    else:
        temperature = 10 ** (rd.uniform(3.5, 4.4))
        color = ct.temp2rgb(temperature)
        return color


def distance(relative_mass):
    # Unit in light years
    if relative_mass < 2:
        d = max(4 + rd.gauss(0, 0.1), rd.gauss(80, 50))
    elif relative_mass >= 2:
        d = max(100 + rd.gauss(0, 3), rd.gauss(500, 100))
    return d


def spectral_class(temp):
    # Unit in Kevin
    if temp > 30000:
        spec = "O"
    elif 10000 < temp <= 30000:
        spec = "B"
    elif 7500 < temp <= 10000:
        spec = "A"
    elif 6000 < temp <= 7500:
        spec = "F"
    elif 5200 < temp <= 6000:
        spec = "G"
    elif 3700 < temp <= 5200:
        spec = "K"
    elif 2400 < temp <= 3700:
        spec = "M"
    return spec


def abs_m(relative_luminosity):
    # baseless
    M = -2.5 * np.log10(relative_luminosity * (3.826 / 3.0128) * (10 ** -2))
    M = float("{0:.2f}".format(M))
    return M


def app_mag(distance, abs_mag):
    # baseless
    m = abs_mag + 5 * np.log10(distance / 32.6)
    m = float("{0:.2f}".format(m))
    return m


def parallax(distance):
    # unit in arcsecond
    para = 3.26 / distance
    para = float("{0:.4f}".format(para))
    return para


def rotation_period(relative_radius):
    # unit in terris days
    p = np.exp(relative_radius / 20) * 28
    p = float("{0:.2f}".format(p))
    return p


def eq_coord():
    # Equatorial coordinates observed from Terris, unit in hours and degrees
    RA, DEC = rd.uniform(0, 24), rd.uniform(-90, 90)
    RA, DEC = float("{0:.2f}".format(RA)), float("{0:.2f}".format(DEC))
    return RA, DEC


def prop_gen(des, ns):
    designate = designation_star(des, ns)
    rel_m = rel_mass()
    rel_lum = rel_luminosity(rel_m)
    star_typ = star_types(rel_m)
    rel_radius = rel_radii(rel_m, star_typ)
    temper, col = temp(rel_lum, rel_radius, False)
    d = distance(rel_m)
    spec = spectral_class(temper)
    abso_m = abs_m(rel_lum)
    app_m = app_mag(d, abso_m)
    para = parallax(d)
    rotate = rotation_period(rel_radius)
    equatorial = eq_coord()
    return designate, rel_m, rel_lum, star_typ, rel_radius, temper, col, d, spec, abso_m, app_m, para, rotate, equatorial


# ------ Planet properties

def designation_planet(des, np):
    # Add lowercase character to system designation
    code = "abcdefghijklmnopqrstuvwxyz"[np - 1]
    des += code
    return des


def plan_type():
    x = rd.uniform(0, 1)
    if x > 0.5:  # Gas Planet
        planet_type = "Gas planet"
    elif x <= 0.5:
        planet_type = "Rocky planet"
    return planet_type


def plan_mass(planet_type):
    # Unit in Terris mass
    if planet_type == "Gas planet":  # Gas Planet
        planet_mass = max(rd.gauss(15, 1), rd.gauss(200, 100))
    elif planet_type == "Rocky planet":
        planet_mass = max(rd.gauss(0.01, 0.01), rd.gauss(1.5, 1))
    return planet_mass


def plan_radius(planet_type):
    # Unit in Terris radius
    if planet_type == "Gas planet":  # Gas Planet
        planet_radius = max(rd.gauss(5, 0.3), rd.gauss(30, 20))
    elif planet_type == "Rocky planet":
        planet_radius = max(rd.gauss(0.01, 0.01), rd.gauss(1.5, 1))
    return planet_radius


def plan_distance(relative_radius):
    # Unit in Astronomical Units
    d = max(relative_radius * (6.96 * 10 ** 5) / (1.5 * 10 ** 8) + rd.uniform(0.01, 0.1),
            rd.uniform(3, 80) + rd.gauss(1, 0.5))
    return d


def surf_temp(relative_luminosity, plan_distance):
    # Unit in Kevin
    T = ((relative_luminosity * 3.83 * 10 ** 26) * (1 - max(0.01, rd.gauss(0.4, 0.1))) / (
            (4 * np.pi * (plan_distance * 1.5 * 10 ** 11) ** 2) * (4 * 5.67 * 10 ** (-8)))) ** 0.25
    return T


def plan_rotate():
    # Unit in Terris day
    w = max(0.01, rd.gauss(10, 5))
    return w


def plan_orbit(plan_distance, relative_mass):
    # Kepler's third law, unit in Terris years
    P = np.sqrt(plan_distance ** 3 / relative_mass)
    return P


def atmosphere(planet_type):
    if planet_type == "Gas planet":
        cum_gas = 1
        H, He, Ch = ["Hydrogen gas", 0], ["Helium gas", 0], ["Methane", 0]
        gas = [H, He, Ch]
        for i in range(0, len(gas)):
            gas[i][1] = max(min(rd.gauss(0.7, 0.1), rd.gauss(0.9, 0.1) * cum_gas, cum_gas), 0)
            cum_gas -= gas[i][1]
        H[1], He[1], Ch[1] = Round([H[1]*100, He[1]*100, Ch[1]*100])
        other = 1 - H[1] - He[1] - Ch[1]
        if other < 0:
            other = 0
        other = ["Other", Round([other])[0]]
        comp = [H, He, Ch, other]
        print (comp)
        return comp
    if planet_type == "Rocky planet":
        cum_gas = 1
        CO2, N2, O2, H2O = ["Carbon Dioxide", 0], ["Nitrogen gas", 0], ["Oxygen gas", 0], ["Water vapor", 0]
        gas = [CO2, N2, O2, H2O]
        rd.shuffle(gas)
        for i in range(0, len(gas)):
            gas[i][1] = max(min(rd.gauss(0.5, 0.1), rd.gauss(0.8, 0.1) * cum_gas, cum_gas), 0)
            cum_gas -= gas[i][1]
            print(gas[i])
        CO2[1], N2[1], O2[1], H2O[1] = Round([CO2[1]*100, N2[1]*100, O2[1]*100, H2O[1]*100])
        other = 100 - CO2[1] - N2[1] - O2[1] - H2O[1]
        if other < 0:
            other = 0
        other = ["Other", Round([other])[0]]
        gas.append(other)
        print(gas)
        return gas


def pressure(relative_mass):
    # Unit in bars
    p = relative_mass ** 2.22 + rd.gauss(0, 0.1)
    if p <= 10 ** (-8):
        p = "trace"
    return p


def planet_prop_gen(np, designation, relative_mass, relative_radius, relative_luminosity):
    desig_planet = designation_planet(designation, np)
    planet_type = plan_type()
    planet_mass = plan_mass(planet_type)
    planet_radius = plan_radius(planet_type)
    planet_distance = plan_distance(relative_radius)
    surface_temp = surf_temp(relative_luminosity, relative_radius)
    planet_rotation = plan_rotate()
    planet_orbit = plan_orbit(planet_distance, relative_mass)
    atmospheric_comp = atmosphere(planet_type)
    atm_pressure = pressure(relative_mass)
    return desig_planet, planet_type, planet_mass, planet_radius, planet_distance, surface_temp, planet_rotation, planet_orbit, atmospheric_comp, atm_pressure
