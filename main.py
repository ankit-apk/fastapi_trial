from fastapi import FastAPI
import pyrebase
import router

app = FastAPI()


@app.get("/")
def index():
    return {"Hello": "World"}


app.include_router(router.router, prefix="/products", tags=["product"])