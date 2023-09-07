from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

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

if __name__ == "__main__":
    load_dotenv()
    uri = os.getenv('URI')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')

    graph_query = GraphQuery(uri, user, password)

    node_id_example = 4
    print("Upstream nodes:", graph_query.get_upstream_nodes(node_id_example))
    print("Downstream nodes:", graph_query.get_downstream_nodes(node_id_example))

    graph_query.close()
