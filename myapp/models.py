requests = []

class User():
    def __init__(self, username, password, reenter_password):
        self.username = username
        self.password = password
        self.reenter_password = reenter_password

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_reenter_password(self):
        return self.reenter_password

class Request():
    def __init__(self):
        self.requests = []

    def add_request(self, device_type, fault_description, device_status = 'Pending'):
        id = len(self.requests)+1
        request = {'id':id, 'device_type': device_type, 'fault_description': fault_description, 'device_status': device_status}
        self.requests.append(request)

    def get_request(self, id):
        return self.requests[id]

    def get_all_requests(self):
        return self.requests

    def modify_request(self, id, device_type, fault_description, device_status = 'Pending'):
        request = {'id':id, 'device_type': device_type, 'fault_description': fault_description, 'device_status': device_status}
        self.requests[id-1] = request

    def number_of_requests(self):
        length = len(self.requests)
        return length