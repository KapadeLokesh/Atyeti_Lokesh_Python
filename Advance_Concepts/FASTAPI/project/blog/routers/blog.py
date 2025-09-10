from typing import List
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas
from blog.database import get_db
from blog.repository import blog


router = APIRouter(
    # prefix="/blog",
    tags=['BLOGS:']
)

@router.get('/',response_model=List[schemas.ShowBlog])
def all_blog(db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    return blog.get_all(db)

@router.post('/', status_code = status.HTTP_201_CREATED,response_model=schemas.ShowBlog)
def create(request:schemas.BlogCreate, db: Session= Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    return blog.create(request, db, user_id= current_user.id)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db),current_user= Depends(oauth2.get_current_user)):
    blog.delete(id,db)
    return {}

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowBlog)
def update_blog(id: int, request: schemas.BlogCreate, db: Session = Depends(get_db),current_user= Depends(oauth2.get_current_user)):
    return blog.update(id,request,db)

@router.get('/{id}',status_code=200,response_model=schemas.ShowBlog)
def blog_By_Id(id:int , db:Session = Depends(get_db),current_user= Depends(oauth2.get_current_user)):
    return blog.show(id,db)


