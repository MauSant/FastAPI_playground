from typing import Union, Any, Dict

from jose import jwt, JWTError

from pydantic import ValidationError
from fastapi import HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer


from sqlalchemy.orm import Session
from db.database import get_db

from crud.user_crud import user_crud
from models.schemas import token_schema
from models.user_db import User as user_db_model #chamado de models
from core.sec_config import SECRET_KEY, ALGORITHM, CREDENTIALS_EXCEPTION

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/access_token")


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
)-> user_db_model:
    
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CREDENTIALS_EXCEPTION
        token_data = token_schema.TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise CREDENTIALS_EXCEPTION
    else:
        db_user = user_crud.get_by_id(db,token_data.sub)
        if not db_user:
         raise HTTPException(status_code=404, detail="User not found")
    return db_user