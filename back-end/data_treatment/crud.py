from sqlalchemy.orm import Session
from sqlalchemy import update, delete, insert
from . import schemas, models
from sqlalchemy.sql import text
from cryptography.hazmat.primitives import serialization
import jwt
from dotenv import load_dotenv
import os



load_dotenv()

def get_all_albums(db: Session):
    return db.query(models.albums).all()

def get_albums(db: Session, album_id : int):
    return db.query(models.albums).filter(models.albums.id_album == album_id).first()

def get_tracks_of_albums(db: Session, album_id: int):
    return db.query(models.tracks).join(models.albums).filter(models.albums.id_album == album_id).all()

def get_all_genres(db: Session):
    return db.query(models.genres).all()

def get_tracks_of_artist(db: Session, artist_id):
    return db.query(models.tracks).join(models.albums).join(models.artist_albums).join(models.artists).filter(models.artists.id_artist == artist_id).all()

def create_user(db: Session, user: schemas.create_user):
    
    encoded_jwt = jwt.encode({"password" : user.password}, os.getenv('SECRET'), algorithm="HS256")
    
    print(encoded_jwt)
    
    db_user = models.users(username=user.username , mail=user.mail, password=encoded_jwt)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def create_album(db: Session, album: schemas.albums):
    db_album = models.albums(id_album=album.id_album, title=album.title, cover=album.title, release_date=album.release_date)
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

def create_track(db: Session, album_id: int, track: schemas.tracks):
    db_track = models.tracks(id_tracks=track.id_tracks, title=track.title, duration=track.duration, id_album=album_id)
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track

def modify_artist(db: Session, artist_id: int, artist: schemas.modify_artist):
    db.execute(update(models.artists).where(models.artists.id_artist == artist_id).values(name=artist.name,avatar=artist.avatar,biography=artist.biography))
    db.commit()
    
    return {"code" : 200}

def modify_albums(db : Session, album_id: int, album: schemas.modify_album):
    db.execute(update(models.albums).where(models.albums.id_album == album_id).values(title=album.title,cover=album.cover,release_date=album.release_date))
    db.commit()
    
    return {"code" : 200}

def modify_genre(db: Session, genre_id: int, genre: schemas.modify_genre):
    db.execute(update(models.genres).where(models.genres.id_genre == genre_id).values(title=genre.title,description=genre.description))
    db.commit()
    
    return {"code" : 200}

def delete_user(db: Session, user_id: int):
    db.execute(delete(models.users).where(models.users.id_user == user_id))
    db.commit()
    
    return {"code" : 200}

def delete_albums(db: Session, album_id: int):
    db.execute(delete(models.tracks).where(models.tracks.id_album == album_id))
    db.commit()
    
    db.execute(delete(models.albums).where(models.albums.id_album == album_id))
    db.commit()
    
    return {"code": 200}

def delete_artist(db: Session, artist_id: int):
    clear = text(f""" DELETE FROM track_genres
    WHERE track_genres.id_tracks in (
	SELECT id_tracks from tracks
	WHERE tracks.id_album IN (
		SELECT id_album FROM albums
		WHERE albums.id_album IN( 
			SELECT id_album FROM artist_albums
			WHERE artist_albums.id_artist IN(
				SELECT id_artist FROM artists
				WHERE artists.id_artist = {artist_id}
			)
		))) """)
    db.execute(clear)
    db.commit()
    
    clear = text(f"""
	DELETE from tracks
	WHERE tracks.id_album IN (
		SELECT id_album FROM albums
		WHERE albums.id_album IN( 
			SELECT id_album FROM artist_albums
			WHERE artist_albums.id_artist IN(
				SELECT id_artist FROM artists
				WHERE artists.id_artist = {artist_id}
			)
		)) """)
    db.execute(clear)
    db.commit()
    
    clear = text(f"""
		DELETE FROM albums
		WHERE albums.id_album IN( 
			SELECT id_album FROM artist_albums
			WHERE artist_albums.id_artist IN(
				SELECT id_artist FROM artists
				WHERE artists.id_artist = {artist_id}
			)
		) """)
    db.execute(clear)
    db.commit()
    
    clear = text(f"""
			DELETE FROM artist_albums
			WHERE artist_albums.id_artist IN(
				SELECT id_artist FROM artists
				WHERE artists.id_artist = {artist_id}
			)
		 """)
    db.execute(clear)
    db.commit()
    
    clear = db.query(models.artists).where(models.artists.id_artist == artist_id)
    for e in clear:
        db.delete(e)
    db.commit()
    
    return {"code": 200}

