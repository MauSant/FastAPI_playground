#FastAPI
from fastapi import APIRouter, Request
from fastapi.param_functions import Depends
from fastapi import Body, HTTPException, Query, Path
from utils.context_timer import Timer
#From 1th
from db.database import async_get_db, AsyncDB
from crud.async_crud.async_user_crud import async_user_crud  
from core.sec_depends import get_current_user, get_current_super_user
from utils.pagination import page_response, Pagination

#from 3th
from typing import List, Dict,Optional


#models & schemas
from models.schemas import user_schema
from models import user_db

router = APIRouter()


@router.get("/async/{user_id}", response_model=user_schema.UserOut)
async def async_read_user_by_id(
        user_id: int,
        db: AsyncDB = Depends(async_get_db),
        current_user = Depends(get_current_user)
    ):
    db_user = await async_user_crud.get_by_id(db,user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found")
    return db_user
    
    # with Timer() as timer:
    #     for _ in range(0,1000):
    #         result = await async_user_crud.get_by_id(db,user_id)

    # return f'It took {timer.t} seconds'


# @router.get(
    # "/async/all/",
    # response_model=page_response(model_out=user_schema.UserOut, name='t')
# )
@router.get(
    "/async/all/",
    response_model=user_schema.UserPageOut
)
async def async_read_users(
    page: int = Query(1),
    page_size: int = Query(10),
    db: AsyncDB = Depends(async_get_db),
    current_user = Depends(get_current_user)
):
    skip = (page-1) * page_size
    list_users = await async_user_crud.get_multi(db=db, skip=skip, page_size=page_size)
    users_count = await async_user_crud.get_count(db)
    page = Pagination(
                data=list_users,
                page_size=page_size,
                page=page,
                path_name='/users/async',
                total_count=users_count)
    
    return page.mk_dict()


@router.post(
        "/async/store",
        response_model=user_schema.UserOut
)
async def async_store_user(
    user: user_schema.UserCreate = Body(...),
    db: AsyncDB = Depends(async_get_db),
    current_user = Depends(get_current_user)
):
    user_in_db = await async_user_crud.get_user_by_email(db=db, email=user.email)
    if user_in_db:
        raise HTTPException(
            status_code=400,
            detail="User already registered")
    db_user = await async_user_crud.create_user(db=db, new_user=user)
    return db_user


@router.put(
    "/async/update/{user_id}",
    response_model=user_schema.UserOut
)
async def async_update_user(
    user_id: int = Path(...),
    user_in: user_schema.UserUpdate = Body(...),
    db: AsyncDB = Depends(async_get_db),
    current_user: user_db.User = Depends(get_current_super_user) 
    # current_user: user_db.User  = Depends(get_current_user)
):
    db_user = await async_user_crud.get_by_id(db=db, model_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Key not valid")
    if db_user.email == current_user.email:
        raise HTTPException(
            status_code=405,
            detail="Not allowed to modify logged user")
    db_user = await async_user_crud.update_user(db, db_user, user_in)
    return db_user


@router.delete(
    "async/delete/{user_id}",
    response_model=user_schema.UserOut
)
async def async_delete_user(
    user_id: int = Path(...),
    db: AsyncDB = Depends(async_get_db),
    current_user: user_db.User = Depends(get_current_user)
):
    db_user = await async_user_crud.get_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="user does not exist")
    if db_user.email == current_user.email:
         raise HTTPException(
            status_code=405,
            detail="Not allowed to delete logged user")
    return await async_user_crud.delete(user_id, db)

#TODO
# @app.post("/delete/{user_id}", response_model=user_schema.UserOut)
    # @app.post("/items") #Recebe um body
    # #use o embed sempre que puder para utilizar sempre o mesmo padrão
    # async def receive_item(item: Item = Body(..., embed = True)): #body - multipleparams Embed(docs)
    #     print(item.name)
    #     return item