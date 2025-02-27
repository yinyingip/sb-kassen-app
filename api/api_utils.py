from .db_utils import session, gm_shops
from sqlalchemy import select, distinct, func
from geojson_pydantic import Feature, Polygon
from pydantic import BaseModel, ValidationError, field_validator
import json


AREA_THRESHOLD = 5e3 * 5e3
RESULT_THRESHOLD = 50

def get_area(area_json_str):
    try:
        stmt = select(func.st_area(func.st_transform(func.ST_GeomFromGeoJSON(area_json_str),3035)).label('area'))
        result = session.execute(stmt).fetchone()
        return result.area
    except Exception as e:
        print(e)
        print('There is a problem when fetching the data.')
        session.rollback()

def get_shop_types():
    try:
        stmt = select(distinct(gm_shops.c.shop))
        results = session.execute(stmt).fetchall()
        return [row.shop for row in results]
    except Exception as e:
        print(e)
        print('There is a problem when fetching the data.')
        session.rollback()

default_shops = get_shop_types()
class ShopsQuery(BaseModel):
    shop_types: list =   default_shops
    area: Feature | None
    with_sb_kassen: bool = True

    @field_validator('area', mode='before')  
    @classmethod
    def dummy_bbox(cls, geo_feature):
        # skip validation of bbox and always provide a valid dummy bbox
        geo_feature['bbox'] = [1,2,3,4]
        return geo_feature  

    @field_validator('area', mode='after')  
    @classmethod
    def is_polygon(cls, geo_feature):
        if type(geo_feature.geometry) != Polygon:
            raise ValueError('The input geofeature is not a GeoJson Polygon.')
        return geo_feature  

def get_shops(shop_types,area_geom,sb_kassen_filter):
    try:
        assert len(shop_types) > 0, 'Please provide at least one shop type.'
        # to-do: provide a default area?
        area_json_str = json.dumps(area_geom)
        assert get_area(area_json_str) <= AREA_THRESHOLD, 'Please select a smaller area.'
        stmt = (select(gm_shops)
            .where(func.ST_Within(gm_shops.c.coords,func.ST_GeomFromGeoJSON(area_json_str)))
            .where(gm_shops.c.shop.in_(shop_types))
        )
        if sb_kassen_filter:
            stmt = stmt.where(gm_shops.c.sb_kassen_exist == True)
        # Step 3: Execute the query
        results = session.execute(stmt).fetchall()
        results = [r._asdict() for r in results]
        # Step 4: Print the results
        print(f'Return {len(results)} Shops')
        return results
    except Exception as e:
        print(e)
        print('There is a problem when fetching the data.')
        session.rollback()