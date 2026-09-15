import file_handeling.handle_csv
import sys
import file_handeling.read_n_write as rw
import functions.sort as s
import ui_features.ui as ui
from file_handeling.handle_csv import full_data_path

songs = {}
song_ids = []
artists = []

full_data_csv = file_handeling.handle_csv.full_data_path

def search_by_first_letter(user_input):
    """Search for songs by first letter."""
    songs.clear()
    rw.read_songs(full_data_csv, songs)
    for song_id,data in songs.items():
        if user_input.capitalize() == data[0][0].capitalize():
            song_ids.append(song_id)

    return song_ids

def search_by_title(user_input):
    """Search for songs by title."""
    songs.clear()
    rw.read_songs(full_data_csv, songs)
    for song_id,data in songs.items():
        if user_input.lower() in data[0].lower():
            song_ids.append(song_id)

    return song_ids

def search_by_artist(user_input,choice):
    """Search for songs by artist."""
    songs.clear()
    if choice == 1:
        user_in = search_artist(user_input)
    else:
        user_in = user_input

    song = s.sort_by_artist()
    for artist,song_id in song.items():
        if user_in.lower() in artist.lower():
            song_ids.append(song_id)

    return song_ids

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

def search():
    while True:
        print("Search for songs ....")
        ui.lines(34)
        print("01. By Song\n02. By Artist \n03. Exit search")
        ui.lines(34)
        user_choice = input("Enter your choice: ")
        ui.clear_screen()
        if user_choice.lower() in ["1", "01", "song", "by song"]:
            print("Search for songs by Title ....")
            ui.lines(45)
            song_search = input("Enter Title of the song : ")
            ui.clear_screen()
            if len(song_search) == 1:
                if song_search.isalpha():
                    print(f"You only entered one letter.\nWe're gonna search for songs starting with {song_search.capitalize()}\n")
                    ui.lines(45)
                    search_by_first_letter(song_search.capitalize())
                    break
                else:
                    print("Please enter a valid English letter.")
            else :
                print(f"We're gonna search for {song_search.capitalize()}\n")
                ui.lines(45)
                search_by_title(song_search.capitalize())
                break

        elif user_choice.lower() in ["2", "02", "artist", "by artist"]:
            artist_search = input("Enter the name of the artist : ")
            ui.clear_screen()
            if len(artist_search) == 1:
                if artist_search.isalpha():
                    print(f"You only entered one letter.\nSo We're gonna search for artists starting with {artist_search.capitalize()}\n")
                    ui.lines(45)
                    search_by_artist(artist_search.capitalize(),1)
                    break
                else:
                    print("Please enter a valid English letter.")
            else:
                print(f"We're gonna search for {artist_search.capitalize()}\n")
                ui.lines(45)
                search_by_artist(artist_search.capitalize(),0)
                break

        elif user_choice.lower() in ["3", "03", "exit", "exit search"]:
            print("You're now exiting the search.")
            break

        else:
            print("Please enter a valid Input.")
            ui.lines(45)