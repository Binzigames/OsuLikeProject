#---------------------------------> connecting files
import src.engine.render as r
import src.data.data as d

#---------------------------------> logic
def run_game():
    r.when_game_start(d.Wx, d.Wy, d.Wname)

    try:
        while not r.pr.window_should_close():
            r.game_cycle()
    finally:
        r.game_exit()

