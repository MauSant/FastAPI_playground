from pydantic import BaseModel
from utils.pagination import PageResponse
from typing import TypeVar, Generic, List, Optional, Dict


class UserBase(BaseModel):
    name: str
    cpf: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str]

class UserOut(UserBase):
    class Config:#Precisa disso para transformar da classe User do db em UserOut!
        orm_mode = True

class User(UserBase):
    id: int
    password: str

    class Config: #Precisa disso para salvar no banco
        orm_mode = True

class UserInDB(User):
    hash_password: str

# class UserPageOut(Page):
#     data: List[Optional[UserOut]]
