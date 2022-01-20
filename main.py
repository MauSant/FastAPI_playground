import uvicorn
from typing_extensions import Required
from fastapi import FastAPI, Body, HTTPException
from fastapi.param_functions import Depends

from db import user_crud
from sqlalchemy.orm import Session
from db.database import SessionLocal,engine

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


@app.get("/{item_id}") #path parameters
async def root(item_id: int):
    return {"message": item_id}

@app.post("/items") #Recebe um body
#use o embed sempre que puder para utilizar sempre o mesmo padrão
async def receive_item(item: Item = Body(..., embed = True)): #body - multipleparams Embed(docs)
    print(item.name)
    return item

@app.post("/create", response_model=user_schema.UserOut)
def create_user(user: user_schema.User, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered")
    return user_crud.create_user(db, user)
   
# @app.post("/delete/{user_id}", response_model=user_schema.UserOut)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # user_crud.teste()