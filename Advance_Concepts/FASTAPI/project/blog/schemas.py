from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, conint

class BlogBase(BaseModel):
    title:str
    body: str
class BlogCreate(BlogBase):
    pass

class User(BaseModel):
    name: str
    email: str
    password: str

class BlogOut(BlogBase):
    id: int
    class Config:
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    body: str
    id: int
    votes: Optional[int] = 0

    class Config:
        from_attributes = True

# class ShowBlog(BlogOut):
#     pass

class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[ShowBlog] = []
    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str
class TokenData(BaseModel):
    email: Optional[str] = None

class Vote(BaseModel):
    blog_id : int
    dir: conint(le=1) # type: ignore

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    blog_id: int
    user_id: int
    created_at: datetime
    class Config:
        orm_mode= True
        