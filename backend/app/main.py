from fastapi import FastAPI
from app.api.main import api_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(api_router)
