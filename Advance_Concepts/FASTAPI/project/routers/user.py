from typing import List
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from blog import models, schemas
from blog.database import get_db
from blog.hashing import Hash
from repository import user

router = APIRouter(
    prefix="/user",
    tags=['USERS:']
)

@router.post('/',response_model=schemas.ShowUser,tags=['USERS:'])
def create_user(request: schemas.User, db:Session = Depends(get_db)):
    return user.create(request,db)

@router.get('/{id}',status_code=200,response_model=schemas.ShowUser,tags=['USERS:'])
def user_By_Id(id,response =Response, db:Session = Depends(get_db)):
    return user.show(id,db)

