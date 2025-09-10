from typing import List
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from blog.database import get_db
from blog.hashing import Hash
from .. import hashing
from blog.repository import user

router = APIRouter(
    prefix="/user",
    tags=['USERS:']
)

@router.post('/',response_model=schemas.ShowUser)
def create_user(request: schemas.User, db:Session = Depends(get_db)):
    hashed_pw = hashing.Hash.bcrypt(request.password)
    new_user = models.User(name = request.name, email = request.email, password =hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',status_code=200,response_model=schemas.ShowUser)
def user_By_Id(id, db:Session = Depends(get_db)):
    return user.show(id,db)

