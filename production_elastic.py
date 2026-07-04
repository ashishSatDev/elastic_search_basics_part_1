#!/usr/bin/env python3
"""Production-style Elasticsearch demo with real-life search use cases.

This script demonstrates four common production scenarios:
1. E-commerce product search with filters and sorting
2. Application log search with date range and aggregation
3. Support ticket search with status and priority filters
4. Knowledge-base article search with highlighting and boosting
"""

import json
import urllib.error
import urllib.request

ES_URL = "http://localhost:9200"
INDEX_NAME = "production_demo"


def request(method: str, path: str, payload: dict | None = None):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(f"{ES_URL}{path}", data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} failed with {exc.code}: {error_body}") from exc


def print_section(title: str) -> None:
    print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")


def print_hits(title: str, result: dict) -> None:
    hits = result.get("hits", {}).get("hits", [])
    print(f"{title}: {len(hits)} result(s)")
    for hit in hits[:3]:
        source = hit.get("_source", {})
        print("-", source)


def create_index() -> None:
    mapping = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        },
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "content": {"type": "text"},
                "category": {"type": "keyword"},
                "status": {"type": "keyword"},
                "priority": {"type": "keyword"},
                "price": {"type": "float"},
                "rating": {"type": "float"},
                "level": {"type": "keyword"},
                "service": {"type": "keyword"},
                "timestamp": {"type": "date"},
                "tags": {"type": "keyword"},
                "author": {"type": "keyword"},
            }
        },
    }
    request("PUT", f"/{INDEX_NAME}", mapping)


def index_documents() -> None:
    docs = [
        {
            "title": "Wireless Noise Cancelling Headphones",
            "content": "Premium headphones with active noise cancellation and long battery life",
            "category": "electronics",
            "price": 249.99,
            "rating": 4.8,
            "status": "active",
            "tags": ["audio", "wireless"],
            "timestamp": "2026-07-01T10:00:00Z",
        },
        {
            "title": "Smart Fitness Watch",
            "content": "Water resistant smartwatch for daily health tracking and notifications",
            "category": "electronics",
            "price": 129.5,
            "rating": 4.6,
            "status": "active",
            "tags": ["wearable", "health"],
            "timestamp": "2026-07-02T08:30:00Z",
        },
        {
            "title": "Ergonomic Office Chair",
            "content": "Comfortable chair designed for long hours and posture support",
            "category": "furniture",
            "price": 189.0,
            "rating": 4.4,
            "status": "active",
            "tags": ["office", "comfort"],
            "timestamp": "2026-07-03T11:20:00Z",
        },
        {
            "title": "Payment gateway timeout error",
            "content": "Checkout requests are timing out during peak traffic",
            "level": "error",
            "service": "payments",
            "timestamp": "2026-07-04T09:15:00Z",
            "status": "open",
            "priority": "high",
        },
        {
            "title": "Login issue reported by customer",
            "content": "Some users cannot sign in after password reset flow",
            "level": "warning",
            "service": "auth",
            "timestamp": "2026-07-04T10:05:00Z",
            "status": "open",
            "priority": "medium",
        },
        {
            "title": "Refund policy update",
            "content": "New refund process for delayed orders and damaged items",
            "category": "support",
            "status": "published",
            "author": "support-team",
            "rating": 4.7,
            "tags": ["refund", "policy"],
            "timestamp": "2026-07-04T12:00:00Z",
        },
        {
            "title": "How to return a defective product",
            "content": "Step-by-step guide for returns, exchanges, and refund requests",
            "category": "support",
            "status": "published",
            "author": "support-team",
            "rating": 4.9,
            "tags": ["returns", "refund"],
            "timestamp": "2026-07-04T13:00:00Z",
        },
    ]

    for doc in docs:
        request("POST", f"/{INDEX_NAME}/_doc", doc)


def run_use_cases() -> None:
    print_section("Use Case 1: E-commerce product search")
    query1 = {
        "size": 5,
        "query": {
            "bool": {
                "must": [{"match": {"content": "wireless headphones"}}],
                "filter": [
                    {"term": {"category": "electronics"}},
                    {"range": {"price": {"gte": 100, "lte": 300}}},
                ],
            }
        },
        "sort": [{"price": {"order": "asc"}}],
    }
    status, result = request("POST", f"/{INDEX_NAME}/_search", query1)
    print_hits("E-commerce search", result)

    print_section("Use Case 2: Application log search")
    query2 = {
        "size": 10,
        "query": {
            "bool": {
                "must": [{"range": {"timestamp": {"gte": "now-24h/h"}}}],
                "filter": [{"term": {"level": "error"}}],
            }
        },
        "aggs": {"by_service": {"terms": {"field": "service"}}},
    }
    status, result = request("POST", f"/{INDEX_NAME}/_search", query2)
    print_hits("Log search", result)
    print("Aggregations:", result.get("aggregations", {}).get("by_service", {}).get("buckets", []))

    print_section("Use Case 3: Support ticket search")
    query3 = {
        "size": 5,
        "query": {
            "bool": {
                "must": [{"multi_match": {"query": "payment timeout", "fields": ["title", "content"]}}],
                "filter": [
                    {"term": {"status": "open"}},
                    {"term": {"priority": "high"}},
                ],
            }
        },
        "highlight": {"fields": {"content": {}}},
    }
    status, result = request("POST", f"/{INDEX_NAME}/_search", query3)
    print_hits("Support ticket search", result)
    hits = result.get("hits", {}).get("hits", [])
    if hits:
        print("Highlights:", hits[0].get("highlight", {}))
    else:
        print("Highlights: none")

    print_section("Use Case 4: Knowledge-base article search")
    query4 = {
        "size": 5,
        "query": {
            "bool": {
                "should": [
                    {"match": {"title": {"query": "refund", "boost": 3}}},
                    {"match": {"content": "refund"}},
                ],
                "filter": [{"term": {"category": "support"}}],
            }
        },
        "sort": [{"rating": {"order": "desc"}}],
    }
    status, result = request("POST", f"/{INDEX_NAME}/_search", query4)
    print_hits("Knowledge-base search", result)


def main() -> None:
    print(f"Connecting to Elasticsearch at {ES_URL}")
    try:
        request("DELETE", f"/{INDEX_NAME}")
    except RuntimeError:
        pass

    create_index()
    index_documents()
    request("POST", f"/{INDEX_NAME}/_refresh")
    run_use_cases()


if __name__ == "__main__":
    main()
