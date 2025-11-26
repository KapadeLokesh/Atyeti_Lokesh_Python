import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

def env() -> str:
    if os.getenv("RENDER") or os.getenv("RENDER_SERVICE_ID"):
        return "render"
    if os.path.exists("/.dockerenv"):
        return "docker"
    return "local"

APP_ENV = env()

if APP_ENV == "local":
    load_dotenv()
elif APP_ENV == "docker":
    if os.path.exists(".env.docker"):
        load_dotenv(".env.docker")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing!")

if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

if APP_ENV == "local" and "@db" in SQLALCHEMY_DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("@db", "@localhost")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        