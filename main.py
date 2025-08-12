from flask import Flask, request, jsonify
import json
import secrets
import os

app = Flask(__name__)

API_KEYS_FILE = "api_keys.json"
JOKES_FILE = "jokes.json"

# Load or create API keys file
if not os.path.exists(API_KEYS_FILE):
    with open(API_KEYS_FILE, "w") as f:
        json.dump([], f)

# Load jokes
if not os.path.exists(JOKES_FILE):
    jokes = []
else:
    with open(JOKES_FILE, "r", encoding="utf-8") as f:
        jokes = json.load(f)


# Generate API Key
def generate_api_key():
    return f"Nk-{secrets.token_hex(8)}-en"


# Save API Key
def save_api_key(key):
    with open(API_KEYS_FILE, "r") as f:
        keys = json.load(f)
    keys.append(key)
    with open(API_KEYS_FILE, "w") as f:
        json.dump(keys, f)


# Check if API Key exists
def is_valid_key(key):
    with open(API_KEYS_FILE, "r") as f:
        keys = json.load(f)
    return key in keys


@app.route("/generate-key", methods=["GET"])
def generate_key():
    key = generate_api_key()
    save_api_key(key)
    return jsonify({"api_key": key})


@app.route("/joke", methods=["GET"])
def get_joke():
    api_key = request.args.get("key")
    if not api_key or not is_valid_key(api_key):
        return jsonify({"error": "Invalid or missing API key"}), 403

    if not jokes:
        return jsonify({"error": "No jokes available"}), 500

    import random
    return jsonify({"joke": random.choice(jokes)})


if __name__ == "__main__":
    app.run(debug=True)
