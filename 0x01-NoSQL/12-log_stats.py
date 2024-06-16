#!/usr/bin/env python3
"""
12. Log stats
"""
from pymongo import MongoClient


def print_stats():
    """
    provides some stats about Nginx logs stored in MongoDB
    """
    client = MongoClient()
    db = client.logs
    print("{} logs".format(db.nginx.count_documents({})))
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = db.nginx.count_documents({"method": method})
        print("	method {}: {}".format(method, count))
    print("{} status check".format(db.nginx.count_documents(
        {"method": "GET", "path": '/status'}
    )))


print_stats()
