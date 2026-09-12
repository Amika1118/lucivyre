import csv
import json

def file_handling(file,Songs):
    def write_songs():
        with open(file, "w", newline="") as csvfile:  # clear file safely

            writer = csv.writer(csvfile)
            for title in Songs:
                writer.writerow([title] + Songs[title])


    def read_songs():
        Songs.clear()
        with open(file, "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    title = row[0]
                    year = row[1]
                    country = row[2]
                    rating = row[3]
                    genre_ids = [g.strip() for g in row[4:] if g.strip()]
                    Songs[title] = [year] + [country] + [rating] + genre_ids