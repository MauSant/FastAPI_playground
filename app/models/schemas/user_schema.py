from pydantic import BaseModel
from utils.pagination import PageResponse
from typing import TypeVar, Generic, List, Optional, Dict


class UserBase(BaseModel):
    name: str
    cpf: str
    email: str

class UserCreate(UserBase):
    password: str
    is_admin: Optional[bool] = False

class UserUpdate(UserBase):
    password: Optional[str]
    is_admin: Optional[bool]

class UserOut(UserBase):
    pass

class User(UserBase):
    id: str
    password: str

    class Config: #Precisa disso para salvar no banco
        orm_mode = True

class UserInDB(User):
    hash_password: str
    is_admin: Optional[bool]



class UserPageOut(PageResponse):
    data: List[UserOut]
