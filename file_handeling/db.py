import sqlite3
import file_handeling.read_n_write as rw

import file_handeling.handle_data as hd

DB_PATH = hd.full_db_path
full_data = hd.full_data_path
songs = {}
new_list = []


def initialize_db():

    # # This ensures the folder exists (good practice even if you know it does)
    # DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute('''CREATE TABLE IF NOT EXISTS songs
                            ( id Text PRIMARY KEY NOT NULL,
                                song_name Text NOT NULL,
                                artist Text NOT NULL,
                                song_length double NOT NULL,
                                song_credits Text NOT NULL,
                                audio_types Text NOT NULL,
                                file_path Text NOT NULL,
                                times_played int NOT NULL,
                                date_added Text NOT NULL )''')

def store_data_in_db():
    rw.read_songs(full_data, songs)
    for song_id,data in songs.items():
        id = song_id
        song_name = data[0]
        artist = data[1]
        song_length = float(data[2])
        song_credits = float(data[3])
        audio_types = data[4]
        file_path = data[5]
        times_played = data[6]
        date_added = data[7]
        new_list.append((id,song_name,artist,song_length,song_credits,audio_types,file_path,times_played,date_added))

    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany("""INSERT OR REPLACE INTO songs 
                        (id, song_name,artist,song_length,song_credits,audio_types,file_path,times_played,date_added)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,new_list
        )
