from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from blog import models, schemas
from blog.database import get_db

router = APIRouter()

@router.get('/blog',response_model=List[schemas.ShowBlog],tags=['BLOGS:'])
def all_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs