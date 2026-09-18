import file_handeling.handle_data
import sys
import file_handeling.read_n_write as rw
import functions.sort as s
import ui_features.ui as ui
from file_handeling.handle_data import full_data_path

songs = {}
artists = []

full_data_csv = file_handeling.handle_data.full_data_path

def search_by_first_letter(user_input,song_ids):
    """Search for songs by first letter."""
    songs.clear()
    rw.read_songs(full_data_csv, songs)
    for song_id,data in songs.items():
        if user_input.capitalize() == data[0][0].capitalize():
            song_ids.append(song_id)

def search_by_title(user_input,song_ids):
    """Search for songs by title."""
    songs.clear()
    rw.read_songs(full_data_csv, songs)
    for song_id,data in songs.items():
        if user_input.lower() in data[0].lower():
            song_ids.append(song_id)
    # return song_ids

def search_by_artist(user_input,choice,song_ids):
    """Search for songs by artist."""
    songs.clear()
    if choice == 1:
        user_in = search_artist(user_input)
    else:
        user_in = user_input

    song = s.sort_by_artist()
    for artist,song_id in song.items():
        if user_in.lower() in artist.lower():
            for id in song_id:
                song_ids.append(id)

def search_artist(user_input):
    """Search for artists by the first letter of their name."""
    songs.clear()
    rw.read_songs(full_data_csv, songs)
    for song_id,data in songs.items():
        if user_input.capitalize() in data[1][0].capitalize():
            if data[1] not in artists:
                artists.append(data[1])

    while True:
        print("Search Results for your search ")
        ui.lines(34)
        for i, artist in enumerate(artists, start = 1):
            if i < 10:
                print(f"0{i}. {artist}")
            elif i > 10 :
                print(f"{i}. {artist}")

        print()
        while True:
            try :
                user_choice = int(input("Enter your choice: "))
                break
            except ValueError:
                print("Please enter a number.")

        if user_choice < 0 or user_choice > len(artists):
            print("Please enter a valid number.")
        else:
            send_artist = artists[user_choice - 1]
            return send_artist