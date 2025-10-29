# gui_watch.py
import tkinter as tk
import math
import time
from datetime import datetime

WIDTH = 400
HEIGHT = 480
CLOCK_RADIUS = 160
CENTER = (WIDTH // 2, HEIGHT // 2 - 20)

class WatchApp:
    def __init__(self, root):
        self.root = root
        root.title("Python Watch")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        # Digital labels
        self.time_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.lbl_time = tk.Label(root, textvariable=self.time_var, font=("Helvetica", 18))
        self.lbl_time.place(x=WIDTH//2, y=HEIGHT-60, anchor="center")
        self.lbl_date = tk.Label(root, textvariable=self.date_var, font=("Helvetica", 12))
        self.lbl_date.place(x=WIDTH//2, y=HEIGHT-35, anchor="center")

        self.running = True

        # buttons
        self.btn_start = tk.Button(root, text="Start", command=self.start)
        self.btn_stop = tk.Button(root, text="Stop", command=self.stop)
        self.btn_start.place(x=WIDTH//2 - 60, y=HEIGHT-25, anchor="center")
        self.btn_stop.place(x=WIDTH//2 + 60, y=HEIGHT-25, anchor="center")

        # Draw clock face static parts
        self.draw_face()
        # keep ids for hands so we can update (delete/redraw)
        self.hand_ids = {"hour": None, "min": None, "sec": None}
        self.update_clock()

    def start(self):
        if not self.running:
            self.running = True
            self.update_clock()

    def stop(self):
        self.running = False

    def draw_face(self):
        cx, cy = CENTER
        r = CLOCK_RADIUS
        # outer circle
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, width=3)
        # hour marks
        for h in range(12):
            angle = math.radians(h * 30)  # 360/12 = 30
            x1 = cx + (r - 10) * math.sin(angle)
            y1 = cy - (r - 10) * math.cos(angle)
            x2 = cx + (r - 30) * math.sin(angle)
            y2 = cy - (r - 30) * math.cos(angle)
            self.canvas.create_line(x1, y1, x2, y2, width=3)

        # center dot
        self.canvas.create_oval(cx-6, cy-6, cx+6, cy+6, fill="black")

    def draw_hand(self, length, angle_deg, width=2, tag=None, color="black"):
        cx, cy = CENTER
        angle = math.radians(angle_deg)
        x = cx + length * math.sin(angle)
        y = cy - length * math.cos(angle)
        return self.canvas.create_line(cx, cy, x, y, width=width, fill=color, capstyle=tk.ROUND, tags=tag)

    def update_clock(self):
        now = datetime.now()
        hh = now.hour
        mm = now.minute
        ss = now.second
        ms = now.microsecond

        # digital display
        # 12-hour format with AM/PM
        hour12 = hh % 12
        hour12 = 12 if hour12 == 0 else hour12
        ampm = "AM" if hh < 12 else "PM"
        self.time_var.set(f"{hour12:02d}:{mm:02d}:{ss:02d} {ampm}")
        self.date_var.set(now.strftime("%A, %d %B %Y"))

        # compute angles:
        # Seconds: each second = 6 degrees; add fractional from microseconds for smoothness
        sec_angle = (ss + ms/1_000_000) * 6
        min_angle = (mm + ss/60.0) * 6
        hour_angle = (hour12 % 12 + mm/60.0 + ss/3600.0) * 30

        # lengths
        hour_len = CLOCK_RADIUS * 0.5
        min_len = CLOCK_RADIUS * 0.75
        sec_len = CLOCK_RADIUS * 0.9

        # remove old hands
        for k in self.hand_ids:
            if self.hand_ids[k]:
                self.canvas.delete(self.hand_ids[k])
                self.hand_ids[k] = None

        # draw new hands
        self.hand_ids["hour"] = self.draw_hand(hour_len, hour_angle, width=6, color="black")
        self.hand_ids["min"]  = self.draw_hand(min_len, min_angle, width=4, color="black")
        self.hand_ids["sec"]  = self.draw_hand(sec_len, sec_angle, width=2, color="red")

        if self.running:
            # schedule next update — aim for smooth update (~50ms)
            self.root.after(50, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = WatchApp(root)
    root.mainloop()
