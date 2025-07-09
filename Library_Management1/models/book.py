from datetime import timedelta
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    is_issued = Column(Boolean, default=False)
    issued_to_id = Column(Integer, ForeignKey('members.id'), nullable=True)
    due_date = Column(DateTime, nullable=True)

    issued_to = relationship("Member", back_populates="books_issued")

    def __str__(self):
        return f"{self.title} by {self.author}"

