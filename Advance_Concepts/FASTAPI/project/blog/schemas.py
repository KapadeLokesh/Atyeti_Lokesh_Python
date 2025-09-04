from typing import List, Optional
from pydantic import BaseModel

class BlogBase(BaseModel):
    title:str
    body: str
class Blog(BlogBase):
    

    class Config():
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str

# class ShowUser(BaseModel):
#     name: str
#     email: str
#     blogs: List[Blog] = []
#     class Config():
#         orm_mode = True


# class ShowBlog(BaseModel):
#     title:str
#     body:str
#     id: int
#     class Config():
#         orm_mode = True

# class Login(BaseModel):
#     username: str
#     password: str


# class TokenData(BaseModel):
#     username: Optional[str] = None

class BlogCreate(BlogBase):
    pass

class BlogOut(BlogBase):
    id: int
    class Config:
        orm_mode = True

class ShowBlog(BlogOut):
    pass

class ShowUser(BaseModel):
    name: str
    email: str
    

    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

# class TokenData(BaseModel):
#     email: Optional[str] = None

class TokenData(BaseModel):
    username: Optional[str] = None