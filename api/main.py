from fastapi import FastAPI, Depends, HTTPException
from .auth import get_api_key
from .api_utils import (
    get_shop_types,
    get_shops,
    ShopsQuery,
    get_review_stat,
    ReviewQuery,
)

desc = """
Here's where magic happens (if any).
"""

app = FastAPI(
    title="ST Testing API", description=desc, dependencies=[Depends(get_api_key)]
)


@app.get("/")
def read_root():
    return {"Hello": "World una"}


@app.get("/get_names")
def get_names():
    return get_shop_types()


@app.post("/shops")
def post_shops(input: ShopsQuery):
    print(input.area.model_dump())
    try:
        result = get_shops(
            input.shop_types, input.area.geometry.model_dump(), input.with_sb_kassen
        )
        return result
    except AssertionError as e:
        print(e)
        print(" Something goes wrong")
        raise HTTPException(status_code=400, detail=f"Bad Request: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error")


@app.post("/reviews")
def post_shops(input: ReviewQuery):
    try:
        result = get_review_stat(input.place_ids)
        return result
    except AssertionError as e:
        print(e)
        print(" Something goes wrong")
        raise HTTPException(status_code=400, detail=f"Bad Request: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error")
