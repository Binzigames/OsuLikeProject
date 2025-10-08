#---------------------------------> importing
import pyray as pr
import sys
import time

import src.engine.NoteManager as Mn
import src.ui.gameFragments as gF

ui = gF.InGameMenus()

#---------------------------------> bools
song_start_time = None
current_tab_index = 0
time_per_step = 0.5


#---------------------------------> game draw
def draw_game():
    global current_tab_index

    ui.handle_input()
    ui.update_notes()
    ui.draw_notes()

    # >reading tabs
    elapsed = time.time() - song_start_time
    if current_tab_index < len(Mn.CurentTaba):
        step_time = current_tab_index * time_per_step

        if elapsed >= step_time:
            for note in Mn.CurentTaba[current_tab_index]:
                ui.spawn_note(note)
            current_tab_index += 1


#---------------------------------> main - game functions
def when_game_start(Wx, Wy, Wname):
    global song_start_time, current_tab_index
    pr.init_window(Wx, Wy, Wname)
    pr.set_target_fps(60)
    song_start_time = time.time()
    current_tab_index = 0


def game_cycle():
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    draw_game()
    pr.end_drawing()


def game_exit():
    pr.close_window()
    sys.exit(0)