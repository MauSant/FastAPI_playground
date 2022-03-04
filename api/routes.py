from fastapi import APIRouter
from api.endpoints import user, auth



api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["users"])


@api_router.get("/me", tags=["Main"])
async def root():
    return 'I live I die, I live Again'
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])