from sqlalchemy.orm import Session
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer

from crud.user_crud import user_crud
from models.schemas import user_schema
from models.user_db import User as user_db_model #chamado de models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/access_token")


def fake_decode_token(token):
    return user_schema.User(
        name='jamal', email="john@example.com", cpf="06722", password='123'
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user

def authenticate_user(db: Session, username: str, plain_pasword: str)-> user_db_model:
    db_user = user_crud.get_user_by_email(db, email=username)
    if not db_user:
        return None
    if not verify_password(db_user.password, plain_pasword):
        return None
    return db_user


def verify_password(hashed_password: str, plain_pasword: str )-> bool:
    return True