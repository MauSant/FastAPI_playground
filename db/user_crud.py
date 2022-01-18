from sqlalchemy.orm import Session
from db.db_models.user_db_model import User as user_db_model #chamado de models
from models.schemas import user_schema #chamado de schema


def teste():
    print('crud testings..')

def get_user(db: Session, user_id: int):
    return db.query(user_db_model).filter(user_db_model.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(user_db_model).filter(user_db_model.email == email).first()

def get_users_by_name(db: Session, name: str):
    return db.query(user_db_model).filter(user_db_model.name == name).all()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user_db_model).offset(skip).limit(limit).all()

def create_user(db: Session,  user: user_schema.UserCreate):
    db_user = user_db_model(email=user.email, password = user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user