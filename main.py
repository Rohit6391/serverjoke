from flask import Flask, request, jsonify
import secrets
import json
import os
import random

app = Flask(__name__)

JOKES_FILE = "jokes.json"
API_KEYS_FILE = "api_keys.json"

# Load jokes
if os.path.exists(JOKES_FILE):
    with open(JOKES_FILE, "r", encoding="utf-8") as f:
        jokes = json.load(f)
else:
    jokes = []

# Load saved API keys
if os.path.exists(API_KEYS_FILE):
    with open(API_KEYS_FILE, "r", encoding="utf-8") as f:
        api_keys = set(json.load(f))
else:
    api_keys = set()

# Save API keys to file
def save_api_keys():
    with open(API_KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(api_keys), f, indent=2)

# Generate random API key in format Nk-xxxxx-en
def generate_api_key():
    random_part = secrets.token_hex(3)  # 6 characters hex
    return f"Nk-{random_part}-en"

# Endpoint to create API key
@app.route("/generate-key", methods=["POST"])
def create_api_key():
    new_key = generate_api_key()
    api_keys.add(new_key)
    save_api_keys()
    return jsonify({"api_key": new_key})

# Endpoint to get a random joke
@app.route("/jokes/random", methods=["GET"])
def get_random_joke():
    key = request.args.get("api_key")

    if not key or key not in api_keys:
        return jsonify({"error": "Invalid or missing API key"}), 403

    if not jokes:
        return jsonify({"error": "No jokes found"}), 404

    joke = random.choice(jokes)
    return jsonify({"joke": joke})

if __name__ == "__main__":
    app.run(debug=True)
