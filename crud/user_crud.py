from os import name
from tokenize import Name
from sqlalchemy.orm import Session
from typing import Dict, Union, Any

from models.user_db import User as user_db_model #chamado de models
from models.schemas import user_schema #chamado de schema
from crud.crud_base import CrudBase

from core.security import get_password_hash, verify_password


class UserCrud(CrudBase[user_db_model,user_schema.UserCreate, user_schema.UserUpdate]):
    # def get_user(self,db: Session, user_id: int) -> user_db_model:
    #     return db.query(user_db_model).filter(user_db_model.id == user_id).first()

    def get_user_by_email(self,db: Session, email: str) -> user_db_model:
        return db.query(user_db_model).filter(user_db_model.email == email).first()

    def filter_user_by_name(self,db: Session, name: str) -> user_db_model:
        return db.query(user_db_model).filter(user_db_model.name == name).all()

    def get_users(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> user_db_model:
        return db.query(user_db_model).offset(skip).limit(limit).all()

    def create_user(
        self,
        db: Session,
        new_user: user_schema.UserCreate
    ) -> user_db_model:
        hash_password = get_password_hash(new_user.password)
        db_model = user_db_model(
            name=new_user.name,
            cpf=new_user.cpf,
            email=new_user.email,
            hash_password=hash_password
        )
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model

    def update_user(
        self,
        db:Session,
        old_user:user_db_model,
        new_user: Union[user_schema.UserUpdate, Dict[str, Any]]
    )-> None:
        if isinstance(new_user, dict):
            new_data = new_user
        else:
            new_data = new_user.dict(exclude_unset=True)
        if new_data['password']:
            hash_password = get_password_hash(new_data['password'])
            del new_data["password"]
            new_data["hash_password"] = hash_password
        return super().update(db, old_user, new_model=new_data)



    def authenticate_user(
        self,
        db: Session,
        username: str,
        plain_password: str
    )-> user_db_model:
        db_user = self.get_user_by_email(db, email=username)
        if not db_user:
            return None
        if not verify_password(db_user.hash_password, plain_password):
            return None
        return db_user


    # def delete_user(self,db: Session, user: user_schema.User) -> user_db_model:
    #     db_user = self.get_user_by_email(db,user.email)
    #     db.delete(db_user)
    #     db.commit()
    #     return db_user

user_crud = UserCrud(user_db_model)