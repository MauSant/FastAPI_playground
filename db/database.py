from fastapi import Depends
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
# import db.db_models.user_db_model 
from core.config import get_settings 

'''SYNC'''
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://mauricio:123@localhost:3306/fastapi_playground"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

'''ASYNC'''
SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://mauricio:123@localhost:3306/fastapi_playground"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)






async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def async_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
    
class AsyncDB(AsyncSession):
    """Lets you use the following dependency: db: AsyncDB = Depends()"""

    def __new__(cls, db: AsyncSession = Depends(async_get_db)) -> AsyncSession:
        return db

# Base = declarative_base()


