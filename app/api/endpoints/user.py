#FastAPI
from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi import Body, HTTPException, Query, Path
#From 1th
from crud.user_crud import user_crud
from db.database import get_db
from core.sec_depends import get_current_user, get_current_super_user
from utils.pagination import page_response, Pagination

#from 3th
from typing import List, Dict, Optional
from pymongo.database import Database

#models & schemas
from models.schemas import user_schema
from models import user_db
from models.py_object_id import PyObjectId


router = APIRouter()


@router.get("/{user_id}",
 response_model=user_schema.UserOut
)
def read_user_by_id(
    user_id: PyObjectId,
    db: Database = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    db_user = user_crud.get_by_id(db,user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found")
    return db_user


# @router.get("/", response_model=user_schema.UserPageOut)
# def read_users(
#     db: Session = Depends(get_db),
#     page: int = Query(1),
#     page_size: int = Query(10),
#     current_user = Depends(get_current_user)
# )-> Dict:
#     skip = (page-1) * page_size
#     list_users = user_crud.get_multi(db=db, skip=skip, page_size=page_size)
#     users_count = user_crud.get_count(db)
#     page = Pagination(
#                     data=list_users,
#                     page_size=page_size,
#                     page=page,
#                     path_name='/users',
#                     total_count=users_count)
    
#     return page.mk_dict()


@router.post("/store", response_model=user_schema.UserOut)
def store_user(
    user: user_schema.UserCreate,
    db: Database = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    user_in_db = user_crud.get_user_by_email(db=db,email=user.email)
    if user_in_db:
        raise HTTPException(
            status_code=400,
            detail="User already registered")
    db_user = user_crud.create_user(db=db, new_user=user)
    return db_user

# @router.put("/update/{user_id}", response_model= user_schema.UserOut)
# def update_user(
#     user_in: user_schema.UserUpdate,
#     user_id: int,
#     db: Session = Depends(get_db),
#     current_user = Depends(get_current_user)
# ):
#     db_user = user_crud.get_by_id(db=db, model_id=user_id)
#     if not db_user:
#         raise HTTPException(
#             status_code=400,
#             detail="Key not valid")
#     db_user = user_crud.update_user(db, db_user, user_in)
#     return db_user

# @router.delete("/delete/{user_id}", response_model=user_schema.UserOut)
# def delete_user(
#     user_id: int,
#     db: Session = Depends(get_db),
#     current_user = Depends(get_current_user)
# ):
#     db_user = user_crud.get_by_id(db, user_id)
#     if not db_user:
#         raise HTTPException(
#             status_code=400,
#             detail="user does not exist")
#     if db_user.email == current_user.email:
#          raise HTTPException(
#             status_code=405,
#             detail="Not allowed to delete logged user")
#     return user_crud.delete(user_id, db)



#TODO
# @app.post("/delete/{user_id}", response_model=user_schema.UserOut)
    # @app.post("/items") #Recebe um body
    # #use o embed sempre que puder para utilizar sempre o mesmo padrão
    # async def receive_item(item: Item = Body(..., embed = True)): #body - multipleparams Embed(docs)
    #     print(item.name)
    #     return item