from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models,schemas

def get_all(db:Session):
   return db.query(models.Blog).all()
    

def create(request:schemas.BlogCreate, db:Session, user_id :int):
    blog = models.Blog(title=request.title, body=request.body, user_id = user_id )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


def delete(id:int,db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Deleted"}

def update(id:int,request:schemas.BlogCreate, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    blog_obj = blog.first()
    if not blog_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not found."
        )
    
    blog.update(request.model_dump(), synchronize_session=False)  # type: ignore
    db.commit()
    return blog_obj

def show(id:int,db:Session):
    blogs = (db.query(models.Blog, func.count(models.Vote.blogid).label("votes")) \
        .join(models.Vote, models.Vote.blogid == models.Blog.id, isouter=True).group_by(models.Blog.id). \
            filter(models.Blog.id == id).first())
    
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")
    blog, votes = blogs
    return {**blog.__dict__, "votes": votes}




