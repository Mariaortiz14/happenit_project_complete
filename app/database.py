from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#DATABASE_URL = "mysql+pymysql://root:00000@localhost/Happenit"
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:YTBeOxWoqBQXbtmqhPpXjPEMXkfJUguY@tramway.proxy.rlwy.net:28729/railway")
#DATABASE_URL = "mysql+pymysql://root:CUYVxFKvxjqKcpGKxWAcbKiBeSCtdMrh@monorail.proxy.rlwy.net:3306/happenit"
#DATABASE_URL = "mysql+pymysql://root:Xyz123asd456@monorail.proxy.rlwy.net:3306/happenit"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin123')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'happenit')

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''