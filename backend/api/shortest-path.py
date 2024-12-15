from flask import Flask, request, jsonify
import osmnx as ox
import networkx as nx

app = Flask(__name__)

# Load the graph of Bengaluru, India
G = ox.graph_from_place("Bengaluru, India", network_type="drive")

@app.route("/shortest-path", methods=["POST"])
def shortest_path():
    try:
        data = request.json
        origin = tuple(data["origin"])  # [latitude, longitude]
        destination = tuple(data["destination"])

        # Find the nearest nodes on the graph
        origin_node = ox.distance.nearest_nodes(G, origin[1], origin[0])
        destination_node = ox.distance.nearest_nodes(G, destination[1], destination[0])

        # Calculate the shortest path
        shortest_path = nx.shortest_path(G, origin_node, destination_node, weight="length")
        path_coords = [(G.nodes[node]["y"], G.nodes[node]["x"]) for node in shortest_path]

        return jsonify({"path": path_coords})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Exporting the Flask app for Vercel's serverless functions
if __name__ == "__main__":
    app.run(debug=True)
