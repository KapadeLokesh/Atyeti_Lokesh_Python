from contextlib import asynccontextmanager
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status, Response
from blog.database import APP_ENV, engine
from fastapi.middleware.cors import CORSMiddleware
from blog import models
from blog.routers import authentication, blog, user, vote, comments
import os
from migrate import run_migrations

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(debug=True, lifespan=lifespan)

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
app.include_router(comments.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to FastAPI Blog API",
        "environment": APP_ENV,
    }
