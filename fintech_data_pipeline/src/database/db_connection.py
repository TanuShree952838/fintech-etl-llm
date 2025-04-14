# src/database/db_connection.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Load environment variables

db_user = os.getenv("DB_USER", "yugabyte")
db_password = os.getenv("DB_PASSWORD", "yugabyte")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5433")
database = os.getenv("DB_NAME", "yugabyte")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{database}"

# Database setup
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
