#---------------------------------> imports
import pyray as pr
import time

#---------------------------------> game class
class InGameMenus:
    def __init__(self, tab_data):
        self.Wx = pr.get_screen_width()
        self.Wy = pr.get_screen_height()

        # lanes
        self.lanes = [
            {"x": self.Wx // 2 + 100, "color": pr.RED},
            {"x": self.Wx // 2 + 150, "color": pr.GREEN},
            {"x": self.Wx // 2 + 200, "color": pr.BLUE},
            {"x": self.Wx // 2 + 250, "color": pr.YELLOW}
        ]

        # notes and timing
        self.notes = []
        self.tab_data = tab_data["tabs"]
        self.bpm = tab_data["bpm"]
        self.start_time = None
        self.next_note_index = 0

        # game state
        self.hit_line_y = self.Wy - 100
        self.hit_tolerance = 30
        self.score = 0
        self.combo = 0


    #---------------------------------> start the song
    def start_song(self):
        self.start_time = time.time()


    #---------------------------------> spawn note
    def spawn_note(self, lane_index):
        lane = self.lanes[lane_index]
        note = {
            "x": lane["x"],
            "y": -20,
            "color": lane["color"],
            "active": True
        }
        self.notes.append(note)


    #---------------------------------> auto spawn from tab_data
    def update_auto_spawn(self):
        if self.start_time is None:
            return

        current_time = time.time() - self.start_time

        while self.next_note_index < len(self.tab_data):
            note_time = self.tab_data[self.next_note_index]["time"]


            if current_time >= note_time - 1.5:
                for lane in self.tab_data[self.next_note_index]["lanes"]:
                    self.spawn_note(lane)
                self.next_note_index += 1
            else:
                break


    #---------------------------------> update notes
    def update_notes(self):
        for note in self.notes:
            if note["active"]:
                note["y"] += self.bpm / 12
                if note["y"] > pr.get_screen_height() + 100:
                    note["active"] = False
                    self.combo = 0

        self.notes = [n for n in self.notes if n["active"]]


    #---------------------------------> draw everything
    def draw_notes(self):
        for lane in self.lanes:
            pr.draw_rectangle(int(lane["x"] - 25), 0, 50, pr.get_screen_height(), pr.fade(lane["color"], 0.2))
            pr.draw_circle(int(lane["x"]), self.hit_line_y, 25, pr.WHITE)

        for note in self.notes:
            pr.draw_circle(int(note["x"]), int(note["y"]), 20, note["color"])

        pr.draw_text(f"Score: {self.score}", 50, 50, 30, pr.WHITE)
        pr.draw_text(f"Combo: {self.combo}", 50, 90, 30, pr.WHITE)


    #---------------------------------> handle key input
    def handle_input(self):
        keys = [pr.KeyboardKey.KEY_A, pr.KeyboardKey.KEY_S, pr.KeyboardKey.KEY_D, pr.KeyboardKey.KEY_F]
        for i, key in enumerate(keys):
            if pr.is_key_pressed(key):
                self.check_hit(i)


    #---------------------------------> check hit
    def check_hit(self, lane_index):
        for note in self.notes:
            if note["active"]:
                if abs(note["y"] - self.hit_line_y) <= self.hit_tolerance:
                    if abs(note["x"] - self.lanes[lane_index]["x"]) <= 25:
                        note["active"] = False
                        self.score += 100
                        self.combo += 1
                        print(f" HIT lane {lane_index}")
                        return
        print(f" MISS lane {lane_index}")
        self.combo = 0

#---------------------------------> song select menu
import os
import json

class SongSelectMenu:
    def __init__(self, music_folder="src/tmp"):
        self.folder = music_folder
        self.songs = self.load_songs()
        self.selected = 0
        self.state = "menu"  # "menu" or "game"
        self.game = None
        self.title = "Select a Song"

    def refresh(self):
        global menu
        if menu.state == "menu":
            menu.songs = menu.load_songs()

    # Load all JSON songs
    def load_songs(self):
        songs = []
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            print("Folder not found, created:", self.folder)
            return songs
        for file in os.listdir(self.folder):
            if file.endswith(".json"):
                path = os.path.join(self.folder, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        songs.append(data)
                except Exception as e:
                    print(f"Failed to load {file}: {e}")
        return songs

    # Handle input (menu & game)
    def handle_input(self):
        if self.state == "menu":
            if pr.is_key_pressed(pr.KeyboardKey.KEY_DOWN):
                self.selected = (self.selected + 1) % len(self.songs)
            if pr.is_key_pressed(pr.KeyboardKey.KEY_UP):
                self.selected = (self.selected - 1) % len(self.songs)
            if pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
                if self.songs:
                    self.start_game(self.songs[self.selected])
            if pr.is_key_pressed(pr.KeyboardKey.KEY_R):
                self.refresh()
        elif self.state == "game":
            self.game.handle_input()
            if pr.is_key_pressed(pr.KeyboardKey.KEY_ESCAPE):
                self.state = "menu"
                self.game = None

    # Start the selected song
    def start_game(self, song_data):
        self.state = "game"
        self.game = InGameMenus(song_data)
        self.game.start_song()

    # Update (menu or game)
    def update(self):
        if self.state == "game" and self.game:
            self.game.update_auto_spawn()
            self.game.update_notes()

    # Draw everything
    def draw(self):
        pr.clear_background(pr.BLACK)
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "game":
            self.game.draw_notes()

    # Draw song selection list
    def draw_menu(self):
        pr.draw_text(self.title, 80, 60, 40, pr.WHITE)

        if not self.songs:
            pr.draw_text("No generated songs found!", 120, 200, 25, pr.RED)
            return

        y = 180
        for i, song in enumerate(self.songs):
            color = pr.YELLOW if i == self.selected else pr.WHITE
            text = f"{song['song_name']} — {int(song['bpm'])} BPM"
            pr.draw_text(text, 120, y, 28, color)
            y += 40

        pr.draw_text("up / down Navigate  |  ENTER Play  |  ESC exit", 80, pr.get_screen_height() - 60, 20, pr.LIGHTGRAY)
        pr.draw_text("R refresh page", 5,20, 20,
                     pr.LIGHTGRAY)



#---------------------------------> globals
menu = SongSelectMenu()

#---------------------------------> draw event
def draw_ev():
    global menu
    if menu:
        menu.draw()

#---------------------------------> update event
def update_ev():
    global menu
    if menu:
        menu.handle_input()
        menu.update()




