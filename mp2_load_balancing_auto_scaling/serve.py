from flask import Flask, request, jsonify
import subprocess
import socket

app = Flask(__name__)

@ app.route("/", methods=['GET'])
def get_private_ip():
    try:
        private_ip = socket.gethostbyname(socket.gethostname())
        return private_ip, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ app.route("/", methods=['POST'])
def stree_cpu():
    try:
        subprocess.Popen(["python3", "stress_cpu.py"])
        return jsonify({"message": "CPU stress started"}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)