import sys
import os
import time
import threading
import msvcrt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from music_player import shared as shared


# ----------------------------------------------------------------------
#  DISPLAY
# ----------------------------------------------------------------------
def draw(status):
    if not status:
        line = "Waiting for music_player..."
        sys.stdout.write("\r" + line.ljust(80))
        sys.stdout.flush()
        return

    left = f"Session: {shared.fmt(status['session_elapsed'])}"
    mid  = f"Vol: {int(status['volume']*100)}%"
    if status["muted"]:
        mid += " (MUTED)"

    right = (f"[>] {shared.fmt(status['song_elapsed'])} "
             f"/ {shared.fmt(status['song_duration'])}")
    if status["paused"]:
        right += "  (paused)"

    line = shared.status_bar(f"{left}   {mid}", right)
    sys.stdout.write("\r" + line)
    sys.stdout.flush()


def display_loop():
    while True:
        draw(shared.read_status())
        time.sleep(0.25)


# ----------------------------------------------------------------------
#  KEYBOARD
# ----------------------------------------------------------------------
def get_key():
    if msvcrt.kbhit():
        try:
            return msvcrt.getwch().lower()
        except Exception:
            return None
    return None


# ----------------------------------------------------------------------
#  MAIN
# ----------------------------------------------------------------------
def main():
    shared.ensure_runtime()

    print("Controller ready.")
    print("Controls: [p]ause [n]ext [b]ack [+/-]vol [m]ute [q]uit music_player")
    print()

    threading.Thread(target=display_loop, daemon=True).start()

    try:
        while True:
            k = get_key()
            if k:
                shared.write_command(k)
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

    print("\nController closed.")


if __name__ == "__main__":
    main()