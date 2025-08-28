from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
from services.library import Library
from models.student import Student
from models.teacher import Teacher
from sqlalchemy.exc import SQLAlchemyError

db_url = "mysql+pymysql://root:loki@localhost/librarydb"
lib = Library(db_url)

app = FastAPI(title="Library Management System")
# Pydantic Schemas

class BookSchema(BaseModel):
    title: str
    author: str

class MemberSchema(BaseModel):
    name: str
    member_type: str #"student" or "teacher"

class BorrowRequest(BaseModel):
    member_id: int
    book_id: int

class ReturnRequest(BaseModel):
    member_id: int
    book_id: int

# API Endpoints:

@app.get("/")
def root():
    return{"message":"Library API is running...!"}

@app.post("/books")
def add_books(book:BookSchema):
    try:
        lib.add_book(book.title,book.author)
        return {"message":"Book added successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/members")
def add_member(member:MemberSchema):
    try:
        if member.member_type.lower()=="student":
            m = Student(name=member.name,member_type="student")
        elif member.member_type.lower()=="teacher":
            m = Teacher(name=member.name,member_type="teacher")
        else:
            raise HTTPException(status_code=400,detail="Invalid member type.")
        lib.add_member(m)
        return {"message": "Member added successfully"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/borrow")
def borrow_book(req:BorrowRequest):
    try:
        lib.borrow_book(req.member_id,req.book_id)
        return{"message":"Book borrowed."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/return")
def return_book(req:ReturnRequest):
    try:
        lib.return_book(req.member_id,req.book_id)
        return {"message":"Book returned."}
    except Exception as e:
        raise HTTPException (status_code=400,detail=str(e))

@app.get("/books")
def get_books():
    books = lib.get_books()
    return[
        {"id":book.id,
         "title":book.title,
         "author":book.author,
         "is_issued":book.is_issued,
         "issued_to_id": book.issued_to_id,
         "due_date": book.due_date
         }for  book in books
    ]

@app.get("/members")
def get_members():
    members = lib.get_members()
    return [
        {
            "id": member.id,
            "name": member.name,
            "member_type": member.member_type,
            "books_issued": [book.title for book in member.books_issued]
        } for member in members
    ]
