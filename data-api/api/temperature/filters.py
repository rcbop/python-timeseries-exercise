import re
from urllib.parse import parse_qs


def parse_query_string(raw_query: str):
    """Parse a query string into a dictionary.

    Args:
        raw_query (str): The query string to parse.

    Returns:
        dict: A dictionary of the parsed query string.
    """
    d = {}
    for key, value in parse_qs(raw_query).items():
        match = re.match(r'(?P<key>[^\[]+)\[(?P<value>[^\]]+)\]', key)
        gd = match.groupdict()
        d.setdefault(gd['key'], {})[gd['value']] = value[0]
    return d
