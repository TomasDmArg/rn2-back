from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# MySQL connection URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Create SQLAlchemy engine with connection pool settings
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=5,
    max_overflow=10
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

def get_db():
    """
    Generator function to get database session.
    Yields a database session and ensures it's closed after use.
    Includes retry mechanism for handling connection errors.
    """
    db = SessionLocal()
    try:
        # Attempt to connect to the database
        retries = 3
        while retries > 0:
            try:
                # Test the connection
                db.execute(text("SELECT 1"))
                yield db
                break
            except OperationalError:
                retries -= 1
                if retries == 0:
                    raise
                time.sleep(1)  # Wait for 1 second before retrying
    finally:
        db.close()