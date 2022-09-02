from typing import Optional, Union

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[str]= None #Need to be a string because the Users.id is a string!
    # sub: Optional[int] = None

