from fastapi import FastAPI, Depends
from .auth import get_api_key

desc = '''
Here's where magic happens.
'''

app = FastAPI(title="ST Testing API",
              description=desc,
              dependencies=[Depends(get_api_key)]
              )

@app.get("/")
def read_root():
    return {"Hello": "World una"}