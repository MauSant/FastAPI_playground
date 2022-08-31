from pydantic import BaseModel, Field
from typing import TypeVar, Generic, List, Optional, Dict
from models.schemas.chapter_schema import Chapter
from models.py_object_id import PyObjectId

class Arc(BaseModel):
    id: PyObjectId
    name: Optional[str]
    description: Optional[str]
    first_cap: Optional[int]
    last_cap: Optional[int]
    qt_cap: Optional[int]
    chapters: Optional[list[Chapter]]

