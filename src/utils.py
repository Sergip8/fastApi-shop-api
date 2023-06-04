from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(pass_hashed: str, pass_in):

    return pwd_context.verify(pass_in, pass_hashed)