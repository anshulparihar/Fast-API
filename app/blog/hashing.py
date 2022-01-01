from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    def bcrypt(password):
        hashedPassword = pwd_context.hash(password)
        return hashedPassword

    def verify(plain_password,hashed_password):
        return pwd_context.verify(plain_password,hashed_password)
