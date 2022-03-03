from typing import TypeVar, Generic, Type, Union, Dict, Any, List
from numpy import isin
from sqlalchemy.orm import Session
from models.schemas import user_schema
from pydantic import BaseModel, EmailStr
from fastapi.encoders import jsonable_encoder
from db.base_class import Base #sqlAlchemy model

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CrudBase(Generic[ModelType,CreateSchemaType,UpdateSchemaType]):
    def __init__(self, model):
        self.model = model
    

    def get_by_id(self,db: Session, model_id: int):
        return db.query(self.model).filter(self.model.id == model_id).first()


    def get_all(self, db: Session):
        return db.query(self.model).all()


    def get_count(self, db:Session)-> int:
        return db.query(self.model).count()


    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    )-> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()


    def create(self, db: Session, model_in: CreateSchemaType)-> ModelType:
        db_model = self.model(**model_in.dict())
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model


    def update(self,
        db: Session,
        old_model: ModelType,
        new_model: Union[UpdateSchemaType, Dict[str,Any]]
    ) ->ModelType:
        old_data = jsonable_encoder(old_model)
        if isinstance(new_model, dict):
            new_data = new_model
        else:
            new_data = new_model.dict(exclude_unset=True)
        
        for field, new_value in new_data.items():
            if field in old_data:
                setattr(old_model, field, new_value)
        
        db.add(old_model)
        db.commit()
        db.refresh(old_model)
        return old_model

        

