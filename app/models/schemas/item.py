from typing import Optional
from pydantic import BaseModel, ValidationError, validator


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    #usado como as rules na model do laravel
    @validator('name')#validações mais complicadas
    def name_must_start_with_z(cls, value: str):
        print(f'dentro da validação nome={value}')

        if not value.startswith('z'):
            print('deu erro')
            raise ValueError('não tem z') 
        print('deu certo')
        return value.title()


class UserBase(BaseModel):
    name: str
    cpf: str
    email: str
    password: str

    

class Lojistas(UserBase):
    pass

class Clients(UserBase):
    pass