from typing import TypeVar, Generic, Type
from sqlalchemy.orm import Session
from models.schemas import user_schema
from pydantic import BaseModel, EmailStr

from db.base_class import Base #sqlAlchemy model

ModelType = TypeVar("ModelType", bound=Base)

class CrudBase(Generic[ModelType]):
    def __init__(self, model):
        self.model = model
    
    def get_by_id(self,db: Session, model_id: int):
        return db.query(self.model).filter(self.model.id == model_id).first()

    def get_by_email(self,db: Session, email: EmailStr):
        return db.query(self.model).filter(self.model.id == email).first()

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, user: user_schema.UserCreate):
        db_model = self.model(**user.dict())
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model

    # def update(self, db: Session, user: user_schema.User, ):
    #     pass


