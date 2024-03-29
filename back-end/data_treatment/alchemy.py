from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_DATABASE_URL = "sqlite:///././spotilike.sqlite3"

print(SQL_DATABASE_URL)

engine = create_engine(
    SQL_DATABASE_URL, connect_args={"check_same_thread": False}
)

Session_local = sessionmaker(autocommit= False, autoflush=False, bind=engine)

Base = declarative_base()