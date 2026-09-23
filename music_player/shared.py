import os
import json
import time
import shutil

RUNTIME     = "runtime"
CMD_FILE    = os.path.join(RUNTIME, "cmd.txt")
STATUS_FILE = os.path.join(RUNTIME, "status.json")


def ensure_runtime():
    os.makedirs(RUNTIME, exist_ok=True)


# ----------------------------------------------------------------------
#  STATUS (music_player writes, controller reads)
# ----------------------------------------------------------------------
def write_status(data):
    tmp = STATUS_FILE + ".tmp"
    try:
        with open(tmp, "w") as f:
            json.dump(data, f)
    except OSError:
        return

    for _ in range(5):
        try:
            os.replace(tmp, STATUS_FILE)
            return
        except PermissionError:
            time.sleep(0.01)

    # still locked — clean up and skip this round
    try:
        os.remove(tmp)
    except OSError:
        pass


def read_status():
    for _ in range(3):
        try:
            with open(STATUS_FILE) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, PermissionError):
            time.sleep(0.005)
    return None


# ----------------------------------------------------------------------
#  COMMANDS (controller writes, music_player reads)
# ----------------------------------------------------------------------
def write_command(cmd):
    tmp = CMD_FILE + ".tmp"
    try:
        with open(tmp, "w") as f:
            f.write(cmd)
    except OSError:
        return

    for _ in range(5):
        try:
            os.replace(tmp, CMD_FILE)
            return
        except PermissionError:
            time.sleep(0.01)

    try:
        os.remove(tmp)
    except OSError:
        pass


def take_command():
    """Read and delete the command file. Returns the string or None."""
    for _ in range(3):
        try:
            with open(CMD_FILE) as f:
                cmd = f.read().strip()
            try:
                os.remove(CMD_FILE)
            except PermissionError:
                pass
            return cmd or None
        except (FileNotFoundError, PermissionError):
            time.sleep(0.005)
        except OSError:
            break
    return None


# ----------------------------------------------------------------------
#  FORMATTING
# ----------------------------------------------------------------------
def fmt(seconds):
    s = int(seconds or 0)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def status_bar(left, right):
    width = shutil.get_terminal_size().columns
    gap = max(1, width - len(left) - len(right))
    return left + " " * gap + right