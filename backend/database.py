import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# .env फाईलमधून environment variables लोड करा
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Database शी जोडणी (engine) तयार करा
engine = create_engine(DATABASE_URL)

# प्रत्येक request साठी नवीन database session तयार करण्यासाठी
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# सर्व डेटाबेस मॉडेल्स (tables) या Base वरून तयार होतील
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()