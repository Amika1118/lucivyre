import os
import shutil
import sys


def lines(count, char="-"):
    """Print a horizontal line of `count` characters."""
    print(char * count)

def clear_screen():
    """Clear the terminal (works on Windows, Linux, Mac)."""
    os.system("cls" if os.name == "nt" else "clear")

def blank(lines=1):
    """Print N blank lines."""
    print("\n" * lines, end="")

def fmt(seconds):
    """Format seconds as m:ss, or h:mm:ss if >= 1 hour."""
    s = int(seconds or 0)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"

def terminal_width():
    """Current terminal width (re-checked every call)."""
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return 80

def status_bar(left, right, width=None):
    """Build a full-width line: left text on the left, right text on the right."""
    width = width or terminal_width()
    gap = width - len(left) - len(right)
    if gap < 1:
        gap = 1
    return left + " " * gap + right

def draw_status(session_seconds, song_seconds, duration_seconds,paused=False, mode="playing"):
    """
    Overwrite the current line with the two-timer status bar.
    Uses \\r so it redraws in place — call it from a loop every 250ms.
    """
    if mode != "playing":
        return

    left  = f"Session: {fmt(session_seconds)}"
    right = f'[>] {fmt(song_seconds)} / {fmt(duration_seconds)}'
    if paused:
        right += "  (paused)"

    line = status_bar(left, right)
    sys.stdout.write("\r" + line)
    sys.stdout.flush()

def end_status():
    """Finish the status line so the next print starts on a new line."""
    sys.stdout.write("\n")
    sys.stdout.flush()