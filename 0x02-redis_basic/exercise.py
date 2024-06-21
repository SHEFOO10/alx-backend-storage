#!/usr/bin/env python3
""" 0. Writing strings to Redis """
import redis
import uuid
from typing import Union, Optional, Callable, Any
import functools


def count_calls(method: Callable) -> Callable:
    """Decorator to count calls to a method."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
     a decorator to store the history of inputs
     and outputs for a particular function.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kargs):
        inputs = method.__qualname__ + ':inputs'
        outputs = method.__qualname__ + ':outputs'
        self._redis.rpush(inputs, str(args))
        self._redis.rpush(outputs, method(self, *args))
    return wrapper


class Cache:
    """ Cache class """
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key
        and return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        Get data from Redis and optionally apply a transformation function.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is int:
            return self.get_int(value)
        if fn is str:
            return self.get_str(value)
        if callable(fn):
            return fn(value)
        return value

    def get_int(self, data: bytes) -> int:
        """Converts data from bytes to int."""
        return int(data)

    def get_str(self, data: bytes) -> str:
        """Converts data from bytes to str."""
        return data.decode('utf-8')
