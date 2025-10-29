from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

class Hash:
    @staticmethod
    def argon2(password: str):
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str):
        return pwd_cxt.verify(plain_password, hashed_password)
