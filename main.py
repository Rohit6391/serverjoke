from flask import Flask, jsonify
from flask_cors import CORS
import random
import string

app = Flask(__name__)
CORS(app)  # allow CORS for local HTML access

# Store only one key at a time
api_key = None

def generate_api_key():
    middle = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"jk-{middle}-en"

@app.route('/get-key', methods=['GET'])
def get_key():
    global api_key
    if api_key is None:
        api_key = generate_api_key()
    return jsonify({"key": api_key})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
