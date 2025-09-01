from fastapi import FastAPI
from . import schemas,models
from .database import engine
from .schemas import Blog

models.Base.metadata.create_all(engine)

app = FastAPI()

@app.post('/blog')
def create(request:schemas.Blog):
    return request