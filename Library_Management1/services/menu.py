from services.library import Library
from models.teacher import Teacher
from models.student import Student
from sqlalchemy.exc import SQLAlchemyError

db_url = "mysql+pymysql://root:loki@localhost/librarydb"
lib = Library(db_url)

def show_menu():
    print("\n Library Management System")
    print("________________________________")
    print("1.Add Book")
    print("2.Add Member")
    print("3.Borrow Book")
    print("4.Return Book")
    print("5.Show All Books")
    print("6.Show All Members")
    print("0.Exit")

def add_book():
    title = input("Enter book title:").strip()
    author = input("Enter author name:").strip()
    if not title and not author:
        print("Title and Author cannot be empty.")
    try:
        lib.add_book(title,author)
    except SQLAlchemyError as e:
        print("Error adding book:",e)

def add_member():
    name = input("Enter member name:").strip()
    mtype = input("Enter member type(student/teacher):").strip().lower()

    if not name or mtype not in['student','teacher']:
        print("Invalid inputs for name and mtype.")
        return
    try:
        if mtype == 'student':
            member = Student(name=name,member_type = 'student')
        else:
            member = Teacher(name=name, member_type='teacher')
        lib.add_member(member)
    except SQLAlchemyError as e:
        print("Error adding a member: ",e)

def borrow_book():
    try:
        member_id = int(input("Enter member ID: "))
        book_id = int(input("Enter book ID: "))
        lib.borrow_book(member_id, book_id)
    except ValueError:
        print("Please enter valid numeric IDs.")
    except SQLAlchemyError as e:
        print("Error borrowing book:", e)

def return_book():
    try:
        member_id = int(input("Enter member ID:"))
        book_id = int(input("Enter book ID:"))
        lib.return_book(member_id, book_id)
    except ValueError:
        print("Please enter integer IDs.")
    except SQLAlchemyError as e:
        print("Error returning book:",e)

def show_books():
    try:
        lib.show_books()
    except SQLAlchemyError as e:
        print("Error fetching books:", e)

def show_members():
    try:
        lib.show_members()
    except SQLAlchemyError as e:
        print("Error fetching members:", e)



