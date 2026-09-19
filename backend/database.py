import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# .env file se environment variables load karo
load_dotenv()

# .env se database credentials nikalna
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# MySQL connection URL banana
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy engine banana (yeh actual connection handle karta hai)
engine = create_engine(DATABASE_URL, echo=True)

# Session banane ka factory (har request ke liye ek session milega)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class jisse hum apne models (tables) banayenge
Base = declarative_base()

# Dependency function - FastAPI routes isko use karenge DB session lene ke liye
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()