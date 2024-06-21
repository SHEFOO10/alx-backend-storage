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
    key = method.__qualname__
    inputs = key + ':inputs'
    outputs = key + ':outputs'

    @functools.wraps(method)
    def wrapper(self, *args, **kargs):
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kargs)
        self._redis.rpush(outputs, data)
        return data
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


def replay(method: Callable) -> None:
    """
    display the history of calls of a particular function.
    """
    key = method.__qualname__
    client = redis.Redis()
    inputs = key + ':inputs'
    outputs = key + ':outputs'
    calls = client.llen(inputs)
    print('{} was called {} times:'.format(key, calls))
    for method_inputs, output in zip
    (
        client.lrange(inputs, 0, -1),
        client.lrange(outputs, 0, -1)
    ):
        print("{}(*{}) -> {}".format(
            key,
            method_inputs.decode('UTF-8'),
            output.decode('UTF-8')))
