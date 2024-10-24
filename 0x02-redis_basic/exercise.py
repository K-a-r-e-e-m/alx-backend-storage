#!/usr/bin/env python3
"""Writing strings to Redis"""
from uuid import uuid4
from typing import Any
import redis


class Cache:
    """Create method should generate a random key store the input
       data in Redis using the random key and return the key"""

    def __init__(self) -> None:
        '''init method that store an instance of the Redis client'''
        self._redis = redis.Redis()
        self._redis.flushdb

    def store(self, data: Any) -> str:
        '''method that takes a data argument and returns a string'''
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key
