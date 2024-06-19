#!/usr/bin/env python3
""" 0. Writing strings to Redis """
import redis
import uuid
from typing import Union


class Cache:
    """ Cache class """
    def __init__(self):
        self._redis = redis.Redis()

    def store(self, data: Union[str, bytes, float, int]) -> str:
        """
        store the input data in Redis using the random key
        and return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
