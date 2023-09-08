# Neo4j Graph Traversal API

This Flask application provides a simple API for traversing a Neo4j graph database, enabling users to fetch the upstream and downstream nodes of a given node.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Fetch Upstream Nodes](#fetch-upstream-nodes)
  - [Fetch Downstream Nodes](#fetch-downstream-nodes)

## Prerequisites

- Python 3.x
- Neo4j instance running
- Load the nba-data.cypher file into the Neo4j instance


## Installation

1. Clone the repository:

```bash
git clone [YOUR REPO URL]
cd [YOUR REPO DIRECTORY]
```

2. Install the required packages
```bash
pip install neo4j flask
```

## Running the Application

1. Start your Neo4j instance.
2. Execute the python script
```bash
python [YOUR SCRIPT NAME].py
```

Once executed, the Flask server will start on http://localhost:8080.

## API Endpoints

### Fetch Upstream Nodes

URL: GET /upstream?node_id=<NODE_ID>

Description: Retrieves the upstream nodes connected to the specified node.

Parameters: node_id - The ID of the node from which you wish to find the upstream nodes.

Example: http://localhost:8080/upstream?node_id=1234

### Fetch Downstream Nodes
URL: GET /downstream?node_id=<NODE_ID>

Description: Retrieves the downstream nodes connected to the specified node.

Parameters: node_id - The ID of the node from which you wish to find the downstream nodes.

Example: http://localhost:8080/downstream?node_id=1234

