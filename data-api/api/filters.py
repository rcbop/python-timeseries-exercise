import re
from urllib.parse import parse_qs

from api.constants import MONGO_OPERATOR_SYMBOLS


class InvalidQueryError(ValueError):
    """Exception raised when an invalid query string is used."""


class InvalidOperatorError(InvalidQueryError):
    """Exception raised when an invalid operator is used in a query string."""


class InvalidFieldError(InvalidQueryError):
    """Exception raised when an invalid field is used in a query string."""


class QueryFilters:
    def __init__(self, valid_fields: list[str],
                 valid_operators: list[str] = list(MONGO_OPERATOR_SYMBOLS)):
        self.__valid_fields = valid_fields
        self.__valid_operators = valid_operators

    # Allow regular expression to group nested key like <key.subkey> format (e.g. metadata.area)
    FILTERS_REGEX = r'(?P<key>[^\[\.]+)(?:\[(?P<value>[^\]]+)\])?(?:\.(?P<subkey>[^\.]+))?'

    def parse_and_validate(self, raw_query: str) -> dict[str, dict[str, str]]:
        """Parse a query string, validates balanced brackets, cleanup empty values and validate the fields and operators.

        Args:
            raw_query (str): The query string to parse.

        Raises:
            InvalidQueryError: If the query string is invalid.
            InvalidQueryFieldError: If the query string contains an invalid field.
            InvalidQueryOperatorError: If the query string contains an invalid operator.

        Returns:
            dict[str, dict[str, str]]: The parsed query string.
        """
        if not self._is_balanced_brackets(raw_query):
            raise InvalidQueryError(
                "The query string operator brackets is not balanced.")

        filters = self.parse_query_string_into_filters(raw_query)
        filters = self._cleanup_query_empty_values(filters)
        self._validate_filters_fields(filters)

        check_operators_filters_copy = filters.copy()
        # Operators are not valid for the limit field
        if "limit" in check_operators_filters_copy:
            del check_operators_filters_copy["limit"]
        # Operators are not valid for the metadata field
        if "metadata" in check_operators_filters_copy:
            del check_operators_filters_copy["metadata"]
        self._validate_filters_operators(check_operators_filters_copy)
        return filters

    def _is_balanced_brackets(self, raw_query: str) -> bool:
        """ Validate that the brackets in the query string are balanced.

            returns False if the query string is not balanced e.g: ?timestamp[=2021-01-01T00:00:00

            this will not work as intended if the closing bracket is in another field
            e.g: ?timestamp[=2021-01-01T00:00:00&metadata.area=kitchen]

            to fix we would need to use a grammar parser like pyparsing

            Returns:
                bool: True if the brackets are balanced, False otherwise.
        """
        brackets_count = 0
        for char in raw_query:
            if char == "[":
                brackets_count += 1
            elif char == "]":
                brackets_count -= 1

        return brackets_count == 0

    def parse_query_string_into_filters(self, raw_query: str) -> dict[str, dict[str, str]]:
        """Parse a query string into a dictionary.

        This query string:

            ?timestamp[gte]=2021-01-01T00:00:00&timestamp[lte]=2021-01-05T00:00:00&metadata.area=kitchen&limit=100"

        Should result in a dictionary like:
            {
                "timestamp": { "gte": "2021-01-01T00:00:00", "lte": "2021-01-05T00:00:00" },
                "metadata": { "area": "kitchen" },
                "limit": "100"
            }

        Only the first occurrence of a key is considered.
        If the same key is repeated, the first value is used.

        Args:
            raw_query (str): The query string to parse.

        Raises:
            InvalidQueryError: If the query string is invalid.

        Returns:
            dict[str, dict[str, str]]: The parsed query string.
        """
        filter = {}
        for key, value in parse_qs(raw_query).items():
            match = re.match(self.FILTERS_REGEX, key)
            group_dict = match.groupdict()
            if not match:
                raise InvalidQueryError(
                    f'Invalid query string: {raw_query}')

            key = group_dict['key']
            if group_dict['subkey']:
                # If a subkey was matched, add the key-value pair to the dictionary
                newkey = f"{key}.{group_dict['subkey']}"
                filter[newkey] = value[0]
            elif group_dict['value']:
                # If a value was matched, add it to the dictionary
                filter.setdefault(key, {})[
                    group_dict['value']] = value[0]
            else:
                # If no value or subkey was matched, add the key-value pair to the dictionary
                filter[key] = value[0]
        return filter

    def _validate_filters_fields(self, filters: dict):
        """Validate the keys of a filter dictionary.

        Args:
            filters (dict): The filter dictionary to validate.
            valid_keys (list): The list of valid keys.

        Raises:
            InvalidFieldError: If the filter dictionary contains invalid keys.
        """
        for key in filters.keys():
            if key not in self.__valid_fields:
                raise InvalidFieldError(f'Invalid filter field: {key}')

    def _validate_filters_operators(self, check_operators_filters: dict):
        """Validate the operators of a filter dictionary.

        Args:
            filters (dict): The filter dictionary to validate.
            valid_operators (list): The list of valid operators.

        Raises:
            InvalidOperatorError: If the filter dictionary contains invalid operators.
        """
        for _, value in check_operators_filters.items():
            if not isinstance(value, dict):
                continue
            for operator in value.keys():
                if operator not in self.__valid_operators:
                    raise InvalidOperatorError(
                        f"Invalid filter operator: {operator}")

    def _cleanup_query_empty_values(self, query: dict) -> dict:
        """Traverse dictionary recursiverly and clean empty fields and operators.
        e.g:

        { "timestamp": { "gte": "", "lte": "2021-01-05T00:00:00" }

        should be cleaned up to:

        { "timestamp": { "lte": "2021-01-05T00:00:00" }

        Args:
            query (dict): The query dictionary to clean up.

        Returns:
            dict: The cleaned up query dictionary.
        """
        if not isinstance(query, dict):
            return query
        return {k: self._cleanup_query_empty_values(v) for k, v in query.items() if v}
