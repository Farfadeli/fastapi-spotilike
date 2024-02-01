from sqlalchemy import Column, ForeignKey, Integer, String
from . import alchemy

class users(alchemy.Base):
    __tablename__ = "users"
    
    id_user = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    mail = Column(String, nullable=False)
    password = Column(String, nullable=False)

class genres(alchemy.Base):
    __tablename__ = "genres"
    
    id_genre = Column(Integer, primary_key=True)
    title = Column(String, primary_key=True)
    description = Column(String, nullable=False)

class artists(alchemy.Base):
    __tablename__ = "artists"
    
    id_artist = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    avatar = Column(String, nullable=False)
    biography = Column(String, nullable=False)

class albums(alchemy.Base):
    __tablename__ = "albums"
    
    id_album = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    cover = Column(String, nullable=False)
    release_date = Column(String, nullable=False)
    
class tracks(alchemy.Base):
    __tablename__ = "tracks"
    
    id_tracks = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    id_album = Column(Integer, ForeignKey("albums.id_album"))

class artist_albums(alchemy.Base):
    __tablename__ = "artist_albums"
    
    id = Column(Integer, primary_key=True)
    id_album = Column(Integer, ForeignKey("albums.id_album"))
    id_artist = Column(Integer, ForeignKey("artists.id_artist"))

class track_genres(alchemy.Base):
    __tablename__ = "track_genres"
    
    id = Column(Integer, primary_key=True)
    id_tracks = Column(Integer, ForeignKey("tracks.id_tracks"))
    id_genre = Column(Integer, ForeignKey("genres.id_genre"))