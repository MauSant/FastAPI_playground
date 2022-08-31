from pydantic import BaseModel, AnyHttpUrl
from typing import TypeVar, Generic, List, Optional, Dict
from utils.enums import LanguageEnum
from models.schemas.mongo.chapter import Chapter


class Chapter(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]
    language: Optional[LanguageEnum] = LanguageEnum.br 
    qt_page: Optional[int] = 0
    link_pages: Optional[list[AnyHttpUrl]]

