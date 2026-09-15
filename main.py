import os

import file_handeling.handle_csv
import store_songs.store_music as sm
import file_handeling.handle_csv as hc
import functions.search as sf
import file_handeling.read_n_write as rw

full_data_csv = file_handeling.handle_csv.full_data_path

song_list = []
songs = {}


def main():
    print("Welcome to Lucivyre")

    # initialization is done only once as it is responsible to make
    # credits 10 for each song, and they will be changed according to user preferences.
    hc.initialize()    # comment this after the first run as it won't run again after the first run.

    # hc.update_csvs()

    rw.read_songs(full_data_csv,songs)








main()

