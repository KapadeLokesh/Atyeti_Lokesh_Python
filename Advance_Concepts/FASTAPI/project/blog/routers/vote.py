from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas,database,models,oauth2

router = APIRouter(
    prefix="/vote",
    tags=['VOTES:']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):

    post = db.query(models.Blog).filter(models.Blog.id == vote.blog_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.blog_id} does not exist")

    vote_query = db.query(models.Vote).filter(
        models.Vote.blogid == vote.blog_id, models.Vote.userid == current_user.id)

    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has alredy voted on post {vote.blog_id}")
        new_vote = models.Vote(blogid=vote.blog_id, userid=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
