from fastapi import APIRouter
from api.endpoints import user,auth
from db.init_db import init_db, close_db


api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
# api_router.include_router(async_user.router, prefix="/users", tags=["users-async"])



@api_router.on_event("startup")
def startup_db_client():
    # api_router.mongo_client = get_mongo_client()
    # init_db(api_router.mongo_client)
    init_db()


@api_router.on_event("shutdown")
def shutdown_db_client():
    close_db()  


@api_router.get("/", tags=["Main"])
def root():
    return 'I live I die, I live Again'

# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])