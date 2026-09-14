import file_handeling.handle_csv
import file_handeling.read_n_write as rw

songs = {}
sorted_songs = {}
reverse_sorted_songs = {}

original = []
reverse = []
full_data_csv = file_handeling.handle_csv.full_data_path

def sort_by_title():
    rw.read_songs(full_data_csv,songs)
    for song_id, data in songs.items():
        title = data[0]
        original.append(title)
        reverse.append(title)

    original.sort()
    reverse.sort(reverse=True)

    for title in original:
        for song_id, data in songs.items():
            if title == data[0]:
                sorted_songs[song_id] = data

    for title in reverse:
        for song_id, data in songs.items():
            if title == data[0]:
                reverse_sorted_songs[song_id] = data

    return sorted_songs, reverse_sorted_songs

def sort_by_artist():
    rw.read_songs(full_data_csv,songs)

    for song_id, data in songs.items():
        artist = data[1]
        if artist not in original:
            original.append(artist)

    original.sort()
    for artist in original:
        for song_id, data in songs.items():
            if artist == data[1]:
                sorted_songs.setdefault(artist, []).append(song_id)

    return sorted_songs

def sort_by_date():
    rw.read_songs(full_data_csv,songs)

    for song_id, data in songs.items():
        date_added = data[-1]
        if date_added not in original:
            original.append(date_added)
            reverse.append(date_added)

    original.sort()
    reverse.sort(reverse=True)

    for date_added in original:
        for song_id, data in songs.items():
            if date_added == data[-1]:
                sorted_songs.setdefault(date_added, []).append(song_id)

    for date_added in reverse:
        for song_id, data in songs.items():
            if date_added == data[-1]:
                reverse_sorted_songs.setdefault(date_added, []).append(song_id)

    return sorted_songs, reverse_sorted_songs
    
def sort_by_times_played():
    rw.read_songs(full_data_csv,songs)
    for song_id, data in songs.items():
        times_played = data[6]
        if times_played not in original:
            original.append(times_played)

    original.sort()

    for times_played in original:
        for song_id, data in songs.items():
            if times_played == data[6]:
                sorted_songs.setdefault(times_played, []).append(song_id)

    return sorted_songs
