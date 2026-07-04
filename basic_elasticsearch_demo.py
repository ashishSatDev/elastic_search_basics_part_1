#!/usr/bin/env python3
"""Simple Elasticsearch demo using the standard library.

This script demonstrates:
1. Checking cluster health
2. Creating an index
3. Indexing sample documents
4. Running a basic search query
5. Running a simple aggregation
"""

import json
import urllib.error
import urllib.request

ES_URL = "http://localhost:9200"
INDEX_NAME = "products"


def request(method: str, path: str, payload: dict | None = None):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(f"{ES_URL}{path}", data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} failed with {exc.code}: {error_body}") from exc


def print_json(title: str, payload: dict) -> None:
    print(f"\n{title}")
    print(json.dumps(payload, indent=2))


def main() -> None:
    print("Connecting to Elasticsearch at", ES_URL)

    status, health = request("GET", "/_cluster/health")
    print(f"Cluster health status: {health['status']} (HTTP {status})")

    try:
        request("DELETE", f"/{INDEX_NAME}")
        print(f"Deleted existing index: {INDEX_NAME}")
    except RuntimeError as exc:
        print(f"No existing index to delete: {exc}")

    mapping = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        },
        "mappings": {
            "properties": {
                "name": {"type": "text"},
                "category": {"type": "keyword"},
                "price": {"type": "float"},
                "in_stock": {"type": "boolean"},
            }
        },
    }
    status, create_result = request("PUT", f"/{INDEX_NAME}", mapping)
    print(f"Index created: {create_result.get('acknowledged')} (HTTP {status})")

    documents = [
        {"name": "Laptop Pro", "category": "electronics", "price": 1200.0, "in_stock": True},
        {"name": "Wireless Mouse", "category": "electronics", "price": 25.5, "in_stock": True},
        {"name": "Notebook", "category": "stationery", "price": 4.0, "in_stock": False},
    ]

    for document in documents:
        status, result = request("POST", f"/{INDEX_NAME}/_doc", document)
        print(f"Indexed document {result.get('_id')} (HTTP {status})")

    status, _ = request("POST", f"/{INDEX_NAME}/_refresh")
    print(f"Index refreshed (HTTP {status})")

    search_payload = {
        "query": {"match": {"name": "wireless"}},
        "size": 5,
    }
    status, search_result = request("POST", f"/{INDEX_NAME}/_search", search_payload)
    print_json("Search results", search_result)

    aggregation_payload = {
        "size": 0,
        "aggs": {
            "by_category": {
                "terms": {"field": "category"}
            }
        },
    }
    status, agg_result = request("POST", f"/{INDEX_NAME}/_search", aggregation_payload)
    print_json("Aggregation results", agg_result)


if __name__ == "__main__":
    main()
