from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    print("Received data:", data)
    return jsonify({"status": "success"}), 200

@app.route('/api/token/', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # For demonstration purposes, we'll use a simple check
    if username == 'testuser' and password == 'password':
        return jsonify({
            "access": "dummy_access_token",
            "refresh": "dummy_refresh_token"
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Global variable to store clients (for demonstration purposes)
clients = [
    {"id": 1, "name": "Client A", "contact_email": "clienta@example.com", "contact_phone": "123-456-7890"},
    {"id": 2, "name": "Client B", "contact_email": "clientb@example.com", "contact_phone": "098-765-4321"}
]

@app.route('/api/clients/', methods=['GET', 'POST'])
def handle_clients():
    if request.method == 'GET':
        return jsonify(clients), 200
    elif request.method == 'POST':
        new_client = request.json
        new_client['id'] = len(clients) + 1  # Simple ID assignment
        clients.append(new_client)
        return jsonify(new_client), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
