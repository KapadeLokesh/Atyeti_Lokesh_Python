from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    member_type = Column(String(50))  # 'student' or 'teacher'

    __mapper_args__ = {
        'polymorphic_identity': 'member',
        'polymorphic_on': member_type
    }

    books_issued = relationship("Book", back_populates="issued_to")

    def max_borrow_limit(self):
        return 3

    def borrow_book(self, book):
        from datetime import datetime, timedelta

        if len(self.books_issued) >= self.max_borrow_limit():
            print(f"{self.name} has reached max limit of books.")
            return False
        if book.is_issued:
            print(f"Sorry, '{book.title}' is already issued.")
            return False

        book.is_issued = True
        book.issued_to = self
        book.due_date = datetime.now() + timedelta(days=14)
        print(f"{self.name} borrowed '{book.title}'. Due on {book.due_date.date()}")
        return True

    def return_book(self, book, fine_per_day=5):
        from datetime import datetime

        if book.issued_to_id != self.id:
            print(f"{self.name} did not borrow '{book.title}'.")
            return

        now = datetime.now()
        overdue_days = (now - book.due_date).days
        fine = fine_per_day * max(0, overdue_days)

        book.is_issued = False
        book.issued_to = None
        book.due_date = None

        print(f"{self.name} returned '{book.title}'.", end=' ')
        if fine > 0:
            print(f"Overdue by {overdue_days} day(s). Fine: ₹{fine}")
        else:
            print("No fine. Thank you!")

    def __str__(self):
        issued = [f"{b.title}(due {b.due_date.date()})" for b in self.books_issued]
        return f"Member[{self.id}]: {self.name} | Issued: {issued}"
