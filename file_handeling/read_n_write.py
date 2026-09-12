import csv
import json



def write_songs(header,file, dictionary):
    with open(file, "w", newline="", encoding="utf-8") as csvfile:  # clear file safely

        writer = csv.writer(csvfile)
        if header:
            writer.writerow(header)
        for title in dictionary:
            writer.writerow([title] + dictionary[title])


def read_songs(header, file,dictionary):
    dictionary.clear()
    with open(file, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                if len(row) == 3:
                    title = row[0]
                    artist = row[1]
                    credits = row[2]
                    dictionary[title] = [artist] + [credits]
                elif len(row) == 8:
                    id = row[0]
                    title = row[1]
                    artist = row[2]
                    length = row[3]
                    audio_type = row[4]
                    credits = row[5]
                    file_path = row[6]
                    times_played = row[7]
                    dictionary[id] = [title] + [artist] + [length] + [audio_type] + [credits] + [file_path] + [times_played]