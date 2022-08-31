
#FastAPI
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from db.init_db import init_db

#From 3th
import uvicorn
from db.database import get_mongo_client


#From 1th
# from api.routes import api_router


app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongo_client = get_mongo_client()
    init_db(app.mongo_client)


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongo_client.close()

# app.include_router(api_router)

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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)