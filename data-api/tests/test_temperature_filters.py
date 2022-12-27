from api.temperature.filters import parse_query_string

def test_parse_query_string():
    """Test the parse_query_string function."""
    result = parse_query_string("timestamp[gte]=2022-12-28T21:29:37.448000&timestamp[lte]=2022-12-28T20:35:41.410000&limit[eq]=2&sensor_area[eq]=kitchen")
    assert result == {
        "timestamp": {
            "gte": "2022-12-28T21:29:37.448000",
            "lte": "2022-12-28T20:35:41.410000",
        },
        "limit": {
            "eq": "2",
        },
        "sensor_area": {
            "eq": "kitchen",
        }
    }
