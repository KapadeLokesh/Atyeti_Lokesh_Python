from typing import List
from fastapi import Depends, FastAPI, HTTPException, status, Response
from blog.database import engine

from blog import models
from blog.routers import authentication, blog,user

models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
 
