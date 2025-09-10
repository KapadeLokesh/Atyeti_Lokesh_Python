from typing import List, Optional
from pydantic import BaseModel

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

class ShowBlog(BlogOut):
    pass

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
