import re
from urllib.parse import parse_qs

from pyparsing import Literal, Or, ParserElement, Word, ZeroOrMore, alphanums
from pyparsing.exceptions import ParseException


class InvalidQueryError(ValueError):
    """Exception raised when an invalid query string is used."""


class QueryFiltersValidationGrammar:
    def __init__(self) -> None:
        # value
        value = Word(alphanums + "-:T.")

        # timestamp field
        timestamp = Literal("timestamp")
        timestamp_op = Or([Literal(x)
                          for x in ["gte", "lte", "eq", "ne", "gt", "lt"]])
        timestamp_expr = timestamp + "[" + timestamp_op + "]=" + value

        # metadata field
        metadata = Literal("metadata.")
        metadata_name = Or(Literal(x) for x in ["area", "uuid", "type"])
        metadata_expr = metadata + metadata_name + "=" + value

        # limit and offset fields
        limit = Literal("limit") + "=" + value
        offset = Literal("offset") + "=" + value

        # associative operators
        connectors = Literal("&")

        multi_expr = timestamp_expr | metadata_expr | limit | offset
        multi_expr_list = multi_expr + ZeroOrMore(connectors + multi_expr)
        self.query: ParserElement = multi_expr_list

    def validate(self, raw_query: str):
        """Validate the query string.

        Raises:
            pyparsing.exceptions.ParseException: If the query string is invalid.

        Args:
            raw_query (str): The query string to validate.
        """
        self.query.parseString(raw_query, parseAll=True)


class QueryFilters:
    def __init__(self, validation_grammar: QueryFiltersValidationGrammar = QueryFiltersValidationGrammar()):
        self.__validation_grammar = validation_grammar

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
        try:
            self.__validation_grammar.validate(raw_query)
        except ParseException as err:
            raise InvalidQueryError(
                f'Invalid query string: {raw_query}') from err

        filters = self.parse_query_string_into_filters(raw_query)
        filters = self._cleanup_query_empty_values(filters)
        return filters

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
