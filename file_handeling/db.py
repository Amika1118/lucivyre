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

def read_data_from_db(new_dict):
    new_dict.clear()
    with sqlite3.connect(DB_PATH) as conn:
        for row in conn.execute("SELECT * FROM songs"):
            new_dict[row[0]] = row[1:]

def update_db(song_id,new_credit):

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE songs SET song_credits = ? WHERE id = ?",
                     (new_credit,song_id)
                     )


"""Sorting Algorithms"""
def sort_by_song_title(sort_type,sorted_list):
    with sqlite3.connect(DB_PATH) as conn:
        if sort_type.upper() == "ASC":
            for row in conn.execute("SELECT id FROM songs ORDER BY song_name ASC"):
                sorted_list.append(row[0])

        else:
            for row in conn.execute("SELECT id FROM songs ORDER BY song_name DESC"):
                sorted_list.append(row[0])

def sort_by_artist(sorted_dict):
    artists = []
    songs.clear()
    with sqlite3.connect(DB_PATH) as conn:
        for row in conn.execute("SELECT id,artist FROM songs ORDER BY artist ASC"):
            if row not in artists:
                sorted_dict.setdefault(row[1], []).append(row[0])

def sort_by_added_time(sort_type,sorted_list):
    with sqlite3.connect(DB_PATH) as conn:
        if sort_type == "ASC":
            for row in conn.execute("SELECT id FROM songs ORDER BY date_added ASC"):
                sorted_list.append(row[0])

        else:
            for row in conn.execute("SELECT id FROM songs ORDER BY date_added DESC"):
                sorted_list.append(row[0])

def sort_by_times_played(sort_type,sorted_list):
    with sqlite3.connect(DB_PATH) as conn:
        if sort_type.upper() == "LEAST":
            for row in conn.execute("SELECT id,times_played FROM songs ORDER BY times_played ASC"):
                sorted_list.append(row[0])

        else:
            for row in conn.execute("SELECT id FROM songs ORDER BY times_played DESC"):
                sorted_list.append(row[0])