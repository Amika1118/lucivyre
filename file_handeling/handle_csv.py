import read_n_write as rw
from pathlib import Path

songs = {}

# getting the file path without issues.
BASE_DIR = Path(__file__).resolve().parent.parent
credit_csv_path = BASE_DIR / "data" / "credits" / "credits.csv"
full_data_path = BASE_DIR / "data" / "song_data" / "full_data.csv"

rw.read_songs(full_data_path, songs)

for song in songs:
    print(song)


