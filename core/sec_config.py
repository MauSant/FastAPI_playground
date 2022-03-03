
from fastapi import HTTPException, status

CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
SECRET_KEY = 'c28b74ebb062f3f752e57fccdf8929d49a3788a1a12dc5838a93f97b306188e0'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
