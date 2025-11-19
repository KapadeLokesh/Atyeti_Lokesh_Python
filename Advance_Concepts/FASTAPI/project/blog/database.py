import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Detect if running inside Docker automatically
def is_running_in_docker() -> str:
    # Docker sets this file in all containers
    if os.getenv("RENDER") or os.getenv("RENDER_SERVICE_ID"):
        return "render"
    if os.path.exists("/.dockerenv"):
        return "docker"
    return "local"

IN_DOCKER = is_running_in_docker()
APP_ENV = IN_DOCKER

if "RENDER" not in os.environ and "RENDER_INTERNAL_HOSTNAME" not in os.environ:
    load_dotenv()
# Get base DATABASE_URL from .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL not set. Please define it in your .env file.")

# Adjust for Render / Docker / Local 
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

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