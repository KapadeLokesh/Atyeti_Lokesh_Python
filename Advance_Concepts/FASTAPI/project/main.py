from typing import List
from fastapi import Depends, FastAPI, HTTPException, status, Response
from blog.database import APP_ENV, engine
from fastapi.middleware.cors import CORSMiddleware
from blog import models
from blog.routers import authentication, blog, user, vote
import os


# def detect_environment():
#     env = os.getenv("APP_ENV", "auto").lower()
#     if env != "auto":
#         return env

#     if os.path.exists("/.dockerenv"):
#         return "docker"

#     if "RENDER_INTERNAL_HOSTNAME" in os.environ:
#         return "render"

#     return "local"

# APP_ENV = detect_environment()

app = FastAPI(debug=True)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(authentication.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to FastAPI Blog API 🚀",
        "environment": APP_ENV,
        # "in_docker": os.path.exists("/.dockerenv")
    }
