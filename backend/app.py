from flask import Flask, request, jsonify
from flask_cors import CORS
import osmnx as ox
import networkx as nx
from waitress import serve

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the graph for the Bengaluru region
G = ox.graph_from_place("Bengaluru, Karnataka, India", network_type="drive")

@app.route("/shortest-path", methods=["POST"])
def shortest_path():
    try:
        data = request.get_json()
        origin = tuple(data["origin"])
        destination = tuple(data["destination"])

        # Find the nearest nodes to the origin and destination
        origin_node = ox.distance.nearest_nodes(G, origin[1], origin[0])  # lng, lat
        destination_node = ox.distance.nearest_nodes(G, destination[1], destination[0])  # lng, lat

        # Calculate the shortest path
        shortest_path = nx.shortest_path(G, origin_node, destination_node, weight="length")
        path_coords = [(G.nodes[node]["y"], G.nodes[node]["x"]) for node in shortest_path]

        return jsonify({"path": path_coords})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
