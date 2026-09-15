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



    sf.search(song_list)

    i = 1
    # 1. Flatten song_list into a single list of song IDs
    song_ids = []
    for group in song_list:
        for key in group:
            if key not in song_ids:  # avoid duplicates
                song_ids.append(key)

    # 2. Print once
    for i, song_id in enumerate(song_ids, start=1):
        data = songs.get(song_id)
        if data is None:
            continue
        print(f"{i:02d}. {data[1]} - {data[0]}")  # artist - title
    print(" 00. Select all")

    # 3. Ask once
    while True:
        choice = input("Enter your choice (0 = all, q = quit): ").strip().lower()

        if choice in ("q", "quit"):
            return

        try:
            choice = int(choice)
        except ValueError:
            print("Please enter a number or q.")
            continue

        if choice == 0:
            selected = song_ids  # all
            break
        elif 1 <= choice <= len(song_ids):
            selected = [song_ids[choice - 1]]
            break
        else:
            print(f"Please enter a number between 0 and {len(song_ids)}")

    # 4. `selected` is a list of song IDs ready for the player
    print(f"Selected: {selected}")
    # player(selected, songs)




main()

