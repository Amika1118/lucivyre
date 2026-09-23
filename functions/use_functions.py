import file_handeling.handle_data as hd
import functions.search as sh
import functions.shuffle as sf
import ui_features.ui as ui
import file_handeling.read_n_write as rw
import file_handeling.db as db

full_data_csv = hd.full_data_path

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

def use(what_for):
        # rw.read_songs(full_data_csv,songs)            # this was the previous way which read a csv and then populated a dictionary
        db.read_data_from_db(songs)                     # now we directly read form sqlite database and populate the same dictionary

        # from here we change what we use we can call this from main.py
        if what_for.lower() in ["search"]:
            search(song_list)
        elif what_for.lower() in ["sort"]:
            sort(song_list)

        """"As this function is now done from search.py now we don't need this."""
        # Flatten song_list into a single list of song IDs
        # if the song_list is filled with id lists
        # song_ids = []
        # if search_for == "artist":
        #     for group in song_list:
        #         for key in group:
        #             if key not in song_ids:  # avoid duplicates
        #                 song_ids.append(key)
        #
        # # if not we can just use the list that is already been made.
        # else:
        song_ids = song_list
        if len(song_ids) != 0:
            # Print all the search results.
            if what_for.lower() in ["search"]:
                for i, song_id in enumerate(song_ids, start=1):
                    data = songs.get(song_id)
                    if data is None:
                        continue
                    print(f"{i:02d}. {data[1]} - {data[0]}")  # artist - title
            else:
                page_size = 20
                current_page = 1
                total_songs = len(song_ids)

                # Calculate total pages (using ceiling division)
                # max(1, ...) prevents a "Page 1 of 0" error if there are no songs
                total_pages = max(1, (total_songs + page_size - 1) // page_size)

                while True:
                    # 1. Calculate the slice indices for the current page
                    start_index = (current_page - 1) * page_size
                    end_index = start_index + page_size

                    # 2. Slice the song_ids list to get only the 20 songs for this page
                    page_song_ids = song_ids[start_index:end_index]

                    print(f"\n--- Page {current_page} of {total_pages} ---")

                    # 3. Print the songs. Notice 'start=start_index + 1' so numbering stays continuous
                    for i, song_id in enumerate(page_song_ids, start=start_index + 1):
                        data = songs.get(song_id)
                        if data is None:
                            continue
                        print(f"{i:02d}. {data[1]} - {data[0]}")

                    print(" 00. Select all")

                    # 4. Navigation Menu
                    print("\n[N] Next 20 | [P] Previous 20 | [Q] Quit / Type a number to select")
                    choice = input("Choose an option: ").strip().lower()

                    if choice == 'n':
                        if current_page < total_pages:
                            current_page += 1
                        else:
                            print(">> You are on the last page.")
                    elif choice == 'p':
                        if current_page > 1:
                            current_page -= 1
                        else:
                            print(">> You are on the first page.")
                    elif choice == 'q':
                        break  # Exit pagination loop and go to the final selection loop
                    elif choice == '0' or choice == '00':
                        # Select all immediately
                        selected = song_ids
                        sf.add_credits(selected)
                        break
                    elif choice.isdigit():
                        # User typed a specific number while browsing
                        num = int(choice)
                        if 1 <= num <= total_songs:
                            selected = [song_ids[num - 1]]
                            sf.add_credits(selected)
                            break
                        else:
                            print(f"Invalid number. Please choose between 1 and {total_songs}.")
                    else:
                        print("Invalid input. Please try again.")

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

                if choice in [0, 00]:
                    selected = song_ids              # all
                    sf.add_credits(selected)
                    break
                elif 1 <= choice <= len(song_ids):
                    selected = [song_ids[choice - 1]]
                    sf.add_credits(selected)
                    break
                else:
                    print(f"Please enter a number between 0 and {len(song_ids)}")

        else:
            print("Sorry!\nYour selection has 0 results.")
            print("Please try again.")
        return selected

def sort(Song_ids):
    while True:
        print("Sort Songs ....")
        print("01. By Song Title \n02. By times played \n03. By Added Date \n04. Exit Sort")
        user_choice = input("Enter your choice: ")
        if user_choice.lower() in ["1", "01", "song", "by song","2","02","by times played","times played","3", "03","by added date" , "added date", "exit sort", "4", "04"]:
            break
        else:
            print("Invalid input. Please try again.")
            continue

    if user_choice.lower() in ["1", "01", "title", "by song title"]:
        while True:
            print("\nSort Songs by song Title ....")
            print("01. Sort ASC \n02. Sort DESC \n03. Exit Sort")
            choice = input("Enter your choice: ")
            if choice.lower() in ["1", "01", "asc", "by asc"]:
                db.sort_by_song_title("ASC",Song_ids)
                break
            elif choice.lower() in ["2", "02", "desc", "by desc"]:
                db.sort_by_song_title("DESC",Song_ids)
                break
            elif choice.lower() in ["3", "03", "exit", "exit sort"]:
                break
            else:
                print("Please enter a valid number.")

    # elif user_choice.lower() in ["2", "02", "by artist"]:
    #     songs.clear()
    #     db.sort_by_artist(songs)

    elif user_choice.lower() in ["2", "02", "by times played", "times played"]:
        while True:
            print("\nSort Songs by times played ....\n( This will be same as sorted by song if you have not used this music_player before.\nSo we recommend playing a few songs before using this sorting method )")
            print("\n01. Most played \n02. Least played \n03. Exit Sorting by times played")
            choice = input("Enter your choice: ")
            if choice.lower() in ["1", "01", "most", "most played"]:
                db.sort_by_times_played("MOST",Song_ids)
                break
            elif choice.lower() in ["2", "02", "least played", "least played"]:
                db.sort_by_times_played("LEAST",Song_ids)
                break
            elif choice.lower() in ["3", "03", "exit", "exit sort"]:
                break
            else:
                print("Please enter a valid number.")

    elif user_choice.lower() in ["3", "03", "by added date","added date"]:
        while True:
            print("\nSort Songs by song Title ....")
            print("01. Sort ASC \n02. Sort DESC \n03. Exit Sort by added date")
            choice = input("Enter your choice: ")
            if choice.lower() in ["1", "01", "asc", "by asc"]:
                db.sort_by_added_time("ASC",Song_ids)
                break
            elif choice.lower() in ["2", "02", "desc", "by desc"]:
                db.sort_by_added_time("DESC",Song_ids)
                break
            elif choice.lower() in ["3", "03", "exit", "exit sort"]:
                break
            else:
                print("Please enter a valid number.")
    elif user_choice.lower() in ["4", "04", "exit", "exit sort"]:
        print("You're exiting the sorting page.")
        return
