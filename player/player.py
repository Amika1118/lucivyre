import os
import sys
import time
import sqlite3
import pygame
import shared

import sys
import os

# add project root (one level up from this file) to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from file_handeling import handle_data as hd

DB_PATH        = hd.full_db_path
DEFAULT_VOLUME = 0.7
TICK_MS        = 50

# ----------------------------------------------------------------------
#  STATE
# ----------------------------------------------------------------------
state = {
    "playlist":            [],
    "index":               0,
    "current_song_id":     None,
    "paused":              False,
    "volume":              DEFAULT_VOLUME,
    "muted":               False,
    "saved_volume":        DEFAULT_VOLUME,
    "song_started_at":     0.0,
    "song_paused_at":      0.0,
    "song_paused_total":   0.0,
    "song_duration":       0.0,
    "session_started_at":  0.0,
    "session_paused_total":0.0,
    "queued_next":         [],
    "running":             True,
    "title":               "",
    "artist":              "",
}


# ----------------------------------------------------------------------
#  DATABASE
# ----------------------------------------------------------------------
def load_songs():
    songs = {}
    with sqlite3.connect(DB_PATH) as conn:
        for row in conn.execute(
            "SELECT id, song_name, artist, song_length, song_credits, "
            "audio_types, file_path, times_played, date_added FROM songs"
        ):
            songs[row[0]] = list(row[1:])
    return songs


def get_credits(sid):
    with sqlite3.connect(DB_PATH) as conn:
        r = conn.execute(
            "SELECT song_credits FROM songs WHERE id = ?", (sid,)
        ).fetchone()
    return float(r[0]) if r else None


def set_credits(sid, v):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE songs SET song_credits = ? WHERE id = ?",
            (round(float(v), 3), sid)
        )


# ----------------------------------------------------------------------
#  STATUS PUBLISH
# ----------------------------------------------------------------------
def publish_status():
    now = time.time()

    if state["paused"]:
        song_elapsed = (state["song_paused_at"]
                        - state["song_started_at"]
                        - state["song_paused_total"])
    else:
        song_elapsed = (now
                        - state["song_started_at"]
                        - state["song_paused_total"])

    session_elapsed = (now
                       - state["session_started_at"]
                       - state["session_paused_total"])

    shared.write_status({
        "title":           state["title"],
        "artist":          state["artist"],
        "index":           state["index"] + 1,
        "total":           len(state["playlist"]),
        "song_elapsed":    song_elapsed,
        "song_duration":   state["song_duration"],
        "session_elapsed": session_elapsed,
        "paused":          state["paused"],
        "volume":          state["volume"],
        "muted":           state["muted"],
    })


# ----------------------------------------------------------------------
#  PLAYBACK
# ----------------------------------------------------------------------
def play_song(index):
    if index < 0 or index >= len(state["playlist"]):
        return False

    songs = load_songs()
    song_id = state["playlist"][index]
    data = songs.get(song_id)
    if not data:
        print(f"missing {song_id}")
        return False

    state["index"] = index
    state["current_song_id"] = song_id
    state["title"] = data[0]
    state["artist"] = data[1]
    state["song_started_at"] = time.time()
    state["song_paused_at"] = 0.0
    state["song_paused_total"] = 0.0
    state["song_duration"] = float(data[2])
    state["paused"] = False

    try:
        pygame.mixer.music.load(data[5])
        pygame.mixer.music.set_volume(state["volume"])
        pygame.mixer.music.play()
    except pygame.error as e:
        print(f"can't play {data[0]}: {e}")
        return False

    print(f"[{index+1}/{len(state['playlist'])}] {data[1]} - {data[0]}")
    return True


def choose_next(action):
    if state["queued_next"]:
        nxt = state["queued_next"].pop(0)
        if nxt in state["playlist"]:
            return state["playlist"].index(nxt)
        state["playlist"].insert(state["index"] + 1, nxt)
        return state["index"] + 1

    if action == "next":
        nxt = state["index"] + 1
        return 0 if nxt >= len(state["playlist"]) else nxt

    if action == "back":
        elapsed = time.time() - state["song_started_at"] - state["song_paused_total"]
        if elapsed > 3.0:
            return state["index"]
        return max(0, state["index"] - 1)

    return state["index"]


def deduct(sid, played):
    if state["song_duration"] <= 0 or played >= state["song_duration"]:
        return
    frac = max(0.0, min(1.0, played / state["song_duration"]))
    c = get_credits(sid)
    if c is not None:
        set_credits(sid, c * frac)


# ----------------------------------------------------------------------
#  VOLUME
# ----------------------------------------------------------------------
def vol_up():
    state["volume"] = min(1.0, round(state["volume"] + 0.1, 2))
    if not state["muted"]:
        pygame.mixer.music.set_volume(state["volume"])


def vol_down():
    state["volume"] = max(0.0, round(state["volume"] - 0.1, 2))
    if not state["muted"]:
        pygame.mixer.music.set_volume(state["volume"])


def mute_toggle():
    if state["muted"]:
        state["volume"] = state["saved_volume"]
        state["muted"] = False
    else:
        state["saved_volume"] = state["volume"]
        state["volume"] = 0.0
        state["muted"] = True
    pygame.mixer.music.set_volume(state["volume"])


def pause_toggle():
    if state["paused"]:
        pygame.mixer.music.unpause()
        delta = time.time() - state["song_paused_at"]
        state["song_paused_total"]    += delta
        state["session_paused_total"] += delta
        state["song_paused_at"] = 0.0
        state["paused"] = False
    else:
        pygame.mixer.music.pause()
        state["song_paused_at"] = time.time()
        state["paused"] = True


# ----------------------------------------------------------------------
#  COMMAND HANDLER
# ----------------------------------------------------------------------
def handle_command(cmd):
    if cmd in ("p", "r"):
        pause_toggle()

    elif cmd == "n":
        played = time.time() - state["song_started_at"] - state["song_paused_total"]
        deduct(state["current_song_id"], played)
        pygame.mixer.music.stop()
        play_song(choose_next("next"))

    elif cmd == "b":
        played = time.time() - state["song_started_at"] - state["song_paused_total"]
        deduct(state["current_song_id"], played)
        pygame.mixer.music.stop()
        play_song(choose_next("back"))

    elif cmd == "+":
        vol_up()

    elif cmd == "-":
        vol_down()

    elif cmd == "m":
        mute_toggle()

    elif cmd == "q":
        state["running"] = False


# ----------------------------------------------------------------------
#  MAIN
# ----------------------------------------------------------------------
def run(playlist):
    shared.ensure_runtime()

    state["playlist"] = list(playlist)
    state["session_started_at"] = time.time()

    pygame.mixer.init()
    pygame.mixer.music.set_volume(state["volume"])

    print("Player running. Keep this window open.")
    print("Open a second terminal and run: python controller.py")
    print()

    if not play_song(0):
        print("Can't start playlist.")
        return

    clock = pygame.time.Clock()

    while state["running"]:
        cmd = shared.take_command()
        if cmd:
            handle_command(cmd)

        # natural end
        if (not state["paused"]
                and state["current_song_id"]
                and not pygame.mixer.music.get_busy()):
            pygame.mixer.music.stop()
            play_song(choose_next("next"))

        publish_status()
        clock.tick(TICK_MS)

    pygame.mixer.music.stop()
    try:
        os.remove(shared.STATUS_FILE)
    except FileNotFoundError:
        pass
    print("Player stopped.")


from file_handeling import db as db
dict= {}
new_list = []
db.read_data_from_db(dict)
for key, value in dict.items():
    new_list.append(key)

run(new_list)