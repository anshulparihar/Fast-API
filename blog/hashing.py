from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    def bcrypt(password):
        hashedPassword = pwd_context.hash(password)
        return hashedPassword
