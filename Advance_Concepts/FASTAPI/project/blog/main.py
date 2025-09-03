from typing import List
from fastapi import Depends, FastAPI, HTTPException, status, Response
from . import schemas,models, hashing
from .database import engine,SessionLocal,get_db
from .schemas import Blog
from sqlalchemy.orm import Session
from .hashing import Hash
from routers import authentication, blog,user

models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
 
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.post('/blog', status_code = status.HTTP_201_CREATED,tags=['BLOGS:'])
# def create(request:schemas.Blog, db: Session= Depends(get_db)):
#     new_blog = models.Blog(title=request.title, body=request.body, user_id = 1)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog

# @app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['BLOGS:'])
# def delete_blog(id, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id)
#     if not blog.first():
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Blog with id {id} is not found."
#         )
#     blog.delete(synchronize_session=False)
#     db.commit()
#     return {"Done."}

# @app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED,tags=['BLOGS:'])
# def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id)
    
#     if not blog.first():
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Blog with id {id} is not found."
#         )
    
#     blog.update(request.model_dump())  # type: ignore
#     db.commit()
    
#     return {"message": "Updated"}

# # @app.get('/blog',response_model=List[schemas.ShowBlog],tags=['BLOGS:'])
# # def all_blog(db: Session = Depends(get_db)):
# #     blogs = db.query(models.Blog).all()
# #     return blogs

# @app.get('/blog/{id}',status_code=200,response_model=schemas.ShowBlog,tags=['BLOGS:'])
# def blog_By_Id(id,response =Response, db:Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#     if not blog:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail = f"Blog with id {id} is not avaliable.")
#         # response.status_code =status.HTTP_404_NOT_FOUND
#         # return {'detail': f"Blog with id {id} is not avaliable."}
#     return blog


# @app.post('/user',response_model=schemas.ShowUser,tags=['USERS:'])
# def create_user(request: schemas.User, db:Session = Depends(get_db)):
    
#     new_user = models.User(name = request.name,email = request.email,password = Hash.bcrypt(request.password) )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# # @app.get('/user')
# # def all_user(db: Session = Depends(get_db)):
# #     users = db.query(models.User).all()
# #     return users

# @app.get('/user/{id}',status_code=200,response_model=schemas.ShowUser,tags=['USERS:'])
# def user_By_Id(id,response =Response, db:Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail = f"Blog with id {id} is not avaliable.")
#         # response.status_code =status.HTTP_404_NOT_FOUND
#         # return {'detail': f"Blog with id {id} is not avaliable."}
#     return user