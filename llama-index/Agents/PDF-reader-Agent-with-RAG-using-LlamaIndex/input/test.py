from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory "database" for simplicity
items = []


# Create
@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    items.append(data)
    return jsonify(data), 201


# Read all
@app.route("/items", methods=["GET"])
def read_items():
    return jsonify(items)


# Read one
@app.route("/items/<int:item_id>", methods=["GET"])
def read_item(item_id):
    if item_id < 0 or item_id >= len(items):
        return "Item not found.", 404
    return jsonify(items[item_id])


# Update
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    if item_id < 0 or item_id >= len(items):
        return "Item not found.", 404
    data = request.get_json()
    items[item_id] = data
    return jsonify(data)


# Delete
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    if item_id < 0 or item_id >= len(items):
        return "Item not found.", 404
    del items[item_id]
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
