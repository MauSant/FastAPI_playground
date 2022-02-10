from typing_extensions import ParamSpecKwargs
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    cpf: str
    email: str

class UserCreate(UserBase):
    password: str

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    class Config:#Precisa disso para transformar da classe User do db em UserOut!
        orm_mode = True

class User(UserBase):
    password: str

    class Config: #Precisa disso para salvar no banco
        orm_mode = True

