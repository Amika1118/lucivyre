# 🎵 Lucivyre

![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/status-in%20development-yellow)
![Database](https://img.shields.io/badge/database-SQLite-07405e?logo=sqlite&logoColor=white)
[![GitHub](https://img.shields.io/badge/repo-lucivyre-181717?logo=github&logoColor=white)](https://github.com/Amika1118/lucivyre)

A little terminal music player I'm building in Python.

## 🎧 What it does

- Reads my songs from a database (used to be a CSV, now SQLite) - a lightweight local store, no external service needed.
- Sorts and shuffles them in different ways, so I can browse by title, artist, date added, or play count.
- Plays them one after another with pause, skip, and stop, so it behaves like a real player instead of just running through a list.
- Shows a timer while a song is playing, so I always know where I am in a track.
- Has a credit system - songs lose credits when I skip them, gain a bit when I search for them - so the shuffle order shifts based on how I actually listen over time.
- Uses those credits to recommend songs I actually like, without needing any external model or service.

## 📁 Files

```
Lucivyre/
├── main.py                 starts everything
├── data/
│   └── lucivyre.db         the database with all songs
├── file_handeling/
│   ├── db.py               database setup and queries
│   └── read_n_write.py     old CSV helpers, kept for backup
├── functions/
│   ├── sort.py             sorting songs by title, artist, date, plays
│   ├── search.py           searching by title or artist
│   └── credits.py          credit math and the weighted shuffle
├── store_songs/
│   └── store_music.py      scanning a folder for new songs
└── ui.py                   terminal drawing helpers
```

## 🚀 How to run

Make sure Python 3.10+ is installed, then:

```
python main.py
```

## ⚙️ How it works

Songs live in a SQLite file. Each song has an ID like `song_0016`, plus title, artist, length, credits, file path, play count, and the date it was added - everything the player needs to browse, sort, and play back lives on that one record.

Credits start at 10. Skip a song and they drop depending on how much you actually listened to - skip it early and the penalty is bigger, skip it near the end and it barely moves. Search for a song and they go up a tiny bit, since going out of your way to look for something is a decent signal you like it. Higher credits mean a song is more likely to show up first when shuffling.

The shuffle is weighted random - not a strict sort. High-credit songs usually come first, but a low-credit one can still sneak in, so a favorite doesn't hog every shuffle and something you haven't heard in a while still gets a chance to come up.

## 📝 Notes

Built this for myself, mostly to learn - no framework doing the heavy lifting, just plain Python working directly with SQLite and the terminal. Code is not fancy, but it works.

> [!NOTE]
> Run it from a real terminal (not PyCharm's Run window) so the timer updates in place instead of scrolling - PyCharm's console doesn't redraw the same way a real terminal does.