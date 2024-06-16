#!/usr/bin/env python3
"""
12. Log stats
"""
from pymongo import MongoClient

def print_stats():
    """
    Provides some stats about Nginx logs stored in MongoDB
    """
    with MongoClient('mongodb://127.0.0.1:27017') as client:
        nginx_collection = client.logs.nginx
        total_logs = nginx_collection.count_documents({})
        print(f"{total_logs} logs")
        
        print("Methods:")
        methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        method_counts = {method: 0 for method in methods}

        # Aggregate counts for each method
        pipeline = [
            {"$group": {"_id": "$method", "count": {"$sum": 1}}}
        ]
        method_stats = nginx_collection.aggregate(pipeline)

        for stat in method_stats:
            method = stat["_id"]
            count = stat["count"]
            method_counts[method] = count

        for method in methods:
            print(f"\tmethod {method}: {method_counts[method]}")

        # Count for method GET and path /status
        status_check_count = nginx_collection.count_documents({"method": "GET", "path": "/status"})
        print(f"{status_check_count} status check")

if __name__ == "__main__":
    print_stats()
