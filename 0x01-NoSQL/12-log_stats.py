#!/usr/bin/env python3
"""
12. Log stats
"""
from pymongo import MongoClient
client = MongoClient('mongodb://127.0.0.1:27017')
nginx_collection = client.logs.nginx


def print_stats():
    """
    provides some stats about Nginx logs stored in MongoDB
    """
    x = nginx_collection.count_documents({})
    print(f"{x} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print("	method {}: {}".format(method, count))
    print("{} status check".format(nginx_collection.count_documents(
        {"method": "GET", "path": '/status'}
    )))


print_stats()
