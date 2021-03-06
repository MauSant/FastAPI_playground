from fastapi import APIRouter
from api.endpoints import user, auth, async_user
from db.init_db import init_db


api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(async_user.router, prefix="/users", tags=["users-async"])
# api_router.include_router(user.router, prefix="/users", tags=["users"])

from db.database import AsyncDB, async_get_db
@api_router.on_event("startup") #Does not work with Depends! Maybe they will change later
async def initialize_db():
    zero = await init_db()
    
@api_router.get("/", tags=["Main"])
def root():
    return 'I live I die, I live Again'

# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])