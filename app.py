from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory user storage
users = {}
next_id = 1

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# GET a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

# POST a new user
@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    data = request.json
    if not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Missing name or email'}), 400
    users[next_id] = {
        'id': next_id,
        'name': data['name'],
        'email': data['email']
    }
    next_id += 1
    return jsonify(users[next_id - 1]), 201

# PUT to update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])
    return jsonify(user)

# DELETE a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        deleted_user = users.pop(user_id)
        return jsonify({'message': 'User deleted', 'user': deleted_user})
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
