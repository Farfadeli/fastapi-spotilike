import sqlite3
import requests
from random import randint

def get_genre():
    nb_genre = randint(1,4)
    liste = []
    for e in range(nb_genre):
        define_genre= randint(1, 10)
        if define_genre not in liste : liste.append(define_genre)
    return liste

def insert_artist(values):
    conn = sqlite3.connect("../spotilike.sqlite3")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO artists(id_artist, name, avatar, biography) VALUES(?,?,?,?)", values)
    conn.commit()
    
    print("Artist Ajouté :", values[0])

def insert_albums(artist_id, values):
    conn = sqlite3.connect("../spotilike.sqlite3")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO albums(id_album, title, cover, release_date) VALUES(?,?,?,?)", values)
    conn.commit()
    
    cursor.execute("INSERT INTO artist_albums(id_album, id_artist) VALUES(?,?)", (values[0], artist_id))
    conn.commit()
    
    print("\tAlbums ajouter :", values[1])
    


def insert_tracks(values):
    conn = sqlite3.connect("../spotilike.sqlite3")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO tracks(id_tracks, title, duration, id_album) VALUES(?,?,?,?)", values)
    conn.commit()
    
    genres = get_genre()
    
    for e in genres:
        cursor.execute("INSERT INTO track_genres(id_tracks, id_genre) VALUES(?,?)", (values[0], e))
        conn.commit()
    
    print("\t\ttrack ajoutée :", values[0])
    
def add_preview(id_tracks: int ,preview_link: str):
    conn = sqlite3.connect("../spotilike.sqlite3")
    cursor = conn.cursor()
    
    cursor.execute("UPDATE tracks SET preview = ? WHERE id_tracks = ?", (preview_link,id_tracks))
    conn.commit()
    
    print("ADD")


nb_artist = 100

for e in range(1, nb_artist+1):
    url_artist = f"https://api.deezer.com/artist/{e}"
    
    req_artist = requests.get(url_artist)
    data_artist = req_artist.json()
    
    if 'error' in data_artist: continue
    artist_id = data_artist["id"]
    
    #insert_artist((artist_id, data_artist["name"], data_artist["picture_xl"], "Lorem Ipsum Dolores Sit Ame"))
    
    url_albums = f"https://api.deezer.com/artist/{e}/albums"
    req_albums = requests.get(url_albums)
    data_albums = req_albums.json()["data"]
    
    for album in data_albums:
        if 'error' in album : continue
        #insert_albums(artist_id, (album["id"], album["title"], album["cover_xl"], album["release_date"]))
        
        url_tracks = f"https://api.deezer.com/album/{album['id']}/tracks"
        req_tracks = requests.get(url_tracks)
        data_track = req_tracks.json()["data"]
        
        for track in data_track:
            if 'error' in data_track: continue
            add_preview(track["id"], track["preview"])
            #insert_tracks((track["id"], track["title"], track["duration"], album["id"]))
        
    