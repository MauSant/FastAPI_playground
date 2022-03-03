import uvicorn
from datetime import timedelta
from typing import List, Dict
from typing_extensions import Required

from fastapi.param_functions import Depends
from fastapi import FastAPI, Body, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm


from sqlalchemy.orm import Session

from db.database import get_db

from core.sec_depends import get_current_user
from core.sec_config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.security import create_access_token

from crud.user_crud import user_crud as user_crud
from models.item import Item
from models.schemas import user_schema, token_schema

from utils.pagination import Pagination, page_response


app = FastAPI()

#must be on a login/security path operations package [tag = login ]
@app.post("/login/access_token", response_model=token_schema.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
)-> None:
    db_user = user_crud.authenticate_user(
                db=db,
                username=form_data.username, # username = email
                plain_password=form_data.password)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
            subject=db_user.id,
            expires_delta=access_token_expires
        )
    return {"access_token": access_token,"token_type": "bearer",}


@app.get("/me", response_model=user_schema.UserOut)
async def root(current_user: user_schema.User = Depends(get_current_user)):
    return current_user


@app.get("/user/{user_id}", response_model=user_schema.UserOut)
def read_user_by_id(
    user_id: int, db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_user = user_crud.get_by_id(db,user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found")
    return db_user


# @app.get("/users", response_model=user_schema.UserPageOut)
@app.get(
    "/users",
    response_model=page_response(model_out=user_schema.UserOut)
)
def read_users(
    db: Session = Depends(get_db),
    page: int = Query(1),
    page_size: int = Query(10)
)-> Dict:
    skip = (page-1) * page_size #0
    limit = skip + page_size # 2
    list_users = user_crud.get_multi(db=db, skip=skip, limit=limit)
    page = Pagination(
                    data=list_users,
                    page_size=page_size,
                    page=page,
                    path_name='/users')
    
    return page.mk_dict()


@app.post("/user/store", response_model=user_schema.UserOut)
def store_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    user_in_db = user_crud.get_by_email(db=db,email=user.email)
    if user_in_db:
        raise HTTPException(
            status_code=400,
            detail="User already registered")
    
    db_user = user_crud.create(db=db, model_in=user)
    return db_user
   

@app.post("/user/update/{user_id}", response_model= user_schema.UserOut)
def update_user(
    user_in: user_schema.UserUpdate,
    user_id: int,
    db: Session = Depends(get_db)
):
    db_user = user_crud.get_by_id(db=db, model_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Key not valid")
    db_user = user_crud.update_user(db, db_user, user_in)
    return db_user



# @app.post("/delete/{user_id}", response_model=user_schema.UserOut)

if 1==2:
    # @app.get("/user/search/{users_name}", response_model=List[user_schema.UserOut])
    # def search_users_by_name(users_name: str, db: Session = Depends(get_db)):
    #     db_users = user_crud.get_users_by_name(db, users_name)
    #     if db_users is None:
    #         raise HTTPException(
    #             status_code=404,
    #             detail=f"None User with {users_name} found")
    #     return db_users
    # @app.get("/{item_id}") #path parameters
    # async def root(item_id: int):
    #     return {"message": item_id}

    # @app.post("/items") #Recebe um body
    # #use o embed sempre que puder para utilizar sempre o mesmo padrão
    # async def receive_item(item: Item = Body(..., embed = True)): #body - multipleparams Embed(docs)
    #     print(item.name)
    #     return item
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)