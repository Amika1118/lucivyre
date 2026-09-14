import os

import store_songs.store_music as sm
import file_handeling.handle_csv as hc

def main():
    print("Welcome to Lucivyre")

    # initialization is done only once as it is responsible to make
    # credits 10 for each song, and they will be changed according to user preferences.
    hc.initialize()



main()

