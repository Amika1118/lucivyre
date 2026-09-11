import os
import mimetypes

def ask_folder():
    while True:
        user_in = input("Enter the folder path :")
        if os.path.isdir(user_in):
                return user_in
        else:
            print("The folder does not exist\nPlease enter a valid folder path")

def check_songs(song_list):
    while True:
        path = ask_folder()  # existing folder picker

        for name in os.listdir(path):
            full = os.path.join(path, name)

            # must be a file, not a subfolder
            if not os.path.isfile(full):
                continue

            mime, _ = mimetypes.guess_type(full)
            if mime and mime.startswith("audio/"):
                song_list.append(full)
            else:
                print(f"Skipped (not audio): {name}")

        if not song_list:
            print("No audio files found in that folder.")

        # if there is 0 audio files ask for the folder path again
        if len(song_list) != 0:
            print(f"Found {len(song_list)} song(s).")
            break
        else:
            print("No songs found in that folder.\n Please enter a valid folder path")