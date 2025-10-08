#---------------------------------> importing
import pyray as pr


#---------------------------------> classes
class InGameMenus:
    def __init__(self):
        self.Wx = pr.get_screen_width()
        self.Wy = pr.get_screen_height()

        # Lanes
        self.lanes = [
            {"x": self.Wx // 2 + 100, "color": pr.RED},
            {"x": self.Wx // 2 + 150, "color": pr.GREEN},
            {"x": self.Wx // 2 + 200, "color": pr.BLUE},
            {"x": self.Wx // 2 + 250, "color": pr.YELLOW}
        ]

        self.notes = []

        # Hit line
        self.hit_line_y = self.Wy + 500
        self.hit_tolerance = 30

        # Score
        self.score = 0
        self.combo = 0


    #---------------------------------> spawn notes
    def spawn_note(self, lane_index):
        lane = self.lanes[lane_index]
        note = {
            "x": lane["x"],
            "y": -20,
            "color": lane["color"],
            "active": True
        }
        self.notes.append(note)


    #---------------------------------> update notes
    def update_notes(self , bps):
        for note in self.notes:
            if note["active"]:
                note["y"] += bps // 12
                if note["y"] > pr.get_screen_height() + 100:
                    note["active"] = False
                    self.combo = 0

        self.notes = [n for n in self.notes if n["active"]]

    # ---------------------------------> draw notes and lanes
    def draw_notes(self):
        # lanes
        for lane in self.lanes:
            pr.draw_rectangle(int(lane["x"] - 25), 0, 50, pr.get_screen_height(), pr.fade(lane["color"], 0.2))
            pr.draw_circle(int(lane["x"]), self.hit_line_y, 25, pr.WHITE)

        # notes
        for note in self.notes:
            pr.draw_circle(int(note["x"]), int(note["y"]), 20, note["color"])

        # score
        pr.draw_text(f"Score: {self.score}", 50, 50, 30, pr.WHITE)
        pr.draw_text(f"Combo: {self.combo}", 50, 90, 30, pr.WHITE)

    #---------------------------------> handle key input
    def handle_input(self):
        keys = [pr.KeyboardKey.KEY_A, pr.KeyboardKey.KEY_S, pr.KeyboardKey.KEY_D, pr.KeyboardKey.KEY_F]
        for i, key in enumerate(keys):
            if pr.is_key_pressed(key):
                self.check_hit(i)

    # ---------------------------------> check hit
    def check_hit(self, lane_index):
        for note in self.notes:
            if note["active"]:
                if abs(note["y"] - self.hit_line_y) <= self.hit_tolerance:
                    if abs(note["x"] - self.lanes[lane_index]["x"]) <= 25:
                        note["active"] = False
                        self.score += 100
                        self.combo += 1
                        print(f"✅ HIT lane {lane_index}")
                        return
        print(f"❌ MISS lane {lane_index}")
        self.combo = 0