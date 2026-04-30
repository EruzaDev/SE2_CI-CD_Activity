from flask import Flask, request, jsonify

app = Flask(__name__)

# -------------------------------------------------------------------
# In-memory store
# -------------------------------------------------------------------
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob",   "email": "bob@example.com"},
]
next_id = 3


# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------

@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify(users), 200


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = _find(user_id)
    if user is None:
        return jsonify({"error": "User not found."}), 404
    return jsonify(user), 200


@app.route("/api/users", methods=["POST"])
def create_user():
    global next_id
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400
    if "name" not in data or "email" not in data:
        return jsonify({"error": "Fields 'name' and 'email' are required."}), 400

    user = {"id": next_id, "name": data["name"], "email": data["email"]}
    users.append(user)
    next_id += 1
    return jsonify(user), 201


@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = _find(user_id)
    if user is None:
        return jsonify({"error": "User not found."}), 404

    data = request.get_json(silent=True) or {}
    if "name" in data:
        user["name"] = data["name"]
    if "email" in data:
        user["email"] = data["email"]

    return jsonify(user), 200


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = _find(user_id)
    if user is None:
        return jsonify({"error": "User not found."}), 404

    users.remove(user)
    return jsonify({"message": f"User {user_id} deleted."}), 200


# -------------------------------------------------------------------
# Helper
# -------------------------------------------------------------------

def _find(user_id):
    return next((u for u in users if u["id"] == user_id), None)


# -------------------------------------------------------------------
# Error handlers
# -------------------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found."}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed."}), 405


if __name__ == "__main__":
    app.run(debug=True, port=5000)
