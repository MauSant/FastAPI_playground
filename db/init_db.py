from fastapi import Depends

from db.database import AsyncDB, async_get_db, SessionLocal
from crud.async_crud.async_user_crud import async_user_crud
from models.schemas import user_schema
from core.config import get_settings

USER_NAME = get_settings().USER_NAME
USER_PASS = get_settings().USER_PASS
USER_EMAIL = get_settings().USER_EMAIL
USER_CPF = get_settings().USER_CPF
USER_IS_ADMIN = get_settings().USER_IS_ADMIN


async def init_db():
    db = SessionLocal()
    try:
        user = await async_user_crud.get_user_by_email(db, USER_EMAIL)
        if not user:
            first_user = user_schema.UserCreate(
                name=USER_NAME,
                cpf=USER_CPF,
                email=USER_EMAIL,
                password=USER_PASS,
                is_admin=USER_IS_ADMIN
            )
            user = await async_user_crud.create_user(db, new_user=first_user)
        return 0
    except Exception as e:
        raise e