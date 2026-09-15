import file_handeling.handle_csv
import file_handeling.read_n_write as rw
import functions.sort as sr

credits_file = file_handeling.handle_csv.credit_csv_path
songs_file = file_handeling.handle_csv.songs_csv_path
sorted_songs, reverse_sorted_songs = sr.sort_by_title()

songs = {}
song_credits = {}

def shuffle():
    print("Hello World")


def deduct_credits(song_id, played_time):
    """Reduce a song's credits based on how much of it was actually played."""
    # 1. Load data
    rw.read_songs(credits_file, song_credits)

    # 2. Find the song
    if song_id not in song_credits:
        print(f"Song {song_id} not found.")
        return

    data = song_credits[song_id]
    artist = data[0]
    length = float(data[1])       # seconds
    credit = int(data[2])

    # 3. Compute new credit
    if length > 0:
        fraction_played = played_time / length
        new_credit = int(credit * fraction_played)
    else:
        new_credit = credit

    # 4. Update the dict
    song_credits[song_id] = [artist, length, new_credit]

    # 5. Save back to CSV
    header = []
    rw.write_songs(credits_file, song_credits,header)



def add_credits():
    print("Add Credits")