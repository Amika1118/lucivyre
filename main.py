import os

import file_handeling.handle_data
import store_songs.store_music as sm
import file_handeling.handle_data as hd
import functions.use_functions as uf
import file_handeling.read_n_write as rw
import file_handeling.db as db
import player.music_player as mp

full_data_csv = file_handeling.handle_data.full_data_path

song_list = []
songs = {}


def main():
    print("Welcome to Lucivyre")

    # initialization is done only once as it is responsible to make
    # credits 10 for each song, and they will be changed according to user preferences.
    hd.initialize()    # comment this after the first run as it won't run again after the first run.

    # hc.update_csvs()

    # rw.read_songs(full_data_csv,songs)            # This is not needed in here anymore as we call it in music_player.py

    user_in = ""
    while True:
        user_in = input("How would you like to play? \n01. Play songs \n02. Play songs at random \n03. Search for songs \n04. Sort songs \n05. Exit")
        if user_in in ["01","02","03","04","05","1","2","3","4","5"]:
            break
        else:
            print("Please enter a valid input.")

    match user_in:
        case "1"|"01":
            mp.player("play")
        case "2"|"02":
            mp.player("play at random")
        case "3"|"03":
            uf.use("search")
        case "4"|"04":
            uf.use("sort")
        case "5"|"05":
            print("Goodbye !\nThank you for playing.")

    finale()

def finale():
    """We write the csv when the user exits the player to store the data in csv."""
    db.read_data_from_db(songs)
    header = ["Song_id","Song","Artist","Length","song_credits","Audio_type","File_path","Times_played","Date_added"]
    rw.write_songs(header,songs,full_data_csv)


main()

