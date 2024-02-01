from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session

from data_treatment import crud, models, schemas, alchemy
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware
import requests

origins = [
    "http://localhost:3000",
]

allowed_methods = ["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"]
allowed_headers = [
    "Content-Type",
    "Authorization",
]




load_dotenv()

app = FastAPI()


# Configurer les options
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=allowed_methods,
    allow_headers=allowed_headers,
)

def get_db():
    db = alchemy.Session_local()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"Message" : "Hello, world!"}

@app.get("/api/artists", response_model=list[schemas.artists])
def get_all_artist(db : Session = Depends(get_db)):
    return crud.get_all_artists(db)

@app.get("/api/albums", response_model=list[schemas.albums])
def get_all_albums(db: Session = Depends(get_db)):
    return crud.get_all_albums(db)

@app.get("/api/albums/{album_id}", response_model=schemas.albums)
def get_albums(album_id : int, db: Session = Depends(get_db)):
    return crud.get_albums(album_id=album_id, db=db)

@app.get("/api/albums/{album_id}/songs", response_model=list[schemas.tracks])
def get_tracks_of_album(album_id: int, db: Session = Depends(get_db)):
    return crud.get_tracks_of_albums(album_id=album_id, db=db)

@app.get("/api/genres", response_model=list[schemas.genres])
def get_all_genres(db: Session = Depends(get_db)):
    return crud.get_all_genres(db=db)

@app.get("/api/artists/{artist_id}/songs", response_model=list[schemas.tracks])
def get_tracks_of_artist(artist_id: int, db : Session = Depends(get_db)):
    return crud.get_tracks_of_artist(artist_id=artist_id, db=db)

@app.get("/api/artists/{artist_id}/albums", response_model=list[schemas.albums])
def get_albums_of_artist(artist_id: int , db : Session = Depends(get_db)):
    return crud.get_albums_of_artist(artist_id=artist_id, db=db)

# POST PATH

@app.post("/api/users/login")
async def create_user(user: schemas.create_user, db: Session = Depends(get_db)):
    return crud.create_user(user=user, db=db)

@app.post("/api/albums")
def create_album(album: schemas.albums, db: Session = Depends(get_db)):
    return crud.create_album(album=album, db=db)

@app.post("/api/albums/{album_id}/songs")
def create_track(track: schemas.tracks, album_id: int, db: Session = Depends(get_db)):
    return crud.create_track(track=track, album_id=album_id, db=db)

# PATCH PATH

@app.patch("/api/artist/{artist_id}")
def modify_artist(artist_id: int, artist: schemas.modify_artist, db: Session = Depends(get_db)):
    return crud.modify_artist(artist_id=artist_id, artist=artist, db=db)

@app.patch("/api/albums/{album_id}")
def modify_album(album_id: int, album: schemas.modify_album, db: Session = Depends(get_db)):
    return crud.modify_albums(album_id=album_id, album=album, db=db)

@app.patch("/api/genres/{genre_id}")
def modify_genre(genre_id: int , genre: schemas.modify_genre, db: Session = Depends(get_db)):
    return crud.modify_genre(genre_id=genre_id, genre=genre, db=db)

# DELETE PATH

@app.delete("/api/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(user_id=user_id, db=db)

@app.delete("/api/albums/{album_id}")
def delete_album(album_id: int, db : Session = Depends(get_db)):
    return crud.delete_albums(album_id=album_id, db=db)

@app.delete("/api/artist/{artist_id}")
def delete_artist(artist_id: int, db: Session = Depends(get_db)):
    return crud .delete_artist(artist_id=artist_id, db=db)