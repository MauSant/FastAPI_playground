from pydantic import BaseModel
from typing import TypeVar, Generic, List, Optional, Dict
from models.schemas.mongo.chapter import Chapter


class Arc(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]
    first_cap: Optional[int]
    last_cap: Optional[int]
    qt_cap: Optional[int]
    chapters: Optional[list[Chapter]]

