from ast import Str
from optparse import Option
from typing import Any, Dict, List, Optional, Union
from functools import cache, lru_cache
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    IS_ASYNC: bool = True
    DB_DRIVER: Optional[str]
    DB_USER: str
    DB_PASSWORD: str
    DB_CONNECTION: str #127.0.0.1 or localhost
    DB_HOST: str
    DB_PORT: str #3310
    DB_TABLE_NAME: str 
    DB_URL: Optional[str] = None


    @validator('DB_DRIVER')
    def driver_none(cls, v: Optional[str]):
        if v is None:
            driver = '' 
        elif isinstance(v, str):
            driver = '+' + v

        return driver

    @validator('DB_URL')
    def db_url_construct(cls, v: Optional[str], values: dict):
        if isinstance(v,str):
            return v #in case is already done
        conn = values.get('DB_CONNECTION')
        driver = values.get('DB_DRIVER')
        user = values.get('DB_USER')
        password = values.get('DB_PASSWORD')
        host = values.get('DB_HOST')
        port = values.get('DB_PORT')
        table_name = values.get('DB_TABLE_NAME')

        db_url = conn+driver+'://'+user+password+'@'+host+':'+port+'/'+table_name
        return db_url

        


    #Security settings
    CORS_ORIGIN: Optional[Union[list,bool]]
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


    # First user
    USER_NAME: str
    USER_PASS: str
    USER_EMAIL: str
    USER_CPF: str
    USER_IS_ADMIN: bool

    # class config:
    #     env_file = '.env'
    #     env_file_encoding = 'utf-8'

@lru_cache(maxsize=1)
def get_settings():
    return Settings(env_file='.env', env_file_encoding='utf- 8')