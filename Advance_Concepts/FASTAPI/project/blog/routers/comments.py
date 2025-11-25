from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/comments", tags=["COMMENTS"])

@router.post("/blogs/{blog_id}/comments", response_model=schemas.CommentResponse)
def create_comment(blog_id: int, comment: schemas.CommentCreate,
                   db: Session = Depends(get_db),
                   current_user = Depends(oauth2.get_current_user)):

    new_comment = models.Comment(
        content=comment.content,
        blog_id=blog_id,
        user_id=current_user.id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/blogs/{blog_id}/comments", response_model=List[schemas.CommentResponse])
def get_comments(blog_id: int, db: Session = Depends(get_db)):
    return db.query(models.Comment).filter(models.Comment.blog_id == blog_id).all()