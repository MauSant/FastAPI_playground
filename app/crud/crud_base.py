#FastAPI
from fastapi.encoders import jsonable_encoder

#From 1th
from models.collection import Collection
from  models.py_object_id import PyObjectId

#From 3th
from pydantic import BaseModel, EmailStr
from pymongo.database import Database
from typing import TypeVar, Generic, Type, Union, Dict, Any, List

#models & schemas
from models.schemas import user_schema




ModelType = TypeVar("ModelType", bound=Collection)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CrudBase(Generic[ModelType,CreateSchemaType,UpdateSchemaType]):
    __slots__=('model',)
    
    def __init__(self, model:ModelType):
        self.model = model
    

    def get_by_id(self,db: Database, model_id: str) -> ModelType:
        id_object = PyObjectId(model_id)
        result = db[self.model.c_name()].find_one({"_id":id_object})
        return self.model(**result)


    # def get_all(self, db: Database):
    #     return db.query(self.model).all()


    # def get_count(self, db:Database)-> int:
    #     return db.query(self.model).count()


    # def get_multi(
    #     self, db: Database, *, skip: int = 0, page_size: int = 100
    # )-> List[ModelType]:
    #     return db.query(self.model).offset(skip).limit(page_size).all()

    
    # #TODO: For future implementation of Cursor Pagination 
    # def alt_get_multi(self, db:Database, page_size: int = 100, cursor: Union[int,str] = 1):
    #     signal, cursor = cursor.split("|")
    #     query = None

    #     if  "next" == signal:
    #         query = db.query(self.model) \
    #                     .filter(self.model.id > cursor) \
    #                     .order_by(self.model.id.asc()) \
    #                     .limit(page_size) \
    #                     .all()
    #     elif "prev" == signal:
    #         query = db.query(self.model) \
    #                     .filter(self.model.id < cursor) \
    #                     .order_by(self.model.id.desc()) \
    #                     .limit(page_size) \
    #                     .all()

    #     return query

    def create(self, db: Database, model_in: CreateSchemaType)-> ModelType:
        db_model: ModelType = self.model(**model_in.dict())
        db[self.model.c_name()].insert_one(db_model.change_id_key())
        return db_model


    # def update(
    #     self,
    #     db: Database,
    #     old_model: ModelType,
    #     new_model: Union[UpdateSchemaType, Dict[str,Any]]
    # ) ->ModelType:
    #     old_data = jsonable_encoder(old_model)
    #     if isinstance(new_model, dict):
    #         new_data = new_model
    #     else:
    #         new_data = new_model.dict(exclude_unset=True)
        
    #     for field, new_value in new_data.items():
    #         if field in old_data:
    #             setattr(old_model, field, new_value)
        
    #     db.add(old_model)
    #     db.commit()
    #     db.refresh(old_model)
    #     return old_model


    # def delete(self, id: int, db: Database)-> ModelType:
    #     db_model = self.get_by_id(db,model_id=id)
    #     db.delete(db_model)
    #     db.commit()
    #     return db_model

        

