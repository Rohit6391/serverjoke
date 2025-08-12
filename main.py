from flask import Flask, request, jsonify
from flask_cors import CORS
import secrets
import json
import os

app = Flask(__name__)
CORS(app)  # Allow all origins

# Store API keys in a file (persistent)
API_KEYS_FILE = "api_keys.json"
if os.path.exists(API_KEYS_FILE):
    with open(API_KEYS_FILE, "r") as f:
        api_keys = set(json.load(f))
else:
    api_keys = set()

# Load jokes
with open("jokes.json", "r", encoding="utf-8") as f:
    jokes = json.load(f)

# Save API keys
def save_keys():
    with open(API_KEYS_FILE, "w") as f:
        json.dump(list(api_keys), f)

@app.route("/generate-key", methods=["POST"])
def generate_key():
    new_key = f"Nk-{secrets.token_hex(8)}-en"
    api_keys.add(new_key)
    save_keys()
    return jsonify({"api_key": new_key})

@app.route("/jokes/random", methods=["GET"])
def get_joke():
    api_key = request.args.get("key")
    if not api_key or api_key not in api_keys:
        return jsonify({"error": "Invalid API Key"}), 403
    return jsonify({"joke": secrets.choice(jokes)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
