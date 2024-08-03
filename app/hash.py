from passlib.context import CryptContext
from typing_extensions import deprecated

pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")
#fixed_salt = "1234567890123456789012"
def hash(password:str):
    return pwd_context.hash(password)

def password_verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
