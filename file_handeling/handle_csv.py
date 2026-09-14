import file_handeling.read_n_write as rw
import store_songs.store_music as sm
from pathlib import Path

import json
from datetime import datetime

# getting the file path without issues.
BASE_DIR = Path(__file__).resolve().parent.parent
credit_csv_path = BASE_DIR / "data" / "song_credits" / "song_credits.csv"
full_data_path = BASE_DIR / "data" / "full_data" / "full_data.csv"
songs_csv_path = BASE_DIR / "data" / "songs" / "songs.csv"
MARKER = BASE_DIR / "data" / ".initialized.json"

music = {}
music_new = {}
music_full = {}
music_key_details = {}

def initialize():
    # checking the existence of the time stamp before running the programme
    # if it exists this code won't run
    if MARKER.exists():
        info = json.loads(MARKER.read_text(encoding="utf-8"))
        print(f"Already initialized at {info['when']}")
        return

    sm.check_songs(music)
    for i, (songs, data) in enumerate(music.items(), start=1):

        if len(str(i)) == 1:
            song_id = f"song_000{i}"
        elif len(str(i)) == 2:
            song_id = f"song_00{i}"
        elif len(str(i)) == 3:
            song_id = f"song_0{i}"
        else:
            song_id = f"song_{i}"

        song = songs
        length = data[0]
        artist = data[1]
        file_type = data[2]
        file_path = data[3]
        times_played = 0
        song_credits = 10
        date_added = data[4]
        music_new[song_id] = [length] + [song_credits]
        music_full[song_id] = [song] + [artist] + [length] + [song_credits] + [file_type] + [file_path] + [times_played] + [date_added]
        music_key_details[song_id] = [song] + [artist] + [length] + [times_played]

    # as an initialization step the 10 credit will be added to each song.
    header = ["Id", "length", "song_credits"]
    rw.write_songs(header,credit_csv_path,music_new)

    # this is made so to be able to update the csv while running unlike the full one.
    header = ["Id","Song","Artist","Length","Times_played"]
    rw.write_songs(header,songs_csv_path,music_key_details)
    
    # this is where we add all the data of each song to a csv.
    # this will only be updated when the system stops running.
    header = ["Id","Song","Artist","Length","song_credits","Audio_type","File_path","Times_played","Date_added"]
    rw.write_songs(header,full_data_path,music_full)

    MARKER.parent.mkdir(parents=True, exist_ok=True)
    MARKER.write_text(
        json.dumps({"when": datetime.now().isoformat()}),
        encoding="utf-8"
    )
