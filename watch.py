# terminal_clock.py
import time
import os
import sys

def clear():
    # cross-platform clear
    os.system('cls' if os.name == 'nt' else 'clear')

def digital_watch():
    try:
        while True:
            t = time.localtime()
            hh = f"{t.tm_hour:02d}"
            mm = f"{t.tm_min:02d}"
            ss = f"{t.tm_sec:02d}"
            ampm = "AM" if t.tm_hour < 12 else "PM"
            # 12-hour display (uncomment if you prefer):
            # hour12 = t.tm_hour % 12
            # hh = f"{12 if hour12 == 0 else hour12:02d}"

            clear()
            print("╔════════════════════╗")
            print("║      PY WATCH      ║")
            print("╠════════════════════╣")
            print(f"║   {hh}:{mm}:{ss} {ampm}    ║")
            print("╚════════════════════╝")
            # sleep until the next second (better sync)
            time.sleep(1 - (time.time() % 1))
    except KeyboardInterrupt:
        print("\nWatch stopped.")
        sys.exit(0)

if __name__ == "__main__":
    digital_watch()
