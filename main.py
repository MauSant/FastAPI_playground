import uvicorn
from typing import List
from typing_extensions import Required
from fastapi import FastAPI, Body, HTTPException
from fastapi.param_functions import Depends

from sqlalchemy.orm import Session
from db.database import SessionLocal,engine

from crud.user_crud import user_crud as UserCrud
from models.item import Item
from models.schemas import user_schema




app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/me")
async def root():
    return {"message": "Hello World"}


@app.get("/user/{user_id}", response_model=user_schema.UserOut)
def show_user(user_id: int, db: Session = Depends(get_db)):
    db_user = UserCrud.get_by_id(db,user_id)
   
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found")
    return db_user

# @app.get("/user/search/{users_name}", response_model=List[user_schema.UserOut])
# def search_users_by_name(users_name: str, db: Session = Depends(get_db)):
#     db_users = UserCrud.get_users_by_name(db, users_name)
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

@app.post("/user/store", response_model=user_schema.UserOut)
def store_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = UserCrud.create(db=db, user=user)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="User already registered")
    return db_user
   
# @app.post("/delete/{user_id}", response_model=user_schema.UserOut)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)