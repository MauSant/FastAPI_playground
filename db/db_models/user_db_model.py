from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.base_class import Base

class User(Base):
    # __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    cpf = Column(String(16))
    email = Column(String,unique=True )
    password = Column(String)
