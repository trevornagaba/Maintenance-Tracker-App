from flask import Flask, request, jsonify
from myapp.models import Request, User
import json

# A list to store requests
requests = []
users = []

app = Flask(__name__)

# Register a user
@app.route('/v1/users/signup', methods = ['POST'])
def signup():
    #Retrieve the data
    data = request.get_json()
    # Validate the data
    if not data['username']:
        return jsonify ({ 'message': 'Please enter your username' }), 400
    if not data['password']:
        return jsonify ({'message': 'Please enter your password'}), 400
    if not data['reenter_password']:
        return jsonify ({'message': 'Please re-enter your password'}), 400

    if data['password'] != data['reenter_password']:
        return jsonify ({'message': 'Your passwords do not match'}), 400

    user = User(data['username'], data['password'], data['reenter_password'])
    users.append(user)
    return jsonify (
        {
            'status': 'OK',
            'message': 'User registered',
            'username': users[-1].get_username(),
            'number of users': len(users)
        }
    ), 201

# Login a user
@app.route('/v1/users/login', methods = ['POST'])
def login():
    # Retrieve the data
    data = request.get_json()
    # Validate the data
    if not data['username']:
        return jsonify ({ 'message': 'Please enter your username' }), 400
    if not data['password']:
        return jsonify ({'message': 'Please enter your password'}), 400
    
    if len(users) > 0:
        for userz in users:
            print(data['password'])
            if userz.get_password() == data['password']:
                return jsonify ({'message': 'User successfully logged in'}), 201
        print (data['password'])
        return jsonify({'message': 'Incorrect password'}), 400

    return jsonify({'message': 'No users have been registered'})

#Create a request
@app.route('/v1/users/requests', methods = ['POST'])
def create_requests():
    # Retrieve the data
    data = request.get_json()
    # Validate the data
    if data['device_type'] == "" or data['fault_description'] == "" or data['device_status'] == "":
        return jsonify (
            {
                'status': 'FAILED',
                'message': 'One of the required fields is empty'
        }
        ), 400
    try:
        if isinstance(data['device_type'].encode(), str) and isinstance (data['fault_description'].encode(), str) and isinstance (data['device_status'].encode(), str):
            # Create id and store the data
            id = len(requests) + 1
            req =  Request(id, data['device_type'], data['fault_description'], data['device_status'])
            requests.append(req)
            return jsonify(
                {
                    'status':'OK',
                    'message': 'Request created successfully',
                    'id': id,
                    'device-status': requests[-1].get_device_status(),
                    'device-type': requests[-1].get_device_type()
                }
            ), 201
    except AttributeError:
        return jsonify(
            {
                'status':'FAILED',
                'message': 'Invalid request. Please check your entry',
            }
        ), 400

#Fetch all requests of a logged in user
@app.route('/v1/users/requests', methods = ['GET'])
def view_requests():
        return jsonify(
                {
                'number of requests': len(requests),
                'status':'OK', 
                'message':'successful',
                'requests': [my_requests.__dict__ for my_requests in requests]
                }
            ), 200

#Fetch a request that belongs to a logged in user
@app.route('/v1/users/requests/<id>', methods = ['GET'])
def view_user_requests(id):
    try:     
        # Convert id to integer 
        id_number = int(id)
        # Validate request
        if isinstance(id_number, int):
            return jsonify(
                {
                'status':'OK', 
                'message':'successful',
                'device-type': requests[id_number-1].get_device_type(),
                'fault description': requests[id_number-1].get_fault_description(),
                'device-status': requests[id_number-1].get_device_status(),
                'id': requests[id_number-1].id
                }
            ), 200
    # Catch none integer input
    except  ValueError:
        return jsonify(
            {
                'status':'FAILED',
                'message':'Invalid request id'
            }
        ), 400
    # Catch request for non-existent id
    except IndexError:
        return jsonify(
            {
                'status':'FAILED',
                'message':'Your request id does not exist'
            }
        ), 400

#Modify a request
@app.route('/v1/users/requests/<id>', methods = ['PUT'])
def modify_requests(id):
    # Retrieve the request
    data = request.get_json()
    # Validate the data
    if data['device_type'] == "" or data['fault_description'] == "" or data['device_status'] == "":
        return jsonify (
            {
                'status': 'OK',
                'message': 'One of the required fields is empty'
        }
        )
    try:
        id_number = int(id)
        if isinstance(data['device_type'].encode(), str) and isinstance(data['fault_description'].encode(), str) and isinstance(data['device_status'].encode(), str) and isinstance(id_number, int):
            # Store the data 
            requests[id_number-1].device_type = data['device_type'].encode()
            requests[id_number-1].fault_description = data['fault_description'].encode()
            requests[id_number-1].device_status = data['device_status'].encode()

            return jsonify(
                {
                'status': 'OK',
                'device-type': requests[id_number-1].get_device_type(),
                'fault-description': requests[id_number-1].get_fault_description(),
                'message': 'A request was modified',
                'request-id': id,
                'device-status': requests[id_number-1].get_device_status()
                }
            ), 200    
    except AttributeError:
        return jsonify(
            {
            'status': 'FAIL',
            'message': 'Failed to modify a request. Data is invalid'
            }
        ), 400
    except IndexError:
        return jsonify(
            {
            'status': 'FAIL',
            'message': 'Request id out of range'
            }
        ), 400

# Run the flask application
if __name__ == '__main__':
    app.run(debug = 'True')   