from .db_utils import session, gm_shops, sb_reviews
from sqlalchemy import select, distinct, func
from geojson_pydantic import Feature, Polygon
from pydantic import BaseModel, ValidationError, field_validator
from typing import List
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta


AREA_THRESHOLD = 10e3 * 10e3
RESULT_THRESHOLD = 50


def get_area(area_json_str):
    try:
        stmt = select(
            func.st_area(
                func.st_transform(func.ST_GeomFromGeoJSON(area_json_str), 3035)
            ).label("area")
        )
        result = session.execute(stmt).fetchone()
        return result.area
    except Exception as e:
        print(e)
        print("There is a problem when fetching the data.")
        session.rollback()


def get_shop_types():
    try:
        stmt = select(distinct(gm_shops.c.shop))
        results = session.execute(stmt).fetchall()
        return [row.shop for row in results]
    except Exception as e:
        print(e)
        print("There is a problem when fetching the data.")
        session.rollback()


default_shops = get_shop_types()


class ShopsQuery(BaseModel):
    shop_types: List[str] = default_shops
    area: Feature | None
    with_sb_kassen: bool = True

    @field_validator("area", mode="before")
    @classmethod
    def dummy_bbox(cls, geo_feature):
        # skip validation of bbox and always provide a valid dummy bbox
        geo_feature["bbox"] = [1, 2, 3, 4]
        return geo_feature

    @field_validator("area", mode="after")
    @classmethod
    def is_polygon(cls, geo_feature):
        if type(geo_feature.geometry) != Polygon:
            raise ValueError("The input geofeature is not a GeoJson Polygon.")
        return geo_feature


def get_shops(shop_types, area_geom, sb_kassen_filter):
    try:
        assert len(shop_types) > 0, "Please provide at least one shop type."
        # to-do: provide a default area?
        area_json_str = json.dumps(area_geom)
        assert (
            get_area(area_json_str) <= AREA_THRESHOLD
        ), "Please select a smaller area."
        stmt = (
            select(gm_shops)
            .where(
                func.ST_Within(
                    gm_shops.c.coords, func.ST_GeomFromGeoJSON(area_json_str)
                )
            )
            .where(gm_shops.c.shop.in_(shop_types))
        )
        if sb_kassen_filter:
            stmt = stmt.where(gm_shops.c.sb_kassen_exist == True)
        # Step 3: Execute the query
        results = session.execute(stmt).fetchall()
        results = [r._asdict() for r in results]
        # Step 4: Return the results
        print(f"Return {len(results)} Shops")
        return results
    except AssertionError as e:
        raise AssertionError(e)
    except Exception as e:
        print(e)
        raise Exception("There is a db problem when fetching the data.")
    finally:
        session.rollback()


class ReviewQuery(BaseModel):
    place_ids: List[str]


def get_review_stat(place_ids):
    try:
        assert len(place_ids) > 0, "Please provide at least one place_id."
        stmt = (
            select(
                sb_reviews.c.place_id,
                func.count().label("num_review"),
                func.max(sb_reviews.c.review_date).label("latest_review_date"),
            )
            .where(sb_reviews.c.verif == "SB")
            .group_by(sb_reviews.c.place_id)
        )
        # Step 3: Execute the query
        results = session.execute(stmt).fetchall()
        results = [r._asdict() for r in results]
        for i in range(len(results)):
            rel_dt_de = relative_date_from_now(results[i]["latest_review_date"], "de")
            rel_dt_en = relative_date_from_now(results[i]["latest_review_date"], "en")
            results[i]["latest_review_relative_date"] = {
                "de": rel_dt_de,
                "en": rel_dt_en,
            }
        # Step 4: Reformatting the list to a dictionary and return the results
        result_dict = {
            item["place_id"]: {
                "num_review": item["num_review"],
                "latest_review_date": item["latest_review_date"],
                "latest_review_relative_date": item["latest_review_relative_date"],
            }
            for item in results
        }
        return result_dict
    except AssertionError as e:
        raise AssertionError(e)
    except Exception as e:
        print(e)
        raise Exception("There is a db problem when fetching the data.")
    finally:
        session.rollback()


def relative_date_from_now(dt_isoformat, lang):
    rel_date_del = relativedelta(datetime.now(), dt_isoformat)
    assert lang in ["de", "en"], "Unsupport Language."
    time_unit = {
        "de": {"month": "Monat", "day": "Tag", "today": "heute"},
        "en": {"month": "month", "day": "day", "today": "today"},
    }
    if rel_date_del.months > 0:
        time_int = rel_date_del.months
        time_unit = time_unit[lang]["month"]
    elif rel_date_del.days > 0:
        time_int = rel_date_del.days
        time_unit = time_unit[lang]["day"]
    else:
        return time_unit[lang]["today"]
    if lang == "de":
        return f"vor {time_int} {time_unit}{'en' if time_int != 1 else ''}"
    return f"{time_int} {time_unit}{'s' if time_int != 1 else ''} ago"
