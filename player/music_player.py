import pygame

import file_handeling.read_n_write as rw
import file_handeling.handle_csv as hc

full_csv = hc.full_data_path
music = {}

import pygame

def player(user_in):
    rw.read_songs(full_csv, music)

    # initializing the pygame module.
    pygame.mixer.init()

    for song_id, data in music.items():
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
