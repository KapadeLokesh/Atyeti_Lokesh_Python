from .member import Member

class Teacher(Member):
    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }

    def max_borrow_limit(self):
        return 5
