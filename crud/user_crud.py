from sqlalchemy.orm import Session
from models.user_db import User as user_db_model #chamado de models
from models.schemas import user_schema #chamado de schema
from crud.crud_base import CrudBase


class UserCrud(CrudBase[user_db_model,user_schema.UserCreate, user_schema.UserUpdate]):
    # def get_user(self,db: Session, user_id: int) -> user_db_model:
    #     return db.query(user_db_model).filter(user_db_model.id == user_id).first()

    def get_user_by_email(self,db: Session, email: str) -> user_db_model:
        return db.query(user_db_model).filter(user_db_model.email == email).first()

    def filter_user_by_name(self,db: Session, name: str) -> user_db_model:
        return db.query(user_db_model).filter(user_db_model.name == name).all()

    def get_users(self,db: Session, skip: int = 0, limit: int = 100) -> user_db_model:
        return db.query(user_db_model).offset(skip).limit(limit).all()

    # def create_user(self,db: Session,  user: user_schema.User) -> user_db_model:
    #     db_user = user_db_model(**user.dict())
    #     db.add(db_user)
    #     db.commit()
    #     db.refresh(db_user)
    #     return db_user

    # def delete_user(self,db: Session, user: user_schema.User) -> user_db_model:
    #     db_user = self.get_user_by_email(db,user.email)
    #     db.delete(db_user)
    #     db.commit()
    #     return db_user

user_crud = UserCrud(user_db_model)