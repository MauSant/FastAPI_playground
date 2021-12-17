from fastapi import FastAPI, Body
from models.item import Item
import uvicorn

app = FastAPI()


@app.get("/me")
async def root():
    return {"message": "Hello World"}


@app.get("/{item_id}") #path parameters
async def root(item_id: int):
    return {"message": item_id}

@app.post("/items") #Recebe um body
#use o embed sempre que puder para utilizar sempre o mesmo padrão
async def receive_item(item: Item = Body(None, embed = True)): #body - multipleparams Embed(docs)
    print(item.name)
    return item


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
