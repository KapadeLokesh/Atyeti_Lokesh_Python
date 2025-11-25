from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base # type: ignore
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    creator = relationship("User", back_populates="blogs")
    comments = relationship("Comment", back_populates="blog", cascade="all, delete")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    blogs = relationship('Blog', back_populates="creator")

class Vote(Base):
    __tablename__ = "votes"
    userid = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    blogid = Column(Integer, ForeignKey("blogs.id", ondelete="CASCADE"), primary_key=True)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer,primary_key=True, index=True)
    content = Column(String,nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    blog_id = Column(Integer, ForeignKey("blogs.id", ondelete="CASCADE"), nullable=False)
    blog = relationship("Blog", back_populates="comments")
    user = relationship("User")