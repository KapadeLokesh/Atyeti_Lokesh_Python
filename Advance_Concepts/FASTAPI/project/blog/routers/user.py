import csv
import io
import json
import os
import tempfile
from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends, Query, Response, status, HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
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

MAX_SIZE = 15 * 1024 * 1024

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

@router.get("/{id}/blogs")
def user_blogs(id,format : str=Query("json",enum = ["json","csv"]),
               db: Session = Depends(get_db),
               background_tasks:BackgroundTasks = None): # type: ignore
    user = db.query(models.User).filter(models.User.id ==id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    
    blogs = [{"id": b.id, "title": b.title, "body": b.body} for b in user.blogs]

 
    if format == "json":
        data = json.dumps(blogs, ensure_ascii=False).encode("utf-8")

        if len(data) > MAX_SIZE:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
            tmp.write(data)
            tmp.close()

            if background_tasks:
                background_tasks.add_task(os.remove, tmp.name)

            return FileResponse(tmp.name, media_type="application/json", filename=f"user_{id}_blogs.json")

        return JSONResponse(content=blogs)


    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "title", "body"])
    writer.writeheader()
    writer.writerows(blogs)

    csv_bytes = output.getvalue().encode("utf-8")

    if len(csv_bytes) > MAX_SIZE:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        tmp.write(csv_bytes)
        tmp.close()

        if background_tasks:
            background_tasks.add_task(os.remove, tmp.name)

        return FileResponse(tmp.name, media_type="text/csv", filename=f"user_{id}_blogs.csv")

    headers = {"Content-Disposition": f'attachment; filename="user_{id}_blogs.csv"'}
    return StreamingResponse(iter([csv_bytes]), media_type="text/csv; charset=utf-8", headers=headers)