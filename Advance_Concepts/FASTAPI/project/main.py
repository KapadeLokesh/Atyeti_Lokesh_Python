from typing import List
from fastapi import Depends, FastAPI, HTTPException, status, Response
from blog.database import engine
from fastapi.middleware.cors import CORSMiddleware
from blog import models
from blog.routers import authentication, blog, user, vote

# models.Base.metadata.create_all(engine)

app = FastAPI(debug=True)

# origins = ["https://www.google.com"]
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
    return {"message":"Hello from Render...!"}

 
