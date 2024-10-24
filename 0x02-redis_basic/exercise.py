#!/usr/bin/env python3
"""Writing strings to Redis"""
from uuid import uuid4
from typing import Union, Optional, Callable
from functools import wraps
import redis


def count_calls(method: Callable) -> Callable:
    '''decorator takes a single method Callable argument and returns a Callable'''
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        '''wrapper function body increamets when class methods called'''
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


class Cache:
    """Create method should generate a random key store the input
       data in Redis using the random key and return the key"""

    def __init__(self) -> None:
        '''init method that store an instance of the Redis client'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''method that takes a data argument and returns a string'''
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key, fn: Optional[Callable] = None) -> Union[
            str, bytes, int, float]:
        '''takes a key string argument and an Callable argument named fn'''

        value = self._redis.get(key)

        if value is None:
            return None

        if fn:
            return fn(value)

        return value

    def get_str(self, key: str) -> str:
        '''automatically parametrize Cache.get with conversion to string'''
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        '''automatically parametrize Cache.get with conversion to integer'''
        value = self._redis.get(key)
        return int(value.decode('utf-8'))
