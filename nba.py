from neo4j import GraphDatabase
from dotenv import load_dotenv
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

class GraphQuery:
    
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def get_upstream_nodes(self, node_id):
        with self._driver.session() as session:
            players = session.execute_read(self._fetch_upstream, node_id)
            result = []
            for player in players:
                result.append(player.data()['upstream_node']['name']) 
            return result

    def get_downstream_nodes(self, node_id):
        with self._driver.session() as session:
            players = session.execute_read(self._fetch_downstream, node_id)
            result = []
            for player in players:
                result.append(player.data()['downstream_node']['name'])
            return result

    @staticmethod
    def _fetch_upstream(tx, node_id):
        query = """
        MATCH (upstream_node)-[r:TEAMMATES|FORMER_TEAMMATES]->(n) 
        WHERE ID(n) = $node_id AND 'PLAYER' IN LABELS(upstream_node)
        RETURN upstream_node
        """
        result = tx.run(query, node_id=node_id)
        return list(result)

    @staticmethod
    def _fetch_downstream(tx, node_id):
        query = """
        MATCH (n)-[r:TEAMMATES]->(downstream_node) 
        WHERE ID(n) = $node_id AND 'PLAYER' IN LABELS(downstream_node)
        RETURN downstream_node
        """
        result = tx.run(query, node_id=node_id)
        return list(result)

@app.route('/upstream', methods=['GET'])
def upstream():
    node_id = request.args.get('node_id')
    if not node_id:
        return jsonify({"error": "node_id parameter is required"}), 400
    try:
        node_id = int(node_id)
        nodes = graph_query.get_upstream_nodes(node_id)
        print(nodes)
        return jsonify({"upstream_nodes": nodes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/downstream', methods=['GET'])
def downstream():
    node_id = request.args.get('node_id')
    if not node_id:
        return jsonify({"error": "node_id parameter is required"}), 400
    try:
        node_id = int(node_id)
        nodes = graph_query.get_downstream_nodes(node_id)
        return jsonify({"downstream_nodes": nodes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    load_dotenv()
    uri = os.getenv('URI')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')

    graph_query = GraphQuery(uri, user, password)
    app.run(debug=True, port=8080)

    # node_id_example = 4
    # print("Upstream nodes:", graph_query.get_upstream_nodes(node_id_example))
    # print("Downstream nodes:", graph_query.get_downstream_nodes(node_id_example))

    graph_query.close()
