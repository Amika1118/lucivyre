import os
import mimetypes

from mutagen import File
from mutagen.id3 import ID3
from mutagen.mp3 import HeaderNotFoundError
from pathlib import Path

old_list = []
skipped_songs = 0
arti = 0

# asks for a pah from the user if audio files exists it returns
# if not asks for a pth until user enters a valid path.
def ask_folder():
    while True:
        user_in = input("Enter the folder path :")
        if os.path.isdir(user_in):
                return user_in
        else:
            print("The folder does not exist\nPlease enter a valid folder path")

def get_first_artist(path):
    # Try raw ID3 first (MP3)
    try:
        tags = ID3(path)
        frame = tags.get("TPE1")
        if frame and frame.text:
            raw = str(frame.text[0])
            first = raw.split("\x00")[0].split("/")[0].strip()
            if first:
                return first
    except Exception:
        pass

    # Fallback: easy interface for other formats .m4a and other formats.
    try:
        audio = File(path, easy=True)
        if audio and audio.tags:
            val = audio.get("artist")
            if val:
                raw = str(val[0])
                return raw.split("\x00")[0].split("/")[0].strip()
    except Exception:
        pass

    return "Unknown"

def get_audio_type(path):
    try:
        file_type = Path(path).suffix.lower()
        return file_type
    except Exception:
        return "Unknown"

# new_list is retuned with name, artist and the length of the song
# old_list has the path of every song
def check_songs(new_list):
    global skipped_songs, artist, length, arti, file_type, file_path
    while True:
        path = ask_folder()  # existing folder picker

        for name in os.listdir(path):
            full = os.path.join(path, name)

            # must be a file, not a subfolder
            if not os.path.isfile(full):
                continue
            # checking the type to only get the audio
            mime, _ = mimetypes.guess_type(full)
            if mime and mime.startswith("audio/"):
                old_list.append(full)
                try:
                    audio = File(full)
                    if audio is None:
                        print(f"Unsupported or unreadable file: {full}")
                        continue
                    length = audio.info.length
                    artist = get_first_artist(full)
                    file_type = get_audio_type(full)
                    file_path = full

                except HeaderNotFoundError:
                    print(f"Skipping {full}")
                    skipped_songs = skipped_songs + 1

                if artist == "Unknown Artist":
                    arti = arti + 1

                new_list[os.path.splitext(os.path.basename(full))[0]] =  [length] + [artist] + [file_type] + [file_path]
            else:
                print(f"Skipped (not audio): {name}")

        if not old_list:
            print("No audio files found in that folder.")

        # if there is 0 audio files ask for the folder path again
        if len(old_list) != 0:
            print(f"Found {len(old_list)} song(s).")
            return old_list
        else:
            print("No songs found in that folder.\n Please enter a valid folder path")