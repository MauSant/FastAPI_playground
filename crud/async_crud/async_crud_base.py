#FastAPI
from fastapi.encoders import jsonable_encoder

#From 1th
from db.base_class import Base #sqlAlchemy model

#From 3th
from pydantic import BaseModel, EmailStr
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Generic, Type, Union, Dict, Any, List

#models & schemas
from models.schemas import user_schema




ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class AsyncCrudBase(Generic[ModelType,CreateSchemaType,UpdateSchemaType]):
    def __init__(self, model:ModelType):
        self.model = model


    async def get_by_id(self, db:AsyncSession, model_id:int):
        query = select(self.model).where(self.model.id == model_id)
        result = await db.execute(query)
        return result.scalars().first()


    async def get_all(self, db: AsyncSession):
        query = select(self.model)
        result = await db.execute(query) 
        return result.scalars().all()

    '''
    Needs test
    '''
    async def get_count(self, db:AsyncSession)-> int:
        query = select([func.count()]).select_from(self.model)
        result = await db.execute(query)
        return result.scalars().all()


    def get_multi(
        self, db: Session, *, skip: int = 0, page_size: int = 100
    )-> List[ModelType]:
        return db.query(self.model).offset(skip).limit(page_size).all()

    
    #TODO: For future implementation of Cursor Pagination 
    def alt_get_multi(self, db:Session, page_size: int = 100, cursor: Union[int,str] = 1):
        signal, cursor = cursor.split("|")
        query = None

        if  "next" == signal:
            query = db.query(self.model) \
                        .filter(self.model.id > cursor) \
                        .order_by(self.model.id.asc()) \
                        .limit(page_size) \
                        .all()
        elif "prev" == signal:
            query = db.query(self.model) \
                        .filter(self.model.id < cursor) \
                        .order_by(self.model.id.desc()) \
                        .limit(page_size) \
                        .all()

        return query

    def create(self, db: Session, model_in: CreateSchemaType)-> ModelType:
        db_model = self.model(**model_in.dict())
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model


    def update(
        self,
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


    def delete(self, id: int, db: Session)-> ModelType:
        db_model = self.get_by_id(db,model_id=id)
        db.delete(db_model)
        db.commit()
        return db_model

        

