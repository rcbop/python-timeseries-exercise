MONGO_OPERATOR_SYMBOLS = {
    'gte': '$gte',
    'lte': '$lte',
    'eq': '$eq',
    'ne': '$ne',
    'gt': '$gt',
    'lt': '$lt'
}
ISO_TIMESTAMP_REGEX = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+Z)?$'
DEFAULT_MONGO_URI = "mongodb://localhost:27017"
DEFAULT_MONGO_DB_NAME = "timeseries-visualization-test"
DEFAULT_MONGO_TS_COLLECTION_NAME = "sensor_data"
