import pytest
from api_utils import get_shops, get_review_stat, AREA_THRESHOLD

# Mock data for a GeoJSON polygon with a large area
large_area_geom = {
    "type": "Polygon",
    "coordinates": [
        [
            [10.931396, 47.761484],
            [10.931396, 48.494768],
            [12.381592, 48.494768],
            [12.381592, 47.761484],
            [10.931396, 47.761484],
        ]
    ],
}


def test_get_shops_raises_when_area_exceeds_threshold():
    with pytest.raises(AssertionError, match="Please select a smaller area."):
        get_shops(
            shop_types=["Supermarkt"], area_geom=large_area_geom, sb_kassen_filter=True
        )


def test_get_review_stat_raises_when_place_ids_empty():
    with pytest.raises(AssertionError, match="Please provide at least one place_id."):
        get_review_stat(place_ids=[])
