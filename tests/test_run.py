from flask_testing import TestCase
from run import app
import json

class MyTests(TestCase):
    
    def create_app(self):
        return app

    # Test for successful user signup
    def test_signup_successful(self):
        with self.client:
            post_data = (
                {
                    'username': 'bebeto',
                    'password': 'secret',
                    'reenter_password': 'secret'
                }
            )
            response = self.client.post(
                'v1/users/signup',
                content_type = 'application/json',
                data = json.dumps(post_data)
            )
            reply = json.loads(response.data.decode())
            self.assertEquals(reply['username'], 'bebeto')
            self.assertEquals(response.status_code, 201)

    # Test for signup with empty username
    def test_signup_empty_username(self):
        with self.client:
            post_data = (
                {
                    'username': '',
                    'password': 'secret',
                    'reenter_password': 'secret'
                }
            )
            response = self.client.post(
                'v1/users/signup',
                content_type = 'application/json',
                data = json.dumps(post_data)
            )
            reply = json.loads(response.data.decode())
            self.assertEquals(reply['message'], 'Please enter your username')
            self.assertEquals(response.status_code, 400)

    # Test for signup with empty password
    def test_signup_empty_password(self):
        with self.client:
            post_data = (
                {
                    'username': 'bebeto',
                    'password': '',
                    'reenter_password': 'secret'
                }
            )
            response = self.client.post(
                'v1/users/signup',
                content_type = 'application/json',
                data = json.dumps(post_data)
            )
            reply = json.loads(response.data.decode())
            self.assertEquals(reply['message'], 'Please enter your password')
            self.assertEquals(response.status_code, 400)

    # Test for signup with empty reenter_password
    def test_signup_empty_reenter_password(self):
        with self.client:
            post_data = (
                {
                    'username': 'bebeto',
                    'password': 'secret',
                    'reenter_password': ''
                }
            )
            response = self.client.post(
                'v1/users/signup',
                content_type = 'application/json',
                data = json.dumps(post_data)
            )
            reply = json.loads(response.data.decode())
            self.assertEquals(reply['message'], 'Please re-enter your password')
            self.assertEquals(response.status_code, 400)

    # Test for signup with wrong reenter_password
    def test_signup_wrong_reenter_password(self):
        with self.client:
            post_data = (
                {
                    'username': 'bebeto',
                    'password': 'secret',
                    'reenter_password': 'not secret'
                }
            )
            response = self.client.post(
                'v1/users/signup',
                content_type = 'application/json',
                data = json.dumps(post_data)
            )
            reply = json.loads(response.data.decode())
            self.assertEquals(reply['message'], 'Your passwords do not match')
            self.assertEquals(response.status_code, 400)

    # Test for successful user login
    def test_login_successful(self):
        with self.client:
            signup_data = (
                {
                    'username': 'bebeto',
                    'password': 'secret',
                    'reenter_password': 'secret'
                }
            )
            self.client.post(
                'v1/users/signup',
                content_type = 'application/json',
                data = json.dumps(signup_data)
            )
            login_data = (
                {
                    'username': 'bebeto',
                    'password': 'secret',
                }
            )
            response = self.client.post(
                'v1/users/login',
                content_type = 'application/json',
                data = json.dumps(login_data)
            )
            reply = json.loads(response.data.decode())
            self.assertEquals(reply['message'], 'User successfully logged in')
            self.assertEquals(response.status_code, 201)

    
    # Test for login with empty username
    def test_login_empty_username(self):
        with self.client:
            signup_data = (
                {
                    'username': 'bebeto',
                    'password': 'secret',
                    'reenter_password': 'secret'
                }
            )
            self.client.post(
                'v1/users/signup',
                content_type = 'application/json',
                data = json.dumps(signup_data)
            )
            login_data = (
                {
                    'username': '',
                    'password': 'secret',
                }
            )
            response = self.client.post(
                'v1/users/login',
                content_type = 'application/json',
                data = json.dumps(login_data)
            )
            reply = json.loads(response.data.decode())
            self.assertEquals(reply['message'], 'Please enter your username')
            self.assertEquals(response.status_code, 400)

    # Test for login with empty password
    def test_login_empty_password(self):
        with self.client:
            signup_data = (
                {
                    'username': 'bebeto',
                    'password': 'secret',
                    'reenter_password': 'secret'
                }
            )
            self.client.post(
                'v1/users/signup',
                content_type = 'application/json',
                data = json.dumps(signup_data)
            )
            login_data = (
                {
                    'username': 'bebeto',
                    'password': '',
                }
            )
            response = self.client.post(
                'v1/users/login',
                content_type = 'application/json',
                data = json.dumps(login_data)
            )
            reply = json.loads(response.data.decode())
            self.assertEquals(reply['message'], 'Please enter your password')
            self.assertEquals(response.status_code, 400)

    # Test for login with wrong password
    def test_login_wrong_username(self):
        with self.client:
            signup_data = (
                {
                    'username': 'bebeto',
                    'password': 'secret',
                    'reenter_password': 'secret'
                }
            )
            self.client.post(
                'v1/users/signup',
                content_type = 'application/json',
                data = json.dumps(signup_data)
            )
            login_data = (
                {
                    'username': 'bebeto',
                    'password': 'not secret',
                }
            )
            response = self.client.post(
                'v1/users/login',
                content_type = 'application/json',
                data = json.dumps(login_data)
            )
            reply = json.loads(response.data.decode())
            self.assertEquals(reply['message'], 'Incorrect password')
            self.assertEquals(response.status_code, 400)

    # Test the create a request endpoint
    def test_create_requests(self):
        with self.client:
            post_data = (
                { 
                    "device_type":"laptop",
                    "fault_description": "Battery malfunctioning"
                }
            )
            response = self.client.post(
                '/v1/users/requests', 
                content_type = 'application/json', 
                data = json.dumps(post_data)
            )
            reply = json.loads(response.data.decode()) 
            self.assertTrue(reply['device-status'] in ['Pending', 'Rejected', 'Approved', 'Resolved'], True)
            self.assertEquals(response.status_code, 201)

    # Test the view all requests endpoint
    def test_view_requests(self):
        with self.client:
            post_data = (
                { 
                    "device_type":"laptop",
                    "fault_description": "Battery malfunctioning"
                }
            )
            self.client.post(
                '/v1/users/requests', 
                content_type = 'application/json', 
                data = json.dumps(post_data)
            )            
            response = self.client.get(
                '/v1/users/requests',
                content_type = 'application/json'
            )
            reply = json.loads(response.data.decode())
            self.assertEquals(reply['number of requests'], 3) 
            self.assertEquals(reply['requests'][0]['id'], 1) 
            self.assertEquals(reply['message'], 'successful') 
            self.assertEquals(response.status_code, 200)

    # Test the view particular request endpoint
    def test_view_user_request(self):
        with self.client:
            post_data = (
                { 
                    "device_type":"laptop",
                    "fault_description": "Battery malfunctioning"
                }
            )
            self.client.post(
                '/v1/users/requests', 
                content_type = 'application/json', 
                data = json.dumps(post_data)
            )
            #remove content type
            response = self.client.get(
                '/v1/users/requests/1', 
                content_type = 'application/json'
            )
            reply = json.loads(response.data.decode()) 
            self.assertTrue(reply['device-status'] in ['Pending', 'Rejected', 'Approved', 'Resolved'], True)
            self.assertEquals(reply['message'], 'successful')
            self.assertTrue(response.status_code, 200)

    # Test the modify a request endpoint
    def test_modify_request(self):
        with self.client:
            post_data = (
                { 
                    "device_type":"laptop",
                    "fault_description": "Battery malfunctioning"
                }
            )
            put_data = (
                {
                    "device_type":"computer",
                    "fault_description": "Dead screen"
                }
            )
            self.client.post(
                '/v1/users/requests', 
                content_type = 'application/json', 
                data = json.dumps(post_data)
            )
            response = self.client.put(
                '/v1/users/requests/1', 
                content_type = 'application/json',
                data = json.dumps(put_data)
            )
            reply = json.loads(response.data.decode())
            self.assertTrue(reply['device-status'] in ['Pending', 'Rejected', 'Approved', 'Resolved'], True)
            self.assertEquals(reply['device-type'], 'computer')
            self.assertEquals(response.status_code, 200)