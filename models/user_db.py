from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.base_class import Base

class User(Base):
    # __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    cpf = Column(String(16))
    email = Column(String(30),unique=True)
    hash_password = Column(String(100), nullable=False)
