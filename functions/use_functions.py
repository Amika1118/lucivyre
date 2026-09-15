import file_handeling.handle_csv
import functions.search as sh
import ui_features.ui as ui
import file_handeling.read_n_write as rw
import functions.shuffle as sf

full_data_csv = file_handeling.handle_csv.full_data_path

song_list = []
songs = {}
song_credits = {}

def search(song_ids):
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
                    sh.search_by_first_letter(song_search.capitalize(),song_ids)
                    break
                else:
                    print("Please enter a valid English letter.")
            else :
                print(f"We're gonna search for {song_search.capitalize()}\n")
                ui.lines(45)
                sh.search_by_title(song_search.capitalize(),song_ids)
                break

        elif user_choice.lower() in ["2", "02", "artist", "by artist"]:
            artist_search = input("Enter the name of the artist : ")
            ui.clear_screen()
            if len(artist_search) == 1:
                if artist_search.isalpha():
                    print(f"You only entered one letter.\nSo We're gonna search for artists starting with {artist_search.capitalize()}\n")
                    ui.lines(45)
                    sh.search_by_artist(artist_search.capitalize(),1,song_ids)
                    break
                else:
                    print("Please enter a valid English letter.")
            else:
                print(f"We're gonna search for {artist_search.capitalize()}\n")
                ui.lines(45)
                sh.search_by_artist(artist_search.capitalize(),0,song_ids)
                break

        elif user_choice.lower() in ["3", "03", "exit", "exit search"]:
            print("You're now exiting the search.")
            break

        else:
            print("Please enter a valid Input.")
            ui.lines(45)

def use_search(search_for, selected_songs):
        rw.read_songs(full_data_csv,songs)
        search(song_list)

        # Flatten song_list into a single list of song IDs
        # if the song_list is filled with id lists
        song_ids = []
        if search_for == "artist":
            for group in song_list:
                for key in group:
                    if key not in song_ids:  # avoid duplicates
                        song_ids.append(key)

        # if not we can just use the list that is already been made.
        else:
            song_ids = song_list

        # Print all the search results.
        for i, song_id in enumerate(song_ids, start=1):
            data = songs.get(song_id)
            if data is None:
                continue
            print(f"{i:02d}. {data[1]} - {data[0]}")  # artist - title
        print(" 00. Select all")

        # Ask whether to play all or play one.
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
                selected_songs = song_ids  # all
                break
            elif 1 <= choice <= len(song_ids):
                selected_songs = [song_ids[choice - 1]]
                break
            else:
                print(f"Please enter a number between 0 and {len(song_ids)}")
