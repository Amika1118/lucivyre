import sqlite3
import file_handeling.read_n_write as rw

import file_handeling.handle_data as hd

DB_PATH = hd.full_db_path
full_data = hd.full_data_path
songs = {}
new_list = []
sorted_list = []
reverse_sorted_list = []

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

def read_data_from_db(new_dict):
    with sqlite3.connect(DB_PATH) as conn:
        for row in conn.execute("SELECT * FROM songs"):
            new_dict[row[0]] = row[1:]

def sort_by_song_title(sort_type):
    with sqlite3.connect(DB_PATH) as conn:
        if sort_type.upper() == "ASC":
            for row in conn.execute("SELECT id FROM songs ORDER BY song_name ASC"):
                sorted_list.append(row)
        else:
            for row in conn.execute("SELECT * FROM songs ORDER BY song_credits DESC"):
                reverse_sorted_list.append(row)

    return sorted_list, reverse_sorted_list

def sort_by_artist():
    with sqlite3.connect(DB_PATH) as conn:
        for row in conn.execute("SELECT id,artist FROM songs ORDER BY artist ASC"):
            if row not in sorted_list:
                songs.setdefault(row[1], []).append(row[0])

        # for row in conn.execute("SELECT id,artist FROM songs ORDER BY artist DESC"):
        #     if row not in reverse_sorted_list:
        #         reverse_sorted_list.append(row)

def sort_by_added_time(new_dict):
    with sqlite3.connect(DB_PATH) as conn:
        for row in conn.execute("SELECT * FROM songs ORDER BY date_added ASC"):
            new_dict[row[0]] = row[1:]