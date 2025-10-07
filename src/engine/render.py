#---------------------------------> importing
import pyray as pr
import sys

#---------------------------------> main - game functions
def when_game_start(Wx, Wy, Wname):
    pr.init_window(Wx, Wy, Wname)
    pr.set_target_fps(60)

def game_cycle():
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    pr.draw_text("Hello, Pyray!", 20, 20, 20, pr.RAYWHITE)
    pr.end_drawing()

def game_exit():
    pr.close_window()
    sys.exit(0)
