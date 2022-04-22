
from fastapi import HTTPException, status
from core.config import get_settings

CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
SECRET_KEY = get_settings().SECRET_KEY
ALGORITHM = get_settings().ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
