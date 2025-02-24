'''
uvicorn api.main:app --reload
'''
from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World una"}