
from core.config import get_settings
from pymongo import MongoClient
from functools import lru_cache


@lru_cache(maxsize=1)
def get_db(mongo_client: MongoClient):
    # db = mongo_client["mongoPlay"]
    db = mongo_client[get_settings().DB_TABLE_NAME]
    return db

def get_mongo_client(v:bool=True) -> MongoClient:
    client = MongoClient(get_settings().DB_URL)
    return client


if __name__ == "__main__":
    client = get_mongo_client()
    get_db(client)
    a = get_db(client)
    a = get_db(client)
    a = get_db(client)



# async def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# async def async_get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         await db.close()
    
# class AsyncDB(AsyncSession):
#     """Lets you use the following dependency: db: AsyncDB = Depends()"""

#     def __new__(cls, db: AsyncSession = Depends(async_get_db)) -> AsyncSession:
#         return db





