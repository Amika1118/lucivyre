import file_handeling.read_n_write as rw
import store_songs.store_music as sm
from pathlib import Path

import json
from datetime import datetime

songs = {}

# getting the file path without issues.
BASE_DIR = Path(__file__).resolve().parent.parent
credit_csv_path = BASE_DIR / "data" / "credits" / "credits.csv"
full_data_path = BASE_DIR / "data" / "song_data" / "full_data.csv"
MARKER = BASE_DIR / "data" / ".initialized.json"

music = {}
music_new = {}

def initialize():
    if MARKER.exists():
        info = json.loads(MARKER.read_text(encoding="utf-8"))
        print(f"Already initialized at {info['when']}")
        return

    sm.check_songs(music)
    for songs, data in music.items():
        song = songs
        length = data[0]
        artist = data[1]
        credits = 10
        music_new[song] = [artist] + [length] + [credits]

    header = ["song", "artist", "length", "credits"]
    rw.write_songs(header,credit_csv_path,music_new)

    MARKER.parent.mkdir(parents=True, exist_ok=True)
    MARKER.write_text(
        json.dumps({"when": datetime.now().isoformat()}),
        encoding="utf-8"
    )
