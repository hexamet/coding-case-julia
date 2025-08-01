from typing import Union

from fastapi import FastAPI
from router import router

app = FastAPI()

app.include_router(router) 


@app.get("/")
def read_root():
    return {"Wellcome to": "Short Location"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}