import os
import pygame
from mutagen.mp3 import HeaderNotFoundError

import store_songs.store_music as sm
import file_handeling.file_handeling as fh
from mutagen import File



song_list = []
skipped_songs = 0
arti = 0


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
            try:
                artist = audio.info.artist
            except AttributeError:
                artist = "Unknown Artist"
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

