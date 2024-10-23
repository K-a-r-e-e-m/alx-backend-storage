#!/usr/bin/env python3
'''This module having function that lists all documents in a collection'''

def list_all(mongo_collection):
    '''lists all documents in a collection'''
    if mongo_collection.count_documents({}) == 0:
        return []

    return mongo_collection.find()
