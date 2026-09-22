import math, random
import file_handeling.handle_data
import file_handeling.read_n_write as rw
import functions.sort as sr
import file_handeling.db as db

credits_file = file_handeling.handle_data.credit_csv_path
songs_file = file_handeling.handle_data.songs_csv_path
sorted_songs, reverse_sorted_songs = sr.sort_by_title()

# These two dicts live at the top of the file so every function can see them.
# They stick around between calls, so whoever uses them has to clear or
# reload them before trusting what's inside.
songs = {}
song_credits = {}

# Every song starts life with 10 credits.
INITIAL_CREDITS = 10


def effective_score(credits):
    # Turns raw credits into a "weight" for the shuffle.
    # Bigger weight = plays sooner.

    # Three tiers:
    #   above 15   → favorite, boost it 3x
    #   below 5    → fading out, cut it to a tenth
    #   in between → leave it alone
    if credits > 15.0:
        return credits * 3.0
    if credits < 5.0:
        # Floor at 0.05 so we never divide by zero later
        return max(credits, 0.05) * 0.1
    return credits


def shuffle(shuffled_list):
    # Shuffle the songs, but "cheat" toward higher-credit ones.
    # A low-credit song can still sneak in - it's random, just weighted.

    # Trick: give each song a random key = log(u) / weight.
    # Sort by that key, biggest first. Higher weight → bigger key → plays sooner.
    songs.clear()
    db.read_data_from_db(songs)

    # Whatever order comes out, dump the IDs into shuffled_list.
    keys = []
    for song_id, data in songs.items():
        credits = float(data[3])                          # credits are at position 3
        s_prime = effective_score(credits)                # apply the tier boost/cut
        u = random.uniform(0.0001, 0.9999)          # random 0..1, avoid the edges
        k = math.log(u) / s_prime                         # always negative, bigger = better
        keys.append((k, song_id))

    # Highest key first
    keys.sort(key=lambda x: x[0], reverse=True)

    # Copy just the IDs out, in order
    for _, song_id in keys:
        shuffled_list.append(song_id)


def deduct_credits(song_id, played_time):
    # Take credits away from a song depending on how much of it you actually heard.

    # Played it all the way → keep all credits.
    # Skipped halfway       → keep half.
    # Skipped instantly     → keep basically nothing.

    # Watch out: played_time and length must be in the SAME unit (both seconds,
    # or both milliseconds). Mixing them up = the fraction gets clamped and
    # nothing gets deducted.

    # Load the current credit table
    song_credits.clear()
    
    # rw.read_songs(full_data_csv, songs)           # this was the previous way which read a csv and then populated a dictionary
    db.read_data_from_db(song_credits)              # now we directly read form sqlite database and populate the same dictionary

    # Song isn't in the table? Nothing to do.
    if song_id not in song_credits:
        print(f"Song {song_id} not found.")
        return

    # Unpack the row: [artist, length, credit]
    # artist, length, credit = song_credits[song_id]
    # length = float(length)
    # credit = float(credit)

    length = 0.0
    credit = 0.0

    for song_id, data in song_credits[song_id].items():
        length = float(data[2])
        credit = float(data[3])


    # Figure out the new credit value
    if length > 0:
        # Clamp to [0, 1] in case played_time is weird
        fraction = max(0.0, min(1.0, played_time / length))
        new_credit = round(credit * fraction, 3)
    else:
        # Song has no length? Don't touch the credits.
        new_credit = credit


    # update the database.
    db.update_db(song_id.lower(), new_credit)


    # this for the csv file
    song_credits.clear()
    song_credits[song_id] = [length, new_credit]

    # Save the file
    rw.write_songs(credits_file, song_credits,
                   ["song_id", "length", "song_credits"])


def add_credits(song_list):
    # Give a little bonus to songs you searched for.
    # If you picked one specific song → +0.10
    # If you picked a bunch at once    → +0.05 each

    # Idea: searching for a song shows you wanted it, so it deserves a nudge.

    # Load the current credit table
    global credit, song_id
    song_credits.clear()

    # rw.read_songs(full_data_csv, songs)                  # this was the previous way which read a csv and then populated a dictionary
    db.read_data_from_db(song_credits)                     # now we directly read form sqlite database and populate the same dictionary

    # Bigger bonus for a single careful pick than for a batch
    bonus = 0.1 if len(song_list) == 1 else 0.05

    for song_id in song_list:
        # Skip anything that isn't in the credits table
        if song_id not in song_credits.keys():
            continue

        # Unpack the row: [artist, length, credit]
        artist, length, credit = song_credits[song_id]

        # Add the bonus. round(...) keeps values tidy - otherwise you get
        # numbers like 7.850000000000001 after a few additions.
        song_credits[song_id] = [float(length),
                                 round(float(credit) + bonus, 3)]

        # update the database
        db.update_db(song_id.lower(), round(float(credit) + bonus, 3))

    # Save the file
    rw.write_songs(credits_file, song_credits,
                   ["song_id", "length", "song_credits"])