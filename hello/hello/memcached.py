import json
import datetime
import time
from pymemcache.client.base import Client
from flask import current_app

def dt_serializer(obj):
    if isinstance(obj, datetime.datetime):
        serialized_time = time.mktime(obj.timetuple())
        return serialized_time
    raise TypeError("Type not serializable")

def json_serializer(key, value):
    if type(value) == str:
        return value, 1
    return json.dumps(value, default=dt_serializer), 2

def json_deserializer(key, value, flags):
    if flags == 1:
        return value
    if flags == 2:
        return json.loads(value)
    raise Exception("Unknown serialization format")

def get_mc_client():
    mc_host = current_app.config.get('MEMCACHED_HOST')
    return Client((mc_host, 11211), serializer=json_serializer, deserializer=json_deserializer)
