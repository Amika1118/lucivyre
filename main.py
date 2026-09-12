import os
import pygame

import store_songs.store_music as sm
import file_handeling.file_handeling as fh

song_list = []

def main():
    print("Welcome to Lucivyre")
    sm.check_songs(song_list)
    # for songs,details in song_list:
    #     print(songs,details)



main()

