import sqlite3
import requests

conn = sqlite3.connect("../spotilike.sqlite3")
cursor = conn.cursor()

nb_genre = 20

for e in range(1, nb_genre+1):
    url = f"https://api.deezer.com/genre/{e}"
    
    req= requests.get(url)
    data = req.json()
    
    if 'error' in data: continue
    
    cursor.execute("INSERT INTO genres(id_genre, title, description) VALUES(?,?,?)", (data["id"], data["name"], "Lorem Ipsum"))
    conn.commit()

cursor.close()
conn.close()