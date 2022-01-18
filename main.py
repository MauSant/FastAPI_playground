from typing_extensions import Required
from fastapi import FastAPI, Body, HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from models.item import Item
import uvicorn
from models.schemas import user_schema
import db.user_crud as user_crud

#testing
from db import user_crud
from db.database import SessionLocal

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

@app.post("/create", response_model=user_schema.UserIn)
def create_user(user:user_schema.UserIn, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        return user_crud.create_user(db, user)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # user_crud.teste()