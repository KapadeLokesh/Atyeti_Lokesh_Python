from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.book import Book
from models.member import Member

class Library:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def add_book(self, title, author):
        book = Book(title=title, author=author)
        self.session.add(book)
        self.session.commit()
        # print(f"Added book: {book}")

    def add_member(self, member_obj):
        self.session.add(member_obj)
        self.session.commit()
        # print(f"Added member: {member_obj}")

    def borrow_book(self, member_id, book_id):
        member = self.session.query(Member).get(member_id)
        book = self.session.query(Book).get(book_id)
        if not member or not book:
            # print("Member or Book not found.")
            # return
            raise Exception("Member or Book not found.")
        if member.borrow_book(book):
            self.session.commit()

    def return_book(self, member_id, book_id):
        member = self.session.query(Member).get(member_id)
        book = self.session.query(Book).get(book_id)
        if not member or not book:
            raise Exception("Invalid member or book ID.")
        member.return_book(book)
        self.session.commit()
        # session = self.Session()
        # try:
        #     member = session.query(Member).filter_by(id=member_id).first()
        #     book = session.query(Book).filter_by(id=book_id).first()

        #     if not member or not book:
        #         print("Invalid member or book ID.")
        #         return

        #     if book.issued_to_id != member.id: # pyright: ignore[reportGeneralTypeIssues]
        #         print(f"{member.name} did not borrow '{book.title}'.")
        #         return

        #     member.return_book(book)
        #     session.commit()
        #     print("Return successful and saved to DB.")
        # except Exception as e:
        #     session.rollback()
        #     print("Database error while returning book:", e)
        # finally:
        #     session.close()

    def show_books(self):
        session = self.Session()
        try:
            books = session.query(Book).all()
            if not books:
                print("No books in Library.")
                return
            for book in books:
                status = f"Issued to Member ID {book.issued_to_id} (Due {book.due_date.date()})" \
                if book.is_issued else "Available" # pyright: ignore[reportGeneralTypeIssues]
                print(f"[{book.id}] {book.title} by {book.author} - {status}")
        finally:
            session.close()

    def show_members(self):
        session = self.Session()
        try:
            members = session.query(Member).all()
            if not members:
                print("No members in system.")
                return
            for member in members:
                issued_titles = [b.title for b in member.books_issued]
                print(f"[{member.id}] {member.name} \
                      ({member.member_type}) - Books issued: {issued_titles}")
        finally:
            session.close()

    def get_books(self):
        return self.session.query(Book).all()


    def get_members(self):
        return self.session.query(Member).all()