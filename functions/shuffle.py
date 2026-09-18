import file_handeling.handle_data
import file_handeling.read_n_write as rw
import functions.sort as sr

credits_file = file_handeling.handle_data.credit_csv_path
songs_file = file_handeling.handle_data.songs_csv_path
sorted_songs, reverse_sorted_songs = sr.sort_by_title()

songs = {}
song_credits = {}


def shuffle():
    print("Hello World")


def deduct_credits(song_id, played_time):
    """Reduce a song's credits based on how much of it was actually played."""
    # 1. Load data
    song_credits.clear()
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
        new_credit = float((float(credit) * float(fraction_played))/10)
    else:
        new_credit = credit

    # 4. Update the dict
    song_credits[song_id] = [artist, length, new_credit]

    # 5. Save back to CSV
    header = ["Id", "length", "song_credits"]
    rw.write_songs(credits_file, song_credits,header)



def add_credits(song_list):
    print("Adding Credits")
    song_credits.clear()
    rw.read_songs(credits_file, song_credits)
    new_credit = 0

    for song_ids, data in song_credits.items():
        for song in song_list:
            if song_ids == song:
                song_id = song
                length = float(data[0])
                credit = float(data[1])

                if len(song_list) == 1:
                    new_credit = credit + 0.1
                elif 1 < len(song_list):
                    new_credit = credit + 0.05

                credit = new_credit
                song_credits[song_id] = [length, credit]


