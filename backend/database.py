import sqlite3

# Initialize SQLite database
conn = sqlite3.connect("history.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS search_history (id INTEGER PRIMARY KEY, origin TEXT, destination TEXT)")
conn.commit()

@app.route("/save-search", methods=["POST"])
def save_search():
    try:
        data = request.get_json()
        origin = data["origin"]
        destination = data["destination"]

        # Save search to database
        cursor.execute("INSERT INTO search_history (origin, destination) VALUES (?, ?)", (str(origin), str(destination)))
        conn.commit()
        return jsonify({"message": "Search saved successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get-history", methods=["GET"])
def get_history():
    try:
        cursor.execute("SELECT origin, destination FROM search_history")
        history = [{"origin": eval(row[0]), "destination": eval(row[1])} for row in cursor.fetchall()]
        return jsonify({"history": history})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
