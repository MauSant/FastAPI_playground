from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cpf = Column(Integer, index=True)
    email = Column(String,unique=True, index=True)
    password = Column(String)


def teste():
    print('staring dbuser')
