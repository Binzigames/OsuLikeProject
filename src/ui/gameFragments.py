#---------------------------------> importing
import pyray as pr

#---------------------------------> classes
class InGameMenus:
    def __init__(self):
        self.Wx = pr.get_screen_width()
        self.Wy = pr.get_screen_height()


        self.lanes = [
            {"x": self.Wx // 2 + 100, "color": pr.RED},
            {"x": self.Wx // 2 + 150,  "color": pr.GREEN},
            {"x": self.Wx // 2 + 200,  "color": pr.BLUE},
            {"x": self.Wx // 2 + 250, "color": pr.YELLOW}
        ]

        self.notes = []

    def spawn_note(self, lane_index):

        lane = self.lanes[lane_index]
        note = {
            "x": lane["x"],
            "y": -20,
            "color": lane["color"],
            "active": True
        }
        self.notes.append(note)

    def update_notes(self):

        for note in self.notes:
            if note["active"]:
                note["y"] += 6
                if note["y"] > pr.get_screen_height() - 20:
                    note["active"] = False
        self.notes = [n for n in self.notes if n["active"]]

    def draw_notes(self):
        for lane in self.lanes:
            pr.draw_rectangle(int(lane["x"] - 25), 0, 50, pr.get_screen_height(), pr.fade(lane["color"], 0.2))

        for note in self.notes:
            pr.draw_circle(int(note["x"]), int(note["y"]), 20, note["color"])