#---------------------------------> importing
import pyray as pr
import sys
import src.ui.gameFragments as gF

ui = gF.InGameMenus()

#---------------------------------> game draw
def draw_game():
    ui.update_notes()
    ui.draw_notes()

    if pr.is_key_pressed(pr.KeyboardKey.KEY_A):
        ui.spawn_note(0)
    if pr.is_key_pressed(pr.KeyboardKey.KEY_S):
        ui.spawn_note(1)
    if pr.is_key_pressed(pr.KeyboardKey.KEY_D):
        ui.spawn_note(2)
    if pr.is_key_pressed(pr.KeyboardKey.KEY_F):
        ui.spawn_note(3)

#---------------------------------> main - game functions
def when_game_start(Wx, Wy, Wname):
    pr.init_window(Wx, Wy, Wname)
    pr.set_target_fps(60)

def game_cycle():
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    draw_game()
    pr.end_drawing()

def game_exit():
    pr.close_window()
    sys.exit(0)
