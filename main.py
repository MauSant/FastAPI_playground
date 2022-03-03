import uvicorn

from fastapi import FastAPI

from api.routes import api_router
app = FastAPI()

app.include_router(api_router)

@app.get("/me")
async def root():
    return 'I live I die, I live Again'











   





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