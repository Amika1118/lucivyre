import os
import sys
import time
import sqlite3

from youtubesearchpython.core import playlist

import shared

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from file_handeling import handle_data as hd
from file_handeling import db

# ---- point at your mpv.exe ----
MPV_EXE = r"C:\Users\USER\Downloads\Compressed\mpv-x86_64-20260923-git-f9850ee727\mpv.exe"

import yt_dlp

def search_youtube(query, max_results=5):
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,   # don't resolve each video fully — fast
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)

    results = []
    for entry in info["entries"]:
        results.append({
            "title":    entry.get("title"),
            "url":      f"https://youtube.com/watch?v={entry['id']}",
            "duration": entry.get("duration"),
            "uploader": entry.get("uploader"),
        })
    return results

from python_mpv_jsonipc import MPV
player = MPV(mpv_location=MPV_EXE, start_mpv=True)
player.vo = "null"

DB_PATH        = hd.full_db_path
DEFAULT_VOLUME = 0.5
TICK_MS        = 50

songs = {}

# ----------------------------------------------------------------------
#  STATE — much smaller now, mpv owns the playback info
# ----------------------------------------------------------------------
state = {
    "playlist":             [],
    "index":                0,
    "current_song_id":      None,
    "running":              True,
    "queued_next":          [],
    "volume":               DEFAULT_VOLUME,
    "muted":                False,
    "saved_volume":         DEFAULT_VOLUME,
    "session_started_at":   0.0,
    "session_paused_total": 0.0,
    "session_paused_at":    0.0,
    "paused":               False,
}

# ----------------------------------------------------------------------
#  DATABASE
# ----------------------------------------------------------------------
def get_credits(sid):
    with sqlite3.connect(DB_PATH) as conn:
        r = conn.execute("SELECT song_credits FROM songs WHERE id = ?", (sid,)).fetchone()
    return float(r[0]) if r else None


def set_credits(sid, v):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE songs SET song_credits = ? WHERE id = ?",
            (round(float(v), 3), sid)
        )


# ----------------------------------------------------------------------
#  STATUS PUBLISH — read mpv's own properties
# ----------------------------------------------------------------------
def publish_status():
    now = time.time()

    # mpv tells us everything about the current song
    song_elapsed  = player.time_pos or 0.0
    song_duration = player.duration or 0.0

    # session timer is ours — mpv doesn't know about "sessions"
    if state["paused"]:
        session_elapsed = state["session_paused_at"] - state["session_started_at"] - state["session_paused_total"]
    else:
        session_elapsed = now - state["session_started_at"] - state["session_paused_total"]

    shared.write_status({
        "title":           player.metadata.get("title", "") if player.metadata else "",
        "artist":          player.metadata.get("artist", "") if player.metadata else "",
        "index":           state["index"] + 1,
        "total":           len(state["playlist"]),
        "song_elapsed":    song_elapsed,
        "song_duration":   song_duration,
        "session_elapsed": session_elapsed,
        "paused":          bool(player.pause),
        "volume":          (player.volume or 0) / 100.0,
        "muted":           state["muted"],
    })


# ----------------------------------------------------------------------
#  PLAYBACK
# ----------------------------------------------------------------------
def play_song(index):
    if index < 0 or index >= len(state["playlist"]):
        return False

    db.read_data_from_db(songs)
    song_id = state["playlist"][index]
    data = songs.get(song_id)
    if not data:
        print(f"missing {song_id}")
        return False

    state["index"] = index
    state["current_song_id"] = song_id
    state["paused"] = False

    try:
        player.play(data[5])          # data[5] = file path
        player.pause = False
        player.volume = state["volume"] * 100
    except Exception as e:
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
        pos = player.time_pos or 0.0
        if pos > 3.0:
            return state["index"]
        return max(0, state["index"] - 1)

    return state["index"]


def deduct(sid, played):
    dur = player.duration or 0.0
    if dur <= 0 or played >= dur:
        return
    frac = max(0.0, min(1.0, played / dur))
    c = get_credits(sid)
    if c is not None:
        set_credits(sid, c * frac)


# ----------------------------------------------------------------------
#  VOLUME
# ----------------------------------------------------------------------
def vol_up():
    state["volume"] = min(1.0, round(state["volume"] + 0.05, 2))
    if not state["muted"]:
        player.volume = state["volume"] * 100


def vol_down():
    state["volume"] = max(0.0, round(state["volume"] - 0.05, 2))
    if not state["muted"]:
        player.volume = state["volume"] * 100


def mute_toggle():
    if state["muted"]:
        state["volume"] = state["saved_volume"]
        state["muted"] = False
    else:
        state["saved_volume"] = state["volume"]
        state["volume"] = 0.0
        state["muted"] = True
    player.volume = state["volume"] * 100


def pause_toggle():
    if player.pause:
        player.pause = False
        delta = time.time() - state["session_paused_at"]
        state["session_paused_total"] += delta
        state["session_paused_at"] = 0.0
        state["paused"] = False
    else:
        player.pause = True
        state["session_paused_at"] = time.time()
        state["paused"] = True


# ----------------------------------------------------------------------
#  COMMAND HANDLER
# ----------------------------------------------------------------------
def handle_command(cmd):
    if cmd in ("p", "r"):
        pause_toggle()

    elif cmd == "n":
        played = player.time_pos or 0.0
        deduct(state["current_song_id"], played)
        play_song(choose_next("next"))

    elif cmd == "b":
        played = player.time_pos or 0.0
        deduct(state["current_song_id"], played)
        play_song(choose_next("back"))

    elif cmd == "+":  vol_up()
    elif cmd == "-":  vol_down()
    elif cmd == "m":  mute_toggle()
    elif cmd == "q":  state["running"] = False


# ----------------------------------------------------------------------
#  MAIN
# ----------------------------------------------------------------------
def run(what_for, playlist):
    shared.ensure_runtime()

    state["playlist"] = list(playlist)
    state["session_started_at"] = time.time()
    state["session_paused_total"] = 0.0
    state["session_paused_at"] = 0.0

    player.volume = state["volume"] * 100

    print("Player running. Keep this window open.")
    print("Open a second terminal and run: python controller.py")
    print()

    if not play_song(0):
        print("Can't start playlist.")
        return

    while state["running"]:
        cmd = shared.take_command()
        if cmd:
            handle_command(cmd)

        # natural end — mpv sets idle_active True when nothing's playing
        if (not state["paused"]
                and state["current_song_id"]
                and player.idle_active):
            play_song(choose_next("next"))

        publish_status()
        time.sleep(TICK_MS / 1000)

    player.stop()
    try:
        os.remove(shared.STATUS_FILE)
    except FileNotFoundError:
        pass
    print("Player stopped.")


dict = {}
listing = []
db.read_data_from_db(dict)
for i,j in dict.items():
    listing.append(i)

run("bye", listing)