from fastapi import APIRouter, Depends, HTTPException, status
from blog import models, schemas
from sqlalchemy.orm import Session
from blog.database import get_db
from blog.hashing import Hash
from blog.token import create_access_token

router = APIRouter(
    tags=['AUTHENTICATION:']
)

@router.post('/login')
def login(request:schemas.Login, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Incorrect Password")
    
    access_token = create_access_token(data={"sub":user.email})

    return {"access_token":access_token, "token_type":"bearer"}



