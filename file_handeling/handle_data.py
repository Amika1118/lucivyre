import file_handeling.read_n_write as rw
import store_songs.store_music as sm
from pathlib import Path

import json
from datetime import datetime

# getting the file path without issues.
BASE_DIR = Path(__file__).resolve().parent.parent
credit_csv_path = BASE_DIR / "data" /  "song_credits.csv"
full_data_path = BASE_DIR / "data" / "full_data" / "full_data.csv"
full_db_path = BASE_DIR / "data" / "full_data" / "full_db.db"
songs_csv_path = BASE_DIR / "data"  / "songs.csv"
artists_csv_path = BASE_DIR / "data" / "artists.csv"
MARKER = BASE_DIR / "data" / ".initialized.json"

old_dict = {}
new_dict_credits = {}
new_dict_artists = {}
new_dict_songs = {}
new_dict_full = {}

def initialize():
    # checking the existence of the time stamp before running the programme
    # if it exists this code won't run
    if MARKER.exists():
        info = json.loads(MARKER.read_text(encoding="utf-8"))
        print(f"Already initialized at {info['when']}")
        return

    sm.check_songs(old_dict)
    for i, (songs, data) in enumerate(old_dict.items(), start=1):

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
        artist_credits = 10

        # music_new[song_id] = [length] + [song_credits]
        new_dict_full[song_id] = [song] + [artist] + [length] + [song_credits] + [file_type] + [file_path] + [times_played] + [date_added]
        # music_key_details[song_id] = [song] + [artist] + [length] + [times_played]

        # Artist Credits won't be added as well.
        # if artist in artists.keys():
        #     continue
        # else:
        #     artists[artist] = [artist_credits]

    """ Previously All the csvs even the updated while initializing now """
    # # as an initialization step the 10 credit will be added to each song.
    # header = ["Id", "length", "song_credits"]
    # rw.write_songs(header,credit_csv_path,music_new)
    #
    # header = ["Artist", "artist_credits"]
    # rw.write_songs(header,artists_csv_path,artists)
    #
    # # this is made so to be able to update the csv while running unlike the full one.
    # header = ["Id","Song","Artist","Length","Times_played"]
    # rw.write_songs(header,songs_csv_path,music_key_details)
    
    # this is where we add all the data of each song to a csv.
    # this will only be updated when the system stops running.
    header = ["Id","Song","Artist","Length","song_credits","Audio_type","File_path","Times_played","Date_added"]
    rw.write_songs(header,full_data_path,new_dict_full)

    MARKER.parent.mkdir(parents=True, exist_ok=True)
    MARKER.write_text(
        json.dumps({"when": datetime.now().isoformat()}),
        encoding="utf-8"
    )

def update_csvs():
    rw.read_songs(full_data_path, old_dict)
    for song_id, data in old_dict.items():
        title = data[0]
        artist = data[1]
        length = data[2]
        song_credits = data[3]
        times_played = data[6]

        new_dict_credits[song_id] = [length] + [song_credits]
        new_dict_songs[song_id] =  [times_played]

        # as an initialization step the 10 credit will be added to each song.
        header = ["Id", "length", "song_credits"]
        rw.write_songs(header, credit_csv_path, new_dict_credits)

        # this is made so to be able to update the csv while running unlike the full one.
        header = ["Id","Times_played"]
        rw.write_songs(header, songs_csv_path, new_dict_songs)
