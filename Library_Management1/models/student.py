from .member import Member

class Student(Member):
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def max_borrow_limit(self):
        return 2
