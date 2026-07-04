# Elasticsearch Basics Plan

## 1. Objective
Learn the basics of Elasticsearch by setting up a local environment and practicing simple indexing and search operations.

## 2. What You Will Learn
By the end of this plan, you should understand:
- what Elasticsearch is
- how indices, documents, and fields work
- how to create an index
- how to insert sample data
- how to run basic search queries
- how Kibana helps you explore data

## 3. Suggested Local Setup
Use Docker for a quick and simple local setup.

### Recommended setup
- Run Elasticsearch and Kibana with Docker Compose
- Keep the setup minimal for learning
- Use localhost for testing

### Files to prepare
- docker-compose.yml
- a small sample dataset
- optional notes for queries

## 4. Learning Order
Follow these topics in order:
1. Elasticsearch basics and use cases
2. Cluster, node, index, and document concepts
3. Mapping and basic data types
4. Simple CRUD operations
5. Search queries such as match, term, and range
6. Filtering and aggregations
7. Basic Kibana exploration

## 5. First Hands-On Steps
1. Start Elasticsearch and Kibana
2. Verify the cluster is healthy
3. Create a sample index
4. Insert a few documents
5. Search the documents using simple queries
6. Try filters and basic aggregations
7. Explore the data in Kibana

## 6. Beginner Exercises
### Exercise 1: Create an index
- Create an index for products, users, or logs
- Define simple fields

### Exercise 2: Add sample data
- Insert 3 to 5 documents
- Observe how Elasticsearch stores them

### Exercise 3: Run searches
- Try a full-text match query
- Try an exact term query
- Try a range filter

### Exercise 4: Explore analytics
- Count documents
- Group by category or status
- Build a simple aggregation

## 7. Useful Elasticsearch Endpoints
- Check health: GET /_cluster/health
- List indices: GET /_cat/indices?v
- Create index: PUT /my_index
- Insert document: POST /my_index/_doc/1
- Search documents: GET /my_index/_search

## 8. Practical Use Cases
Elasticsearch is commonly used for:
- website search
- application search
- log analysis
- product search in e-commerce
- analytics dashboards

## 9. Suggested Study Plan
### Day 1
- Understand the basics of Elasticsearch
- Set up the local environment

### Day 2
- Learn indices, documents, and mappings
- Create a simple index

### Day 3
- Practice basic queries and filters

### Day 4
- Learn aggregations and simple analytics

### Day 5
- Build a small example project

## 10. Next Step
Start with a local setup, create one index, and run a few basic queries before moving to advanced topics.
