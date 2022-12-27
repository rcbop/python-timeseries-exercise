import re
from datetime import datetime

from api.constants import ISO_TIMESTAMP_REGEX, MONGO_OPERATOR_SYMBOLS

class InvalidMongoQueryFilterError(ValueError):
    """Exception raised when an invalid query filter is used."""


class MongoQueryFilter():
    def __init__(self,
                 mongo_operator_symbols: dict[str,
                                              str] = MONGO_OPERATOR_SYMBOLS,
                 iso_timestamp_regex: str = ISO_TIMESTAMP_REGEX) -> None:
        self.__mongo_operator_symbols = mongo_operator_symbols
        self.__iso_timestamp_regex = iso_timestamp_regex

    def build_from_filters(self, filter_params: dict) -> dict:
        """Build a MongoDB query from a filter dictionary.

        Args:
            filter_params (dict): The filter dictionary to convert.

        Raises:
            ValueError: If the filter dictionary contains a limit key.

        Returns:
            dict: The MongoDB query.
        """

        if "limit" in filter_params:
            raise InvalidMongoQueryFilterError("Limit is not allowed in query")

        query = {}
        for key, value in filter_params.items():
            # Check if the value is a dictionary
            if isinstance(value, dict):
                # Add the subquery to the main query
                query[key] = self._build_subquery(value)
            else:
                # If the value is not a dictionary, add it to the main query as-is
                query[key] = value
        return self.convert_isotimestamp_to_datetime(query)

    def _build_subquery(self, value: dict) -> dict:
        # If the value is a dictionary, iterate over the key-value pairs
        subquery = {}
        for subkey, subvalue in value.items():
            # Check if the subkey is in the operator_symbols map
            if subkey in self.__mongo_operator_symbols:
                # If the subkey is an operator, convert it to the corresponding MongoDB operator
                subquery[self.__mongo_operator_symbols[subkey]] = subvalue
            else:
                # If the subkey is not an operator, add it to the subquery as-is
                subquery[subkey] = subvalue
        return subquery


    def convert_isotimestamp_to_datetime(self, mongo_query: dict) -> dict:
        """Convert ISO timestamp strings to datetime objects for pymongo.

        Args:
            mongo_query (dict): The MongoDB query to convert.

        Returns:
            dict: The converted MongoDB query.
        """
        for key, value in mongo_query.items():
            if isinstance(value, dict):
                mongo_query[key] = self.convert_isotimestamp_to_datetime(value)
            elif isinstance(value, str) and re.match(self.__iso_timestamp_regex, value):
                mongo_query[key] = datetime.fromisoformat(value)
        return mongo_query
