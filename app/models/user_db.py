from models.py_object_id import PyObjectId
from bson import ObjectId
from pydantic import Field
from models.collection import Collection
from typing import Optional

class Users(Collection):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    cpf: str
    hash_password: str
    email: str
    is_admin: Optional[bool]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
      