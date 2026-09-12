import os
import pygame

import store_songs.store_music as sm
import file_handeling.file_handeling as fh

song_list = {}

def main():
    print("Welcome to Lucivyre")
    sm.check_songs(song_list)
    for songs,details in song_list.items():
        print(f"{float(details[0][0]/60):.2f}")
        print(details[2][0])
        print(songs)




main()

