"""ObjectRocket Python client constants."""

API_URL_MAP = {
    'default': 'http://localhost:5050/v2/',  # Point this to the LB when deployed.
    'testing': 'http://localhost:5050/v2/',
}

MONGODB_SHARDED_INSTANCE = 'mongodb_sharded'
MONGODB_REPLICA_SET_INSTANCE = 'mongodb_replica_set'

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
