import pygame

import file_handeling.read_n_write as rw
import file_handeling.handle_data as hd
import file_handeling.db as db

full_csv = hd.full_data_path
songs = {}

def player(user_in):

    # rw.read_songs(full_data_csv, songs)           # this was the previous way which read a csv and then populated a dictionary
    db.read_data_from_db(songs)                     # now we directly read form sqlite database and populate the same dictionary

    # initializing the pygame module.
    pygame.mixer.init()

    for song_id, data in songs.items():
        title = data[0]
        path  = data[5]

        print(f"Playing: {title}")

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()

            # wait here until this song ends
            # this is where we play the song.
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        except pygame.error as e:
            print(f"  Skipped: {e}")

    print("All songs finished.")
