#!/usr/bin/env python3
"""Writing strings to Redis"""
from uuid import uuid4
from typing import Union, Optional, Callable
from functools import wraps
import redis


def call_history(method: Callable) -> Callable:
    """Function to store the history of inputs and outputs of a function"""

    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Function that defines wrapper"""

        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper


def count_calls(method: Callable) -> Callable:
    '''takes a single method Callable argument and returns a Callable'''
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

    @call_history
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


def replay(method: Callable):
    """Function that prints the history of calls of a function"""

    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    redis = method.__self__._redis
    count = redis.get(key).decode("utf-8")
    print("{} was called {} times:".format(key, count))

    list_input = redis.lrange(inputs, 0, -1)
    list_output = redis.lrange(outputs, 0, -1)
    zipped = list(zip(list_input, list_output))

    for ins, outs in zipped:
        attr, data = ins.decode("utf-8"), outs.decode("utf-8")
        print("{}(*{}) -> {}".format(key, attr, data))
