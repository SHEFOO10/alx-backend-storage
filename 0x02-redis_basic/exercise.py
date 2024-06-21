#!/usr/bin/env python3
""" 0. Writing strings to Redis """
import redis
import uuid
from typing import Union, Optional, Callable, Any
import functools


def count_calls(method: Callable) -> Callable:
    """ count_calls decorator """
    @functools.wraps(method)
    def wrapper(*args, **kargs):
        """ wrapper function """
        self = args[0]
        client = self._redis
        client.incr(method.__qualname__, 1)
        return method(*args, **kargs)
    return wrapper


class Cache:
    """ Cache class """
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store the input data in Redis using the random key
        and return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        get data from redis
        """
        client = self._redis
        value = client.get(key)
        if not value:
            return
        if fn is int:
            return self.get_int(value)
        if fn is str:
            return self.get_str(value)
        if callable(fn):
            return fn(value)
        return value

    def get_int(self, data: bytes) -> int:
        """ converts data from bytes to int """
        return int(data)

    def get_str(self, data: bytes) -> str:
        return data.decode('UTF-8')
