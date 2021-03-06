
#FastAPI
from fastapi import APIRouter, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.param_functions import Depends
from fastapi import Body, HTTPException, Query


#From 1th
from db.database import get_db, async_get_db, AsyncDB
from crud.user_crud import user_crud
from crud.async_crud.async_user_crud import async_user_crud
from core.sec_config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.security import create_access_token
from core.sec_depends import get_current_user


#from 3th
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List, Dict


#models & schemas
from models.schemas import token_schema

#Cruds



router = APIRouter()

'''
REMEMBER:
For front-end to use this login, it must make a request with forma-data
and this form-data must contain a field username and password
'''
@router.post("/login/access_token", response_model=token_schema.Token)
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
)-> dict:
    db_user = user_crud.authenticate_user(
                db=db,
                username=form_data.username, # username = email
                plain_password=form_data.password)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
            subject=db_user.id,
            expires_delta=access_token_expires
        )
    return {"access_token": access_token,"token_type": "bearer",}


@router.post("/async/login/access_token", response_model=token_schema.Token)
async def async_login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(async_get_db)
)-> dict:
    db_user = await async_user_crud.authenticate_user(
                db=db,
                username=form_data.username, # username = email
                plain_password=form_data.password)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
            subject=db_user.id,
            expires_delta=access_token_expires
        )
    return {"access_token": access_token,"token_type": "bearer",}









#TODO: Could Not do it! Must find a way
# @router.post("/login/destroy-token")
# async def logout(
#     request: Request,
#     response: Response,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user)
# ):
#     response.delete_cookie("access_token")
#     return response