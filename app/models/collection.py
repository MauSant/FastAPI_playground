from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
class Collection(BaseModel):
    @classmethod
    def c_name(cls):
        return cls.__name__.lower()

    def json_encode(self):
        return jsonable_encoder(self)
