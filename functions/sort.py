import file_handeling.handle_data
import file_handeling.read_n_write as rw

# Shared dictionaries and lists used across the sort functions.
songs = {}
sorted_songs = {}
reverse_sorted_songs = {}

# Temporary working lists used to collect and sort the values
original = []   # sorted ascending
reverse = []    # sorted descending

# Path to the full song data CSV
full_data_csv = file_handeling.handle_data.full_data_path


def sort_by_title():
    """Sort songs by title (A→Z and Z→A)."""
    # Clear all the dictionaries before the sorting.
    songs.clear()
    sorted_songs.clear()
    reverse_sorted_songs.clear()

    # Load all song records from the CSV into `songs`
    rw.read_songs(full_data_csv, songs)

    # Collect every title into both working lists
    for song_id, data in songs.items():
        title = data[0]              # data[0] = title
        original.append(title)
        reverse.append(title)

    # Sort the two lists in opposite directions
    original.sort()                  # A → Z
    reverse.sort(reverse=True)       # Z → A

    # Build the ascending result dict: {song_id: data}
    for title in original:
        for song_id, data in songs.items():
            if title == data[0]:
                sorted_songs[song_id] = data

    # Build the descending result dict: {song_id: data}
    for title in reverse:
        for song_id, data in songs.items():
            if title == data[0]:
                reverse_sorted_songs[song_id] = data

    return sorted_songs, reverse_sorted_songs

def sort_by_artist():
    """Group song IDs under each artist name (alphabetical by artist)."""
    songs.clear()
    sorted_songs.clear()
    reverse_sorted_songs.clear()
    rw.read_songs(full_data_csv, songs)

    # Collect unique artist names (data[1] = artist)
    for song_id, data in songs.items():
        artist = data[1]
        if artist not in original:
            original.append(artist)

    # Sort artists alphabetically
    original.sort()

    # For each artist, gather all song IDs that belong to them
    # setdefault ensures the list exists before appending (avoids KeyError)
    for artist in original:
        for song_id, data in songs.items():
            if artist == data[1]:
                sorted_songs.setdefault(artist, []).append(song_id)

    return sorted_songs

def sort_by_date():
    """Group song IDs by date added (ascending and descending)."""
    songs.clear()
    sorted_songs.clear()
    reverse_sorted_songs.clear()
    rw.read_songs(full_data_csv, songs)

    # Collect unique dates (the last field in each record)
    for song_id, data in songs.items():
        date_added = data[-1]
        if date_added not in original:
            original.append(date_added)
            reverse.append(date_added)

    # Sort dates ascending and descending
    original.sort()
    reverse.sort(reverse=True)

    # Build ascending result: {date: [song_id, ...]}
    for date_added in original:
        for song_id, data in songs.items():
            if date_added == data[-1]:
                sorted_songs.setdefault(date_added, []).append(song_id)

    # Build descending result: {date: [song_id, ...]}
    for date_added in reverse:
        for song_id, data in songs.items():
            if date_added == data[-1]:
                reverse_sorted_songs.setdefault(date_added, []).append(song_id)

    return sorted_songs, reverse_sorted_songs

def sort_by_times_played():
    """Group song IDs by play count (ascending)."""
    rw.read_songs(full_data_csv, songs)

    # Collect unique play counts (data[6] = times_played)
    for song_id, data in songs.items():
        times_played = int(data[6])
        if times_played not in original:
            original.append(int(times_played))

    # Sort play counts ascending
    # Converted to int before appending to get the numeric order.
    original.sort()

    # Build result: {times_played: [song_id, ...]}
    for times_played in original:
        for song_id, data in songs.items():
            if times_played == int(data[6]):
                sorted_songs.setdefault(times_played, []).append(song_id)

    return sorted_songs