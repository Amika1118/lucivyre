import csv
import json

# the csv writer
def write_songs(header,file, dictionary):
    with open(file, "w", newline="", encoding="utf-8") as csvfile:  # clear file safely

        writer = csv.writer(csvfile)
        if header:
            writer.writerow(header)
        for title in dictionary:
            writer.writerow([title] + dictionary[title])

# the csv reader
def read_songs(file,dictionary):
    dictionary.clear()
    with open(file, "r", newline="", encoding="utf-8") as csvfile:

        reader = csv.reader(csvfile)
        next(reader, None)  # skip the first row (header)

        for row in reader:
            if row:
                if len(row) == 4:
                    title = row[0]
                    artist = row[1]
                    length = row[2]
                    credits = row[3]
                    dictionary[title] = [artist] + [length] + [credits]
                elif len(row) == 9:
                    id = row[0]
                    title = row[1]
                    artist = row[2]
                    length = row[3]
                    audio_type = row[4]
                    credits = row[5]
                    file_path = row[6]
                    times_played = row[7]
                    date_added = row[8]
                    dictionary[id] = [title] + [artist] + [length] + [audio_type] + [credits] + [file_path] + [times_played] + [date_added]