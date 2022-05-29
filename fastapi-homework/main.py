import os

from fastapi import FastAPI


MSG = os.environ.get("MSG")
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": MSG}
