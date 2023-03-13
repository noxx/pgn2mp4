from pathlib import Path
import os
project_path =str(Path.cwd()) + "/" 
import configparser
import random


def get_pgn_database():
    print("You haven't entered a database, here is a list of databases:")
    database_names = [x for x in os.listdir(project_path+"input_pgns") if os.path.isdir(project_path+"input_pgns/"+x)]
    i = 1
    for database in database_names:
        print(str(i) + ") " + database)
        i += 1
    ans = int(input())
    return database_names[ans-1]

def get_reverse():
    print("Reverse board? (y or n) (default=n)")
    ans = input()
    if (ans=='n' or ans=='N' or ans=='no' or ans==''):
        return False
    if (ans=="y" or ans=="Y" or ans=="yes"):
        return True
    else:
        return get_reverse()


def get_duration():
    print("Duration inbetween moves: (default=0.5)")
    ans = input()
    default_duration = 0.5
    if (ans == ''):
        return default_duration
    else:
        return float(ans)


def get_theme():
    print("Choose a theme:")
    themes = [x for x in os.listdir(project_path+"assets/themes") if (x.endswith(".ini"))] 
    i=1
    for theme in themes:   
        print(str(i) + ") " + theme)
        i+=1
    print("m) Make manual theme")
    ans_theme = input()
    if (ans_theme != "m"):
        chosen_theme = themes[int(ans_theme)-1]
        config = configparser.ConfigParser()
        config.read(project_path+"assets/themes/" + chosen_theme)
        ws_color = config["DEFAULT"]["ws_color"]
        bs_color = config["DEFAULT"]["bs_color"]
        piece_set = config["DEFAULT"]["piece_set"]
        sound = config["DEFAULT"]["sound"]
        return ws_color, bs_color, piece_set, sound
    else:
        print("Chose square color")
        sqare_colors = [x for x in os.listdir(project_path+"assets/square_colors") if x.endswith(".ini")] 
        i=1
        for sq in sqare_colors:
            print(str(i) + ") " + sq)
            i+=1
        ans_sq = input()
        chosen_sq = sqare_colors[int(ans_sq)-1]
        config = configparser.ConfigParser()
        config.read(project_path+"assets/square_colors/" + chosen_sq)
        ws_color = config["DEFAULT"]["ws_color"]
        bs_color = config["DEFAULT"]["bs_color"]
        # taking piece_set
        print("Chose piece set")
        piece_sets = [x for x in os.listdir(project_path+"assets/pieces/pngs") if os.path.isdir(project_path+"assets/pieces/pngs/"+x)]
        i = 1
        for piece_set in piece_sets:
            print(str(i)+") " + piece_set)
            i+=1
        ans_ps = input()
        chosen_ps = piece_sets[int(ans_ps)-1]
        #taking sounds
        print("Chose sound")
        sounds = [x for x in os.listdir(project_path+"assets/sounds")]
        i = 1
        for sound in sounds:
            print(str(i)+") " + sound)
            i+=1
        ans_sound = input()
        chosen_sound = sounds[int(ans_sound)-1]
        return ws_color, bs_color, chosen_ps, chosen_sound

def get_output_folder(pgn_database, is_reverse, piece_set):
    default_output_folder = pgn_database+"_"+piece_set+"_"
    if (is_reverse):
        default_output_folder += "rev_"
    random_string = str(random.randrange(100, 999))
    default_output_folder += random_string

    print("Output folder name: (default="+default_output_folder+')')
    ans_output = input()
    if (ans_output == ""):
        return default_output_folder
    else:
        return  ans_output




