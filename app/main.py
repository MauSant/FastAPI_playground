
#FastAPI
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from db.init_db import init_db

#From 3th
import uvicorn
import asyncio

#From 1th
from api.routes import api_router


app = FastAPI()

app.include_router(api_router)

origins = [
    "http://127.0.0.1:8000",
    "https://127.0.0.1:8000 ",
    "http://localhost"
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#TODO: Not working, must select the interpreter created by poetry and run on a normal launch.json
def start_debug():
    a=asyncio.run(init_db())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    a=asyncio.run(init_db())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)