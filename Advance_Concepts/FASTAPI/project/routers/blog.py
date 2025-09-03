from typing import List
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from blog import models, schemas
from blog.database import get_db
from repository import blog


router = APIRouter(
    # prefix="/blog",
    tags=['BLOGS:']
)

@router.get('/',response_model=List[schemas.ShowBlog])
def all_blog(db: Session = Depends(get_db)):
    return blog.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request:schemas.Blog, db: Session= Depends(get_db)):
    return blog.create(request, db)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db)):
    return blog.delete(id,db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(id,request,db)


@router.get('/{id}',status_code=200,response_model=schemas.ShowBlog)
def blog_By_Id(id:int ,response =Response, db:Session = Depends(get_db)):
    return blog.show(id,db)


