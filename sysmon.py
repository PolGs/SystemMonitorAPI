from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
import psutil

app = Flask(__name__)

# setup the JWT manager
app.config['JWT_SECRET_KEY'] = 'your_secret_api_key'
jwt = JWTManager(app)

@app.route('/')
def index():
    return 'Welcome to the System Monitoring API'

@app.route('/cpu')
@jwt_required()
def cpu():
    current_user = get_jwt_identity()
    if current_user == 'your_secret_api_key':
        cpu_percent = psutil.cpu_percent(interval=1)
        return jsonify(cpu_percent=cpu_percent)
    else:
        return jsonify(msg='Unauthorized'), 401

@app.route('/memory')
@jwt_required()
def memory():
    current_user = get_jwt_identity()
    if current_user == 'your_secret_api_key':
        memory_info = psutil.virtual_memory()
        return jsonify(memory_info._asdict())
    else:
        return jsonify(msg='Unauthorized'), 401

@app.route('/disk')
@jwt_required()
def disk():
    current_user = get_jwt_identity()
    if current_user == 'your_secret_api_key':
        disk_usage = psutil.disk_usage('/')
        return jsonify(disk_usage._asdict())
    else:
        return jsonify(msg='Unauthorized'), 401

@app.route('/login', methods=['POST'])
def login():
    # Get the json from the request
    json = request.get_json()
    # Extract the key
    key = json.get('key', None)
    if key == 'your_secret_api_key':
        # Create the access token
        access_token = create_access_token(identity=key)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(msg='Invalid key'), 401

if __name__ == '__main__':
    app.run(debug=True)
