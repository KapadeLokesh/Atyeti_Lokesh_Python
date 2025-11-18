import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Get base DATABASE_URL from .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL not set. Please define it in your .env file.")

# Detect if running inside Docker automatically
def is_running_in_docker() -> bool:
    # Docker sets this file in all containers
    return os.path.exists("/.dockerenv")

IN_DOCKER = is_running_in_docker()
APP_ENV = "docker" if IN_DOCKER else "local"

# Adjust for Render / Docker / Local 
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# # Auto-adjust host depending on environment
# if not IN_DOCKER and SQLALCHEMY_DATABASE_URL and "host.docker.internal" in SQLALCHEMY_DATABASE_URL: # type: ignore
#     # Replace Docker hostname with localhost for local run
#     SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("host.docker.internal", "localhost") # type: ignore

if not IN_DOCKER:
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("@db:", "@localhost:")

# SQLAlchemy setup
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()