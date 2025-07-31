from fastapi import FastAPI
from router import router

app = FastAPI()

app.include_router(router) 

@app.get("/")
def read_root():
    return {"Wellcome to": "Short Location"}
