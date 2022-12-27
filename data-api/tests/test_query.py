import pytest
from api.query import MongoQueryFilter, InvalidMongoQueryFilterError
from datetime import datetime

@pytest.mark.parametrize("test_case,filter_params,expected_query", [
    (
        "Empty filter >>>",
        {},
        {}
    ),
    (
        "complex filter >>>",
        {
            "timestamp": {
                "gte": "2022-12-28T21:29:37.448000",
                "lte": "2022-12-28T20:35:41.410000",
            },
            "metadata": {
                "sensor_area": "kitchen",
            }
        },
        {
            "timestamp": {
                "$gte": datetime.fromisoformat("2022-12-28T21:29:37.448000"),
                "$lte": datetime.fromisoformat("2022-12-28T20:35:41.410000"),
            },
            "metadata": { "sensor_area": "kitchen" }
        }
    )
])
def test_mongo_query_filter_build_from_filters(test_case: str, filter_params: dict, expected_query: dict):
    """Test mongo query filter."""
    print(f"Test case: {test_case}")
    mongo_query_filter = MongoQueryFilter()
    got_query = mongo_query_filter.build_from_filters(filter_params)
    assert got_query == expected_query


@pytest.mark.parametrize("test_case,filter_params,expected_error",
    [
        (
            "Invalid field >>>",
            {
                "limit": "2",
            },
            InvalidMongoQueryFilterError
        ),
    ]
)
def test_mongo_query_filter_build_with_error(test_case: str, filter_params: dict, expected_error: Exception):
    """Test mongo query filter."""
    print(f"Test case: {test_case}")
    mongo_query_filter = MongoQueryFilter()
    with pytest.raises(expected_error):
        mongo_query_filter.build_from_filters(filter_params)
