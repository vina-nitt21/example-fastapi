# database.py

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, sessionmaker, declarative_base
from sqlalchemy import create_engine
from psycopg2.extras import RealDictCursor
import os
import psycopg2
import time

# Load your database URL (you can use dotenv or hardcode it here)
DATABASE_URL = "postgresql://postgres:password@localhost/fastapi"

# Async engine
engine = create_engine(DATABASE_URL, echo=True)

# Async session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


max_retries = 5
attempts = 0
    #inport library - psycopg that gives u the driver to connect to db
while attempts < max_retries:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connected successfully")
        break
    except Exception as error:
        print("failed connection to DB", error)
        attempts += 1
        time.sleep(5)

if attempts == max_retries:
    raise ConnectionError("Max retries exceeded. Database unavailable.")