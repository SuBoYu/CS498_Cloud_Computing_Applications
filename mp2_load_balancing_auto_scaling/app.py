from flask import Flask, request, jsonify

app = Flask(__name__)

seed_value = 100

@app.route("/", methods=['GET'])
def get_seed():
    return str(seed_value), 200

@app.route("/", methods=['POST'])
def update_seed():
    global seed_value
    try:
        data = request.get_json()
        if "num" in data and isinstance(data["num"], int):
            seed_value = data["num"]
            return jsonify({"message": f"Seed value updated successfully to {seed_value}"}), 200
        else:
            return jsonify({"error": "Invalid input. Expecting JSON {'num': <integer>}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)