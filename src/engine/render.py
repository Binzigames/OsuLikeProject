#---------------------------------> importing
import pyray as pr
import sys
import time

from src.engine import NoteManager as Mn
from src.ui import gameFragments as gF
from src.auto_tab_generator import  generate_all_tabs_from_folder


#---------------------------------> globals
song_start_time = None


#---------------------------------> main initialization
def when_game_start(Wx, Wy, Wname):
    global menu
    pr.init_window(Wx, Wy, Wname)
    pr.set_target_fps(60)
    generate_all_tabs_from_folder()

#---------------------------------> main game loop
def game_cycle():
    while not pr.window_should_close():
        gF.update_ev()
        pr.begin_drawing()
        gF.draw_ev()
        pr.end_drawing()

    game_exit()


#---------------------------------> exit
def game_exit():
    pr.close_window()
    sys.exit(0)
