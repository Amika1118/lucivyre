import os
import pygame

import store_songs.store_music as sm
import file_handeling.file_handeling as fh

from mutagen import File
from mutagen.id3 import ID3
from mutagen.mp3 import HeaderNotFoundError




song_list = []
skipped_songs = 0
arti = 0


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

def main():
    global skipped_songs, arti
    print("Welcome to Lucivyre")
    old_list = sm.check_songs(song_list)
    artist = ""
    length = 0
    for audio_file in old_list:
        try:
            audio = File(audio_file)
            if audio is None:
                print(f"Unsupported or unreadable file: {audio_file}")
                continue
            length = audio.info.length
            artist = get_first_artist(audio_file)

        except HeaderNotFoundError:
            print(f"Skipping {audio_file}")
            skipped_songs = skipped_songs + 1


        print("Song Title: ", os.path.splitext(os.path.basename(audio_file))[0])
        print("Artist: " + artist)
        if artist == "Unknown Artist":
            arti = arti + 1
        print("Length: " , length)

    print(f"{skipped_songs} songs skipped.")
    print(f"{arti} artists skipped.")


main()

