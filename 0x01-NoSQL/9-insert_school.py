#!/usr/bin/env python3
'''function that inserts a new document in a collection based on kwargs'''


def insert_school(mongo_collection, **kwargs):
    '''inserts a new document in a collection based on kwargs'''
    document = mongo_collection.insert_one(kwargs)
    return document.inserted_id
