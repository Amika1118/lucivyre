import csv
import json

def file_handling():
    def write_movies():
        with open("Movies.csv", "w", newline="") as csvfile:  # clear file safely

            writer = csv.writer(csvfile)
            for title in Movies:
                writer.writerow([title] + Movies[title])


    def read_movies():
        Movies.clear()
        with open("Movies.csv", "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    title = row[0]
                    year = row[1]
                    country = row[2]
                    rating = row[3]
                    genre_ids = [g.strip() for g in row[4:] if g.strip()]
                    Movies[title] = [year] + [country] + [rating] + genre_ids