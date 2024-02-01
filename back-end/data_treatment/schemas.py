from pydantic import BaseModel

class albums(BaseModel): 
    id_album : int
    title : str
    cover: str
    release_date: str
    
    class config:
        orm_mode = True

class tracks(BaseModel):
    id_tracks : int
    title: str
    duration: int
    preview: str
    
    class config:
        orm_mode = True

class genres(BaseModel):
    id_genre : int
    title: str
    description : str
    
    class config:
        orm_mode = True

class artists(BaseModel):
    id_artist: int
    name: str
    avatar: str
    biography: str
    
    class config:
        orm_mode = True

class create_user(BaseModel):
    username: str = ""
    mail: str = ""
    password: str = ""


class modify_artist(BaseModel):
    name: str
    avatar: str
    biography: str
    
class modify_album(BaseModel):
    title: str
    cover: str
    release_date: str
    
class modify_genre(BaseModel):
    title: str
    description: str
    