# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import get_settings
from models.schemas import user_schema

IS_ASYNC = get_settings().IS_ASYNC



if IS_ASYNC is True:
    '''ASYNC'''
    from fastapi import Depends
    from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
    SQLALCHEMY_DATABASE_URL = get_settings().DB_URL
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
else:
    '''SYNC'''
    from sqlalchemy import create_engine
    SQLALCHEMY_DATABASE_URL = get_settings().DB_URL
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



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


