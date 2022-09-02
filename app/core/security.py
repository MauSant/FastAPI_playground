from typing import Union, Any, Dict
from datetime import datetime, timedelta


from jose import jwt, JWTError
from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer

from core.sec_config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from models.py_object_id import PyObjectId
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/access_token")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/access_token")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def create_access_token(
    subject: PyObjectId,
    expires_delta: timedelta = None,
):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_password(hash_password: str, plain_password: str )-> bool:
    return pwd_context.verify(secret=plain_password,hash=hash_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)