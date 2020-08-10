import facebook
import Amain_system as ms
import os
import warp

current = "E:\Python projects\Python Resource\spacebot\game_states/current.txt"
unex_star = "E:\Python projects\Python Resource\spacebot\game_states/unexplored_star.txt"
unex_planet = "E:\Python projects\Python Resource\spacebot\game_states/unexplored_planet.txt"
dir_save_states = "E:\Python projects\Python Resource\spacebot\save_states"
warp_path = "E:\Python projects\Python Resource\spacebot\warp.png"
key_path = "E:\Python projects\Python Resource\spacebot/automata_key.txt"
system_states = "E:\Python projects\Python Resource\spacebot/save_states/states_system.txt"
dir_image = "E:\Python projects\Python Resource\spacebot/system_image"


def upload(message, access_token, img_path=None):
    graph = facebook.GraphAPI(access_token)
    if img_path:
        post = graph.put_photo(image=open(img_path, 'rb'), message=message)
    else:
        post = graph.put_object(parent_object='me', connection_name='feed', message=message)
    return graph, post['post_id']


def up_warp_initial():
    warp.warp()
    line1 = "Astra, the Terris first interstellar spacecraft, has finally launched into space to embark for a 100 days space journey."
    line2 = "The spacecraft immediately enter a long-range warp session which will send it to a nearby star system in 1 day (60 Facebook minutes)."
    message = "{}\r{}".format(line1, line2)
    token = open(key_path, "r")
    access_token = token.readlines()[0]
    token.close()
    upload(message, access_token, warp_path)
    c_state = open(current, "r")
    c_read = c_state.readlines()
    c_state.close()
    c_read[5] = str(1)
    c_state = open(current, "w")
    for line in c_read:
        c_state.writelines("{}".format(line))
    c_state.close()


def up_warp():
    warp.warp()
    message = "Having fully explored the star system, Astra departed from it via a long-range warp session bound for the new star syatem. \rIt will reach the new star system in 1 day (60 Facebook minutes)."
    token = open(key_path, "r")
    access_token = token.readlines()[0]
    token.close()
    upload(message, access_token, warp_path)
    c_state = open(current, "r")
    c_read = c_state.readlines()
    c_state.close()
    c_read[5] = str(1)
    c_state = open(current, "w")
    for line in c_read:
        c_state.writelines("{}\n".format(line))
    c_state.close()


# states = open("game_states/current.txt", "r")
#
# seed = "empty"
# save = open("save_states.txt", "r+")
# for i, line in enumerate(save):
#     if i == 0:
#         pass
#     elif i == 1:
#         seed = int(line)
#         break

def body_list(path):
    list = os.listdir(path)  # dir is your directory path
    file_s = open(unex_star, "w")
    file_p = open(unex_planet, "w")
    starlist = []
    planetlist = []
    for file in list:
        if "star" in file:
            starlist.append(file)
    for file in list:
        if "planet" in file:
            planetlist.append(file)
    for star in starlist:
        file_s.writelines("{}\n".format(star))
    for planet in planetlist:
        file_p.writelines("{}\n".format(planet))
    file_s.close()
    file_p.close()


def change_body():
    file_s = open(unex_star, "r")
    file_p = open(unex_planet, "r")
    read_s = file_s.readlines()
    read_p = file_p.readlines()
    file_s.close()
    file_p.close()
    if len(read_s) != 0:
        star_name = dir_save_states + "/{}".format(read_s[0])
        for n in range(0, 100):
            if str(n) in star_name:
                star_pic = "star{}.png".format(str(n))
                break
        del read_s[0]
        file_s = open(unex_star, "w")
        for file in read_s:
            file_s.writelines("{}\n".format(file))
        star_states = open(star_name, "r")
        read_star = star_states.readlines()
        message = {}
        for line in read_star:
            message += line
        token = open(key_path, "r")
        access_token = token.readlines()[0]
        token.close()
        img_star = dir_image + "/{}".format(star_pic)
        upload(message, access_token, img_star)
    elif len(read_s) == 0 and len(read_p) != 0:
        planet_name = dir_save_states + "/{}".format(read_p[0])
        for n in range(0, 100):
            if str(n) in planet_name:
                planet_pic = "planet{}.png".format(str(n))
                break
        del read_p[0]
        p = open(unex_planet, "w")
        for file in read_p:
            file_p.writelines("{}\n".format(file))
        planet_states = open(planet_name, "r")
        read_star = planet_states.readlines()
        message = {}
        for line in read_star:
            message += line
        token = open(key_path, "r")
        access_token = token.readlines()[0]
        token.close()
        img_star = dir_image + "/{}".format(planet_pic)
        upload(message, access_token, img_star)
    elif len(read_s) == 0 and len(read_p) == 0:
        time = 0
        clock(time)


def new_system():
    c_state = open(current, "r")
    read_c = c_state.readlines()
    old_seed = int(read_c[1])
    old_date = int(read_c[3])
    time = int(read_c[5])
    c_state.close()
    if old_date >= 100:
        end_journey()
    else:
        c_state = open(current, "w")
        new_seed = old_seed + 1
        new_date = old_date + 1
        line0 = "seed"
        line1 = str(new_seed)
        line2 = "day"
        line3 = str(new_date)
        line4 = "time"
        line5 = str(time)
        lineset = [line0, line1, line2, line3, line4, line5]
        for [i, line] in zip(range(0, len(lineset)), lineset):
            c_state.writelines("{}\n".format(line))
        ms.generate_star_system(new_seed)
        body_list(dir_save_states)


def end_journey():
    pass


def up_system():
    state = open(system_states, "r")
    r_state = state.readlines()
    state.close()
    message = ""
    for line in r_state:
        message += line
    token = open(key_path, "r")
    access_token = token.readlines()[0]
    token.close()
    img_sys = dir_image + "/system.png"
    upload(message, access_token, img_sys)


def clock(time):
    if time == 0:
        up_warp()
    elif time == 1:
        new_system()
        up_system()
        c_state = open(current, "r")
        c_read = c_state.readlines()
        c_state.close()
        c_read[5] = str(2)
        c_state = open(current, "w")
        for line in c_read:
            c_state.writelines("{}".format(line))
        c_state.close()
    elif time == 2:
        change_body()
    elif time == -1:
        up_warp_initial()


c_state = open(current, "r")
c_read = c_state.readlines()
c_state.close()
time = int(c_read[5])
clock(time)
