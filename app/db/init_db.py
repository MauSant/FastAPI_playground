from fastapi import Depends

from db.database import get_db
from crud.async_crud.async_user_crud import async_user_crud
from models.schemas import user_schema
from core.config import get_settings
from pymongo import MongoClient

USER_NAME = get_settings().USER_NAME
USER_PASS = get_settings().USER_PASS
USER_EMAIL = get_settings().USER_EMAIL
USER_CPF = get_settings().USER_CPF
USER_IS_ADMIN = get_settings().USER_IS_ADMIN

def init_db(mongo_client: MongoClient) -> None:
    db =  get_db(mongo_client)
    pass
    #TODO: We must make a get call to see if the user exists,
    #TODO: in case there is no user, we must create 1

    
# async def init_db():
#     db = SessionLocal()
#     try:
#         user = await async_user_crud.get_user_by_email(db, USER_EMAIL)
#         if not user:
#             first_user = user_schema.UserCreate(
#                 name=USER_NAME,
#                 cpf=USER_CPF,
#                 email=USER_EMAIL,
#                 password=USER_PASS,
#                 is_admin=USER_IS_ADMIN
#             )
#             user = await async_user_crud.create_user(db, new_user=first_user)
#         return await db.close()
#     except Exception as e:
#         raise e