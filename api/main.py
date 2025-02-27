from fastapi import FastAPI, Depends
from .auth import get_api_key
from .api_utils import get_shop_types, get_shops, ShopsQuery

desc = '''
Here's where magic happens (if any).
'''

app = FastAPI(title="ST Testing API",
              description=desc,
              dependencies=[Depends(get_api_key)]
              )

@app.get("/")
def read_root():
    return {"Hello": "World una"}

@app.get("/get_names")
def get_names():
    return get_shop_types()

@app.post("/shops")
def post_shops(input:ShopsQuery):
    print(input.area.model_dump())
    try:
        result = get_shops(input.shop_types,
                           input.area.geometry.model_dump(),
                           input.with_sb_kassen
                           )
        
        # return {"Hello": input.shop_types,
        #         # model_dump transform the class into dict
        #         # "Area": input.area.model_dump().get('geometry').get('coordinates'),
        #         "Area": input.area.geometry.model_dump(),
        #         "SB Kassen Filter": input.with_sb_kassen
        #         }
        return result
    except Exception as e:
        print(e)
        print(' Something goes wrong')