import sqlite3
import requests

conn = sqlite3.connect("../spotilike.sqlite3")
cursor = conn.cursor()

stmt = cursor.execute("SELECT id_tracks from tracks")
conn.commit()
for e in stmt.fetchall():
    url = f"https://api.deezer.com/track/{e[0]}"
    req = requests.get(url)
    data = req.json()
    
    if 'error' in data: continue
    
    print(data["preview"])
    
    # cursor.execute("UPDATE tracks SET image = ")
    # print(e[0])